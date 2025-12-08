/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

import { CubismFramework, Option } from '@framework/live2dcubismframework';

import * as LAppDefine from './lappdefine';
import { LAppLive2DManager } from './lapplive2dmanager';
import { LAppPal } from './lapppal';
import { LAppTextureManager } from './lapptexturemanager';
import { LAppView } from './lappview';
import { canvas, gl } from './lappglmanager';

export let s_instance: LAppDelegate = null;
export let frameBuffer: WebGLFramebuffer = null;
export let selectionMonitor: SelectionMonitor = null;

import { SelectionMonitor } from './lappselectionmonitor';

/**import
  *  应用程序类。
  *  管理Cubism SDK。
 */
export class LAppDelegate {
/**
*返回类的实例（单个）。
*如果未生成实例，则在内部生成实例。
*
*@return类实例
*/
  public static getInstance(): LAppDelegate {
    if (s_instance == null) {
      s_instance = new LAppDelegate();
    }

    return s_instance;
  }

/**
*释放类的实例（单个）。
*/
  public static releaseInstance(): void {
    if (s_instance != null) {
      s_instance.release();
    }

    s_instance = null;
  }

/**
*初始化APP所需的内容。
*/
  public initialize(): boolean {
    // キャンバスを DOM に追加
    var sanyueContainer = document.getElementById('sanyue');
    sanyueContainer.appendChild(canvas);
    if (LAppDefine.CanvasSize === 'auto') {
      this._resizeCanvas();
    } else {
      canvas.width = LAppDefine.CanvasSize.width;
      canvas.height = LAppDefine.CanvasSize.height;
    }

    if (!frameBuffer) {
      frameBuffer = gl.getParameter(gl.FRAMEBUFFER_BINDING);
    }
    //透过设定
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    const supportTouch: boolean = 'ontouchend' in canvas;

    if (supportTouch) {
      // 触摸关联回调函数登录
      canvas.addEventListener('touchstart', onTouchBegan, { passive: true });
      canvas.addEventListener('touchmove', onTouchMoved, { passive: true });
      canvas.addEventListener('touchend', onTouchEnded, { passive: true });
      canvas.addEventListener('touchcancel', onTouchCancel, { passive: true });
    } else {
      // 鼠标关联回调函数注册
      canvas.addEventListener('mousedown', onClickBegan, { passive: true });
      canvas.addEventListener('mousemove', onMouseMoved, { passive: true });
      canvas.addEventListener('mouseup', onClickEnded, { passive: true });
    }

    // 初始化AppView
    this._view.initialize();

    // 初始化Cubism SDK
    this.initializeCubism();

    return true;
  }

  /**
   * 调整画布大小并重新初始化视图。
   */
  public onResize(): void {
    this._resizeCanvas();
    this._view.initialize();
    this._view.initializeSprite();
  }

  /**
   * 解放
   */
  public release(): void {
    this._textureManager.release();
    this._textureManager = null;

    this._view.release();
    this._view = null;

    // 释放资源
    LAppLive2DManager.releaseInstance();

    // 释放Cubism SDK
    CubismFramework.dispose();
  }

  /**
   * 实时处理
   */
  public run(): void {
    //主循环
    const loop = (): void => {
      //确认是否有实例
      if (s_instance == null) {
        return;
      }

      // 时间更新
      LAppPal.updateTime();

      // 画面初始化
      gl.clearColor(0.0, 0.0, 0.0, 0);

      // 启用深度测试
      gl.enable(gl.DEPTH_TEST);

      // 附近的物体会掩盖远处的物体
      gl.depthFunc(gl.LEQUAL);

      // 清除颜色缓冲区和深度缓冲区
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

      gl.clearDepth(1.0);

      // 透过设定
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

      // 描画更新
      this._view.render();

      // 循环的递归调用
      requestAnimationFrame(loop);
    };
    loop();
  }

  /**
   * 注册着色器。
   */
  public createShader(): WebGLProgram {
    // 编译条形着色器
    const vertexShaderId = gl.createShader(gl.VERTEX_SHADER);

    if (vertexShaderId == null) {
      LAppPal.printMessage('failed to create vertexShader');
      return null;
    }

    const vertexShader: string =
      'precision mediump float;' +
      'attribute vec3 position;' +
      'attribute vec2 uv;' +
      'varying vec2 vuv;' +
      'void main(void)' +
      '{' +
      '   gl_Position = vec4(position, 1.0);' +
      '   vuv = uv;' +
      '}';

    gl.shaderSource(vertexShaderId, vertexShader);
    gl.compileShader(vertexShaderId);

    // 编译碎片着色器
    const fragmentShaderId = gl.createShader(gl.FRAGMENT_SHADER);

    if (fragmentShaderId == null) {
      LAppPal.printMessage('failed to create fragmentShader');
      return null;
    }

    const fragmentShader: string =
      'precision mediump float;' +
      'varying vec2 vuv;' +
      'uniform sampler2D texture;' +
      'void main(void)' +
      '{' +
      '   gl_FragColor = texture2D(texture, vuv);' +
      '}';

    gl.shaderSource(fragmentShaderId, fragmentShader);
    gl.compileShader(fragmentShaderId);

    // 创建程序对象
    const programId = gl.createProgram();
    gl.attachShader(programId, vertexShaderId);
    gl.attachShader(programId, fragmentShaderId);

    gl.deleteShader(vertexShaderId);
    gl.deleteShader(fragmentShaderId);

    // 链接
    gl.linkProgram(programId);

    gl.useProgram(programId);

    return programId;
  }
  /**
   * 获取查看信息。
   */
  public getView(): LAppView {
    return this._view;
  }

  public getTextureManager(): LAppTextureManager {
    return this._textureManager;
  }

  /**
   * 构造函数
   */
  constructor() {
    this._captured = false;
    this._mouseX = 0.0;
    this._mouseY = 0.0;
    this._isEnd = false;
    this._cubismOption = new Option();
    this._view = new LAppView();
    this._textureManager = new LAppTextureManager();
    this._monitor = new SelectionMonitor();

   
  }

  /**
   * 初始化Cubism SDK
   */
  public initializeCubism(): void {
    // setup cubism
    this._cubismOption.logFunction = LAppPal.printMessage;
    this._cubismOption.loggingLevel = LAppDefine.CubismLoggingLevel;
    CubismFramework.startUp(this._cubismOption);

    // initialize cubism
    CubismFramework.initialize();

    // load model
    LAppLive2DManager.getInstance();
   

    LAppPal.updateTime();

    this._view.initializeSprite();

  }

  /**
   * 调整画布大小以填充屏幕。
   */
  
  private _resizeCanvas(): void {
    canvas.width = canvas.clientWidth * window.devicePixelRatio;
    canvas.height = canvas.clientHeight * window.devicePixelRatio;
    gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);
  }

  _cubismOption: Option; // Cubism SDK Option
  _view: LAppView; // View情报
  _captured: boolean;
  _mouseX: number; 
  _mouseY: number; 
  _isEnd: boolean;
  _textureManager: LAppTextureManager; 
  _monitor: SelectionMonitor;
}




/**
 * 点击时操作。
 */
function onClickBegan(e: MouseEvent): void {
  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }
  LAppDelegate.getInstance()._captured = true;
  const posX: number = e.pageX;
  const posY: number = e.pageY;
  LAppDelegate.getInstance()._view.onTouchesBegan(posX, posY);
}

/**
 * 当鼠标指针移动时被称为。
 */
function onMouseMoved(e: MouseEvent): void {
  if (!LAppDelegate.getInstance()._captured) {
    return;
  }

  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  const rect = (e.target as Element).getBoundingClientRect();
  const posX: number = e.clientX - rect.left;
  const posY: number = e.clientY - rect.top;

  LAppDelegate.getInstance()._view.onTouchesMoved(posX, posY);
}

/**
 * 点击结束后被叫。
 */
function onClickEnded(e: MouseEvent): void {
  LAppDelegate.getInstance()._captured = false;
  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  const rect = (e.target as Element).getBoundingClientRect();
  const posX: number = e.clientX - rect.left;
  const posY: number = e.clientY - rect.top;

  LAppDelegate.getInstance()._view.onTouchesEnded(posX, posY);
}

/**
 * 触摸的时候被叫。
 */
function onTouchBegan(e: TouchEvent): void {
  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  LAppDelegate.getInstance()._captured = true;

  const posX = e.changedTouches[0].pageX;
  const posY = e.changedTouches[0].pageY;

  LAppDelegate.getInstance()._view.onTouchesBegan(posX, posY);
}

/**
 * 被称为天鹅。
 */
function onTouchMoved(e: TouchEvent): void {
  if (!LAppDelegate.getInstance()._captured) {
    return;
  }

  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  const rect = (e.target as Element).getBoundingClientRect();

  const posX = e.changedTouches[0].clientX - rect.left;
  const posY = e.changedTouches[0].clientY - rect.top;

  LAppDelegate.getInstance()._view.onTouchesMoved(posX, posY);
}

/**
 * 触摸结束后被叫。
 */
function onTouchEnded(e: TouchEvent): void {
  LAppDelegate.getInstance()._captured = false;

  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  const rect = (e.target as Element).getBoundingClientRect();

  const posX = e.changedTouches[0].clientX - rect.left;
  const posY = e.changedTouches[0].clientY - rect.top;

  LAppDelegate.getInstance()._view.onTouchesEnded(posX, posY);
}

/**
 * 被称为触摸被取消。
 */
function onTouchCancel(e: TouchEvent): void {
  LAppDelegate.getInstance()._captured = false;

  if (!LAppDelegate.getInstance()._view) {
    LAppPal.printMessage('view notfound');
    return;
  }

  const rect = (e.target as Element).getBoundingClientRect();

  const posX = e.changedTouches[0].clientX - rect.left;
  const posY = e.changedTouches[0].clientY - rect.top;

  LAppDelegate.getInstance()._view.onTouchesEnded(posX, posY);
}
