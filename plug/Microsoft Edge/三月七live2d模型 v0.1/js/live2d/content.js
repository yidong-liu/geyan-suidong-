(function() {  
    // 创建看板娘切换按钮  
    var toggleButton = document.createElement('div');  
    toggleButton.id = 'sanyue-toggle';  
    toggleButton.innerHTML = '<span>看板娘</span>';  
  
    // 创建看板娘容器  
    var sanyueContainer = document.createElement('div');  
    sanyueContainer.id = 'sanyue';  
  
    // 创建提示容器  
    var tipsContainer = document.createElement('div');  
    tipsContainer.id = 'sanyue-tips';  
    sanyueContainer.appendChild(tipsContainer);  
  
    // 创建Live2D画布容器  
    var live2dCanvas = document.createElement('div');  
    live2dCanvas.id = 'live2d';  
    live2dCanvas.className = 'Canvas left';  
    sanyueContainer.appendChild(live2dCanvas);  
  
    // 创建工具容器（如果需要）  
    var toolContainer = document.createElement('div');  
    toolContainer.id = 'sanyue-tool';  
    sanyueContainer.appendChild(toolContainer);  
  
    // 将看板娘切换按钮和容器添加到body中  
    document.body.appendChild(toggleButton);  
    document.body.appendChild(sanyueContainer);  
  })();
