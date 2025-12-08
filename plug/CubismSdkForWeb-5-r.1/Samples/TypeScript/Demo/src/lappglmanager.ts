/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

export let canvas: HTMLCanvasElement = null;
export let gl: WebGLRenderingContext = null;
export let s_instance: LAppGlManager = null;

/**
 * 用于管理Cubism SDK示例中使用的WebGL的类
 */
export class LAppGlManager {
  /**
   * 返回一个类的实例。
   * 如果未生成实例，则在内部生成实例。
   *
   * @return 类实例
   */
  public static getInstance(): LAppGlManager {
    if (s_instance == null) {
      s_instance = new LAppGlManager();
    }

    return s_instance;
  }

  /**
   * 释放一个类的实例（单个）。
   */
  public static releaseInstance(): void {
    if (s_instance != null) {
      s_instance.release();
    }

    s_instance = null;
  }

  constructor() {
    canvas = <HTMLCanvasElement>document.getElementById("live2d");
    // 创建画布
    // 创建看板娘切换按钮  
    // var toggleButton = document.createElement('div');  
    // toggleButton.id = 'sanyue-toggle';  
    // toggleButton.innerHTML = '<span>看板娘</span>';  
      
    // // 创建看板娘容器  
    // var sanyueContainer = document.createElement('div');  
    // sanyueContainer.id = 'sanyue';  
      
    // // 创建提示容器  
    // var tipsContainer = document.createElement('div');  
    // tipsContainer.id = 'sanyue-tips';  
    // sanyueContainer.appendChild(tipsContainer);  
      
    // // 创建Live2D画布容器  
    // var live2dCanvas = document.createElement('canvas');
    // live2dCanvas.id = 'live2d';  
    // live2dCanvas.className = 'Canvas left';  
    // sanyueContainer.appendChild(live2dCanvas);  
      
    // // 创建工具容器（如果需要）  
    // var toolContainer = document.createElement('div');  
    // toolContainer.id = 'sanyue-tool';  
    // sanyueContainer.appendChild(toolContainer);  
      
    // // 将看板娘切换按钮和容器添加到body中  
    // document.body.appendChild(toggleButton);  
    // document.body.appendChild(sanyueContainer);  
    // // glコンテキストを初期化
    // // @ts-ignore
    // canvas = live2dCanvas
    gl = canvas.getContext('webgl2');

    if (!gl) {
      // gl初期化失敗
      alert('无法初始化WebGL。此浏览器不支持。');
      gl = null;

      document.body.innerHTML =
        '此浏览器不支持<code>&lt；画布&gt</代码>元素。';
    }
  }

  /**
   * 解放
   */
  public release(): void {}
}
