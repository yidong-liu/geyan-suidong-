/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

import { ACubismMotion } from './acubismmotion';
import { CubismMotionQueueEntry } from './cubismmotionqueueentry';
import { csmVector, iterator } from '../type/csmvector';
import { CubismModel } from '../model/cubismmodel';
import { csmString } from '../type/csmstring';

/**
*管理运动播放
*
*用于管理运动播放的类。用于播放ACubismMotion的子类，例如CubismMotion运动。
*
*@note再生过程中如果另一个运动被StartMotion（），则平滑地变化为新运动，旧运动中断。
*将表情用动作、体用动作等分开进行动作化时等
*要同时播放多个运动，请使用多个CubismMotionQueueManager实例。
*/
export class CubismMotionQueueManager {
    /**
    *构造函数
    */
  public constructor() {
    this._userTimeSeconds = 0.0;
    this._eventCallBack = null;
    this._eventCustomData = null;
    this._motions = new csmVector<CubismMotionQueueEntry>();
  }

    /**
    *析构函数
    */
  public release(): void {
    for (let i = 0; i < this._motions.getSize(); ++i) {
      if (this._motions.at(i)) {
        this._motions.at(i).release();
        this._motions.set(i, null);
      }
    }
    this._motions = null;
  }

/**
*启动指定的运动
*
*启动指定的运动。如果已经存在相同类型的运动，则在现有运动上建立结束标记以开始淡出。
*
*@param motion开始的运动
*@param autoDelete如果要删除播放结束的运动实例，则为真
*@param userTimeSeconds Deprecated：因为在增量时间的累计值[秒]函数内没有参照，所以不推荐使用。
*@return返回已启动运动的标识号。用于确定单独的运动是否结束的IsFinished（）的参数。无法开始时为“-1”
*/
  public startMotion(
    motion: ACubismMotion,
    autoDelete: boolean,
    userTimeSeconds?: number
  ): CubismMotionQueueEntryHandle {
    if (motion == null) {
      return InvalidMotionQueueEntryHandleValue;
    }

    let motionQueueEntry: CubismMotionQueueEntry = null;

    //如果已经有动作，则标记结束
    for (let i = 0; i < this._motions.getSize(); ++i) {
      motionQueueEntry = this._motions.at(i);
      if (motionQueueEntry == null) {
        continue;
      }
      motionQueueEntry.setFadeOut(motionQueueEntry._motion.getFadeOutTime()); //淡出设置
    }
    motionQueueEntry = new CubismMotionQueueEntry(); //结束时废弃
    motionQueueEntry._autoDelete = autoDelete;
    motionQueueEntry._motion = motion;
    this._motions.pushBack(motionQueueEntry);


    return motionQueueEntry._motionQueueEntryHandle;
  }
  public endMotion(motion: ACubismMotion,autoDelete:boolean){
    let motionQueueEntry: CubismMotionQueueEntry = null;
    for (let i = 0; i < this._motions.getSize(); ++i) {
        motionQueueEntry = this._motions.at(i);
        if (motionQueueEntry == null) {
          continue;
        }
        motionQueueEntry.setFadeOut(motionQueueEntry._motion.getFadeOutTime()); //淡出设置
      }
      motionQueueEntry = new CubismMotionQueueEntry(); //结束时废弃
      motionQueueEntry._autoDelete = autoDelete;
      motionQueueEntry._motion = motion;
      this._motions.pushBack(motionQueueEntry);
  }
  /**
    *确认所有运动结束
    *@return true全部结束
    *@return false未终止
   */
  public isFinished(): boolean {
    //------进行处理------
    //如果已经有动作，则标记结束
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());

    ) {
      let motionQueueEntry: CubismMotionQueueEntry = ite.ptr();

      if (motionQueueEntry == null) {
        ite = this._motions.erase(ite); // 削除
        continue;
      }

      const motion: ACubismMotion = motionQueueEntry._motion;

      if (motion == null) {
        motionQueueEntry.release();
        motionQueueEntry = null;
        ite = this._motions.erase(ite); // 削除
        continue;
      }

      //-----如果有结束的处理，则删除-----
      if (!motionQueueEntry.isFinished()) {
        return false;
      } else {
        ite.preIncrement();
      }
    }

    return true;
  }

    /**
    *确认指定运动结束
    *@param motionQueueEntryNumber运动的标识号
    *@return true全部结束
    *@return false未终止
    */
  public isFinishedByHandle(
    motionQueueEntryNumber: CubismMotionQueueEntryHandle
  ): boolean {
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());
      ite.increment()
    ) {
      const motionQueueEntry: CubismMotionQueueEntry = ite.ptr();

      if (motionQueueEntry == null) {
        continue;
      }

      if (
        motionQueueEntry._motionQueueEntryHandle == motionQueueEntryNumber &&
        !motionQueueEntry.isFinished()
      ) {
        return false;
      }
    }
    return true;
  }

    /**
    *停止所有运动
    * 拓展功能 实现渐出渐入
    */
  public stopAllMotions(): void {
    //------进行处理------
    //如果已经有动作，则标记结束
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());
    ) {
      let motionQueueEntry: CubismMotionQueueEntry = ite.ptr();

      if (motionQueueEntry && motionQueueEntry._motion) {
        ite = this._motions.erase(ite);
        continue;
    }    
      //-----如果有结束的处理，则删除-----
      motionQueueEntry.release();
      motionQueueEntry = null;
      ite = this._motions.erase(ite); // 削除
    }
    }

    /**
    *获取@brief CubismMotionQueueEntry数组
    *
    *获取CubismMotionQueueEntry数组。
    *
    *@return CubismMotionQueueEntry指向数组的指针
    *@retval NULL未找到
    */
  public getCubismMotionQueueEntries(): csmVector<CubismMotionQueueEntry> {
    return this._motions;
  }

    /**
   * 指定したCubismMotionQueueEntryの取得

   * @param   motionQueueEntryNumber  运动标识号
   * @return  指定したCubismMotionQueueEntry
   * @return  null   見つからなかった
   */
  public getCubismMotionQueueEntry(
    motionQueueEntryNumber: any
  ): CubismMotionQueueEntry {
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());
      ite.preIncrement()
    ) {
      const motionQueueEntry: CubismMotionQueueEntry = ite.ptr();

      if (motionQueueEntry == null) {
        continue;
      }

      if (motionQueueEntry._motionQueueEntryHandle == motionQueueEntryNumber) {
        return motionQueueEntry;
      }
    }

    return null;
  }

  /**
    *注册要接收事件的Callback
    *
    *@param callback回调函数
    *@param customData回调返回的数据
   */
  public setEventCallback(
    callback: CubismMotionEventFunction,
    customData: any = null
  ): void {
    this._eventCallBack = callback;
    this._eventCustomData = customData;
  }

    /**
    *更新运动以在模型中反映参数值。
    *
    *@param model对象的模型
    *@param userTimeSeconds增量时间累计值[秒]
    *@return true模型反映参数值
    *@return false模型不反映参数值（无运动变化）
    */
  public doUpdateMotion(model: CubismModel, userTimeSeconds: number): boolean {
    let updated = false;

    //------进行处理-------
    //如果已经有动作，则标记结束
    for (
      let ite: iterator<CubismMotionQueueEntry> = this._motions.begin();
      ite.notEqual(this._motions.end());

    ) {
      let motionQueueEntry: CubismMotionQueueEntry = ite.ptr();

      if (motionQueueEntry == null) {
        ite = this._motions.erase(ite); // 削除
        continue;
      }

      const motion: ACubismMotion = motionQueueEntry._motion;

      if (motion == null) {
        motionQueueEntry.release();
        motionQueueEntry = null;
        ite = this._motions.erase(ite); // 削除

        continue;
      }

      //-----反映值-----
      motion.updateParameters(model, motionQueueEntry, userTimeSeconds);
      updated = true;

      //-----检查用户触发事件-----
      const firedList: csmVector<csmString> = motion.getFiredEvent(
        motionQueueEntry.getLastCheckEventSeconds() -
          motionQueueEntry.getStartTime(),
        userTimeSeconds - motionQueueEntry.getStartTime()
      );

      for (let i = 0; i < firedList.getSize(); ++i) {
        this._eventCallBack(this, firedList.at(i), this._eventCustomData);
      }

      motionQueueEntry.setLastCheckEventSeconds(userTimeSeconds);

      //-----如果有完成的处理，则删除-----
      if (motionQueueEntry.isFinished()) {
        motionQueueEntry.release();
        motionQueueEntry = null;
        ite = this._motions.erase(ite); // 削除
      } else {
        if (motionQueueEntry.isTriggeredFadeOut()) {
          motionQueueEntry.startFadeOut(
            motionQueueEntry.getFadeOutSeconds(),
            userTimeSeconds
          );
        }
        ite.preIncrement();
      }
    }

    return updated;
  }
  _userTimeSeconds: number; // 增量时间累计值[秒]

  _motions: csmVector<CubismMotionQueueEntry>; // モーション
  _eventCallBack: CubismMotionEventFunction; // コールバック関数
  _eventCustomData: any; // コールバックに戻されるデータ
}

/**
*定义事件的回调函数
*
*可以在事件回调中注册的函数类型信息
*@param caller点燃事件的CubismMotionQueueManager
*@param eventValue点燃事件的字符串数据
*@param customData回调中返回的注册时指定的数据
 */
export interface CubismMotionEventFunction {
  (
    caller: CubismMotionQueueManager,
    eventValue: csmString,
    customData: any
  ): void;
}

/**
*运动标识号
*
*定义运动标识号
 */
export declare type CubismMotionQueueEntryHandle = any;
export const InvalidMotionQueueEntryHandleValue: CubismMotionQueueEntryHandle =
  -1;

// Namespace definition for compatibility.
import * as $ from './cubismmotionqueuemanager';
// eslint-disable-next-line @typescript-eslint/no-namespace
export namespace Live2DCubismFramework {
  export const CubismMotionQueueManager = $.CubismMotionQueueManager;
  export type CubismMotionQueueManager = $.CubismMotionQueueManager;
  export const InvalidMotionQueueEntryHandleValue =
    $.InvalidMotionQueueEntryHandleValue;
  export type CubismMotionQueueEntryHandle = $.CubismMotionQueueEntryHandle;
  export type CubismMotionEventFunction = $.CubismMotionEventFunction;
}
