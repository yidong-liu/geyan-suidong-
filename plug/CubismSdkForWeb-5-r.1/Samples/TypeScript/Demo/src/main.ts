/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

import { LAppDelegate } from './lappdelegate';
import * as LAppDefine from './lappdefine';
import { LAppGlManager } from './lappglmanager';

/**
 * 浏览器加载后的处理
 */
window.addEventListener(
  'load',
  (): void => {
    // 初始化WebGL并创建应用程序实例
    if (
      !LAppGlManager.getInstance() ||
      !LAppDelegate.getInstance().initialize()
    ) {
      return;
    }
    
    LAppDelegate.getInstance().run();
  },
  { passive: true }
);

/**
 * 结束时的处理
 */
window.addEventListener(
  'beforeunload',
  (): void => LAppDelegate.releaseInstance(),
  { passive: true }
);

/**
 * Process when changing screen size.
 */
// window.addEventListener(
//   'resize',
//   () => {
//     if (LAppDefine.CanvasSize === 'auto') {
//       LAppDelegate.getInstance().onResize();
//     }
//   },
//   { passive: true }
// );
