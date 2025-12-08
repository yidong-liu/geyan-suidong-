/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

import { LogLevel } from '@framework/live2dcubismframework';

/**
 * Sample Appで使用する定数
 */

// Canvas width and height pixel values, or dynamic screen size ('auto').
// export const CanvasSize: { width: number; height: number } | 'auto' = {  
//     width: 200,  // 指定宽度  
//     height: 280  // 指定高度  
//   };
// var rootPath = chrome.runtime.getURL(
//     "js/model/march_7/expressions/1.exp3.json"
//   );
//   let parts = rootPath.split("/js/");
//   if (parts.length > 1) {
//     rootPath = parts[0] + "/js/model/";
//   } else {
//     rootPath = "";
//   }
var rootPath = './model/'
export const CanvasSize: { width: number; height: number } | 'auto' = 'auto';
// 画面
export const ViewScale = 1.0;
export const ViewMaxScale = 2.0;
export const ViewMinScale = 0.8;

export const ViewLogicalLeft = -1.0;
export const ViewLogicalRight = 1.0;
export const ViewLogicalBottom = -1.0;
export const ViewLogicalTop = 1.0;

export const ViewLogicalMaxLeft = -2.0;
export const ViewLogicalMaxRight = 2.0;
export const ViewLogicalMaxBottom = -2.0;
export const ViewLogicalMaxTop = 2.0;

// 相対パス
export const ResourcesPath = rootPath;

// モデルの後ろにある背景の画像ファイル
export const BackImageName = '';

// 歯車
export const GearImageName = '';

// 終了ボタン
export const PowerImageName = 'CloseNormal.png';

// モデル定義---------------------------------------------
// モデルを配置したディレクトリ名の配列
// ディレクトリ名とmodel3.jsonの名前を一致させておくこと
export const ModelDir: string[] = [
    'march_7'
];
export const ModelDirSize: number = ModelDir.length;

// 外部定義ファイル（json）と合わせる
export const MotionGroupIdle = 'Idle'; // アイドリング
export const MotionGroupTapBody = 'TapBody'; // 体をタップしたとき

//与外部定义文件（json）匹配
export const HitAreaNameHead = 'Head';
export const HitAreaNameBody = 'Body';

//运动优先级常数
export const PriorityNone = 0;
export const PriorityIdle = 1;
export const PriorityNormal = 2;
export const PriorityForce = 3;

//MOC3一致性验证选项
export const MOCConsistencyValidationEnable = true;

//调试日志显示选项
export const DebugLogEnable = true;
export const DebugTouchLogEnable = false;
//从框架输出的日志级别设置
export const CubismLoggingLevel: LogLevel = LogLevel.LogLevel_Verbose;

//默认渲染目标大小
export const RenderTargetWidth = 450;
export const RenderTargetHeight = 480;
