import { CubismId, CubismIdHandle } from '../id/cubismid';
import { LogLevel, csmDelete } from '../live2dcubismframework';
import { CubismModel } from '../model/cubismmodel';
import { csmVector, iterator } from '../type/csmvector';
import { ACubismMotion } from './acubismmotion';
import { CubismExpressionMotion } from './cubismexpressionmotion';
import { CubismMotionQueueEntry } from './cubismmotionqueueentry';
import {
  CubismMotionQueueEntryHandle,
  CubismMotionQueueManager
} from './cubismmotionqueuemanager';

/**
 * @brief 具有应用于参数表情值的结构体
 */
export class ExpressionParameterValue {
  parameterId: CubismIdHandle; // パラメーターID
  additiveValue: number; // 加算値
  multiplyValue: number; // 乗算値
  overwriteValue: number; // 上書き値
}

/**
 * @brief 表情モーションの管理
 *
 * 进行表情动作管理的班级。
 */
export class CubismExpressionMotionManager extends CubismMotionQueueManager {
  /**
   * コンストラクタ
   */
  public constructor() {
    super();
    this._currentPriority = 0;
    this._reservePriority = 0;
    this._expressionParameterValues = new csmVector<ExpressionParameterValue>();
    this._fadeWeights = new csmVector<number>();
  }

  /**
   * デストラクタ相当の処理
   */
  public release(): void {
    if (this._expressionParameterValues) {
      csmDelete(this._expressionParameterValues);
      this._expressionParameterValues = null;
    }

    if (this._fadeWeights) {
      csmDelete(this._fadeWeights);
      this._fadeWeights = null;
    }
  }

  /**
   * @brief 再生中のモーションの優先度の取得
   *
   * 再生中のモーションの優先度を取得する。
   *
   * @returns モーションの優先度
   */
  public getCurrentPriority(): number {
    return this._currentPriority;
  }

  /**
   * @brief 予約中のモーションの優先度の取得
   *
   * 予約中のモーションの優先度を取得する。
   *
   * @return  モーションの優先度
   */
  public getReservePriority(): number {
    return this._reservePriority;
  }

  /**
   * @brief 再生中のモーションのウェイトを取得する。
   *
   * @param[in]    index    表情のインデックス
   * @returns               表情モーションのウェイト
   */
  public getFadeWeight(index: number): number {
    return this._fadeWeights.at(index);
  }

  /**
   * @brief 予約中のモーションの優先度の設定
   *
   * 予約中のモーションの優先度を設定する。
   *
   * @param[in]   priority     優先度
   */
  public setReservePriority(priority: number) {
    this._reservePriority = priority;
  }

/**
*@brief设置优先级以开始运动
*
*设置优先级以开始运动。
*
*@param[in]motion运动
*@param[in]autoDelete删除播放结束的运动实例时为真
*@param[in]priority优先级
*@return返回已启动运动的标识号。用于确定单独的运动是否结束的IsFinished（）的参数。无法开始时为“-1”
*/
  public startMotionPriority(
    motion: ACubismMotion,
    autoDelete: boolean,
    priority: number,
    userTimeSeconds?: number
  ): CubismMotionQueueEntryHandle {
    if (priority == this.getReservePriority()) {
      this.setReservePriority(0);
    }
    this._currentPriority = priority;

    this._fadeWeights.pushBack(0.0);

    return this.startMotion(motion, autoDelete,userTimeSeconds);
  }

    /**
    *@brief更新运动
    *
    *更新运动以在模型中反映参数值。
    *
    *@param[in]model对象的模型
    *@param[in]deltaTimeSeconds增量时间[秒]
    *@retval true已更新
    *@retval false未更新
    */
  public updateMotion(model: CubismModel, deltaTimeSeconds: number): boolean {
    this._userTimeSeconds += deltaTimeSeconds;
    let updated = false;
    const motions = this.getCubismMotionQueueEntries();

    let expressionWeight = 0.0;
    let expressionIndex = 0;

    //------进行处理-------
    //如果已经有动作，则标记结束
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());

    ) {
      const motionQueueEntry = ite.ptr();

      if (motionQueueEntry == null) {
        ite = motions.erase(ite); //削除
        continue;
      }

      const expressionMotion = <CubismExpressionMotion>(
        motionQueueEntry.getCubismMotion()
      );

      if (expressionMotion == null) {
        csmDelete(motionQueueEntry);
        ite = motions.erase(ite); //削除
        continue;
      }

      const expressionParameters = expressionMotion.getExpressionParameters();
      if (motionQueueEntry.isAvailable()) {
        //列出正在播放的Expression引用的所有参数
        for (let i = 0; i < expressionParameters.getSize(); ++i) {
          if (expressionParameters.at(i).parameterId == null) {
            continue;
          }

          let index = -1;
          //搜索列表中是否存在参数ID
          for (let j = 0; j < this._expressionParameterValues.getSize(); ++j) {
            if (
              this._expressionParameterValues.at(j).parameterId !=
              expressionParameters.at(i).parameterId
            ) {
              continue;
            }

            index = j;
            break;
          }

          if (index >= 0) {
            continue;
          }

          //如果列表中不存在参数，则添加新参数
          const item: ExpressionParameterValue = new ExpressionParameterValue();
          item.parameterId = expressionParameters.at(i).parameterId;
          item.additiveValue = CubismExpressionMotion.DefaultAdditiveValue;
          item.multiplyValue = CubismExpressionMotion.DefaultMultiplyValue;
          item.overwriteValue = model.getParameterValueById(item.parameterId);
          this._expressionParameterValues.pushBack(item);
        }
      }

      //-----计算值-----
      expressionMotion.setupMotionQueueEntry(
        motionQueueEntry,
        this._userTimeSeconds
      );
      this._fadeWeights.set(
        expressionIndex,
        expressionMotion.updateFadeWeight(
          motionQueueEntry,
          this._userTimeSeconds
        )
      );
      expressionMotion.calculateExpressionParameters(
        model,
        this._userTimeSeconds,
        motionQueueEntry,
        this._expressionParameterValues,
        expressionIndex,
        this._fadeWeights.at(expressionIndex)
      );

      expressionWeight +=
        expressionMotion.getFadeInTime() == 0.0
          ? 1.0
          : CubismMath.getEasingSine(
              (this._userTimeSeconds - motionQueueEntry.getFadeInStartTime()) /
                expressionMotion.getFadeInTime()
            );

      updated = true;
      if (motionQueueEntry.isTriggeredFadeOut()) {
       //开始淡出
        motionQueueEntry.startFadeOut(
          motionQueueEntry.getFadeOutSeconds(),
          this._userTimeSeconds
        );
      }

      ite.preIncrement();
      ++expressionIndex;
    }
    //-----如果最新的Expression淡入已完成，则删除以前的内容-----
    if (motions.getSize() > 1) {
      const expressionMotion = <CubismExpressionMotion>(
        motions.at(motions.getSize() - 1).getCubismMotion()
      );
      const latestFadeWeight: number = this._fadeWeights.at(
        this._fadeWeights.getSize() - 1
      );
      if (latestFadeWeight >= 1.0) {
        //不删除数组的最后一个元素
        setTimeout(()=>{
            for (let i = motions.getSize() - 2; i >= 0; --i) {
                const motionQueueEntry = motions.at(i);
                csmDelete(motionQueueEntry);
                motions.remove(i);
                this._fadeWeights.remove(i);
              }
        },2000)

      }
    }

    if (expressionWeight > 1.0) {
      expressionWeight = 1.0;
    }

    //将每个值应用于模型
    for (let i = 0; i < this._expressionParameterValues.getSize(); ++i) {
      const expressionParameterValue = this._expressionParameterValues.at(i);
      model.setParameterValueById(
        expressionParameterValue.parameterId,
        (expressionParameterValue.overwriteValue +
          expressionParameterValue.additiveValue) *
          expressionParameterValue.multiplyValue,
        expressionWeight
      );

      expressionParameterValue.additiveValue =
        CubismExpressionMotion.DefaultAdditiveValue;
      expressionParameterValue.multiplyValue =
        CubismExpressionMotion.DefaultMultiplyValue;
    }

    return updated;
  }

  private _expressionParameterValues: csmVector<ExpressionParameterValue>; ///<应用于模型的每个参数的值
  private _fadeWeights: csmVector<number>; ///<播放中的表情权重
  private _currentPriority: number; ///<当前播放的运动优先级
  private _reservePriority: number; ///<要播放的运动的优先级。播放中为0。在其他线程中导入运动文件时的功能。
  private _startExpressionTime: number; ///<表情的再生开始时间
}

// Namespace definition for compatibility.
import * as $ from './cubismexpressionmotionmanager';
import { CubismMath } from '../math/cubismmath';
import { CubismDebug, CubismLogError } from '../utils/cubismdebug';
// eslint-disable-next-line @typescript-eslint/no-namespace
export namespace Live2DCubismFramework {
  export const CubismExpressionMotionManager = $.CubismExpressionMotionManager;
  export type CubismExpressionMotionManager = $.CubismExpressionMotionManager;
}
