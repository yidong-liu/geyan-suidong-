// 创建一个新的 div 元素，并设置其 ID 和内部 HTML  
var toggleDiv = document.createElement('div');
toggleDiv.id = 'sanyue-toggle';
toggleDiv.innerHTML = '<span>看板娘</span>';

// 将 toggleDiv 添加到 body 的末尾  
document.body.appendChild(toggleDiv);

// 创建另一个新的 div 元素，并设置其 ID  
var sanyueDiv = document.createElement('div');
sanyueDiv.id = 'sanyue';

// 在 sanyueDiv 内部创建一个新的 div 元素，并设置其 ID 和类名（这里类名为空字符串）  
var tipsDiv = document.createElement('div');
tipsDiv.id = 'sanyue-tips';
// 将 tipsDiv 添加到 sanyueDiv 内部  
sanyueDiv.appendChild(tipsDiv);

// 创建一个新的 canvas 元素，并设置其 ID、类名、宽度和高度  
var canvas = document.createElement('canvas');
canvas.id = 'live2d';
canvas.className = 'Canvasleft';
canvas.width = 450;  // 画布实际像素宽度
canvas.height = 630; // 画布实际像素高度
canvas.style.width = '300px';   // 显示宽度
canvas.style.height = '350px';  // 显示高度

// 将 canvas 添加到 sanyueDiv 内部  
sanyueDiv.appendChild(canvas);

// 最后，将 sanyueDiv 添加到 body 的末尾  
document.body.appendChild(sanyueDiv);
