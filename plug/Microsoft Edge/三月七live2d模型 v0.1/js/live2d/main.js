const sanyue_path= "https://blog.sanyue.website/live2d/js/sanyue-tips.json"
function loadWidget() {
    localStorage.removeItem("sanyue-display");
    sessionStorage.removeItem("sanyue-text");
    setTimeout(() => {
        document.getElementById("sanyue").style.bottom = 0;
    }, 0);
    function welcomeMessage(time) {
    if (location.pathname === "/") { // 如果是主页
        for (let { hour, text } of time) {
            const now = new Date(),
                after = hour.split("-")[0],
                before = hour.split("-")[1] || after;
            if (after <= now.getHours() && now.getHours() <= before) {
                return text;
            }
        }
    }
    const text = `欢迎阅读<span>「${document.title.split(" - ")[0]}」</span>`;
    let from;
    if (document.referrer !== "") {
        const referrer = new URL(document.referrer),
            domain = referrer.hostname.split(".")[1];
        const domains = {
            "baidu": "百度",
            "so": "360搜索",
            "google": "谷歌搜索"
        };
        if (location.hostname === referrer.hostname) return text;

        if (domain in domains) from = domains[domain];
        else from = referrer.hostname;
        return `Hello！来自 <span>${from}</span> 的朋友<br>${text}`;
    }
    return text;
}


function registerEventListener(result) {
    // 检测用户活动状态，并在空闲时显示消息
    let userAction = false,
        userActionTimer,
        messageArray = result.message.default,
        lastHoverElement;
    window.addEventListener("mousemove", () => userAction = true);
    window.addEventListener("keydown", () => userAction = true);
    setInterval(() => {
        if (userAction) {
            userAction = false;
            clearInterval(userActionTimer);
            userActionTimer = null;
        } else if (!userActionTimer) {
            userActionTimer = setInterval(() => {
                showMessage(messageArray, 6000, 9);
            }, 20000);
        }
    }, 1000);
    showMessage(welcomeMessage(result.time), 7000, 11);
    window.addEventListener("mouseover", event => {
        for (let { selector, text } of result.mouseover) {
            if (!event.target.closest(selector)) continue;
            if (lastHoverElement === selector) return;
            lastHoverElement = selector;
            text = randomSelection(text);
            text = text.replace("{text}", event.target.innerText);
            showMessage(text, 4000, 8);
            return;
        }
    });
    window.addEventListener("click", event => {
        for (let { selector, text } of result.click) {
            if (!event.target.closest(selector)) continue;
            text = randomSelection(text);
            text = text.replace("{text}", event.target.innerText);
            showMessage(text, 4000, 8);
            return;
        }
    });
    result.seasons.forEach(({ date, text }) => {
        const now = new Date(),
            after = date.split("-")[0],
            before = date.split("-")[1] || after;
        if ((after.split("/")[0] <= now.getMonth() + 1 && now.getMonth() + 1 <= before.split("/")[0]) && (after.split("/")[1] <= now.getDate() && now.getDate() <= before.split("/")[1])) {
            text = randomSelection(text);
            text = text.replace("{year}", now.getFullYear());
            messageArray.push(text);
        }
    });

    const devtools = () => { };
    console.log("%c", devtools);
    devtools.toString = () => {
        showMessage(result.message.console, 6000, 9);
    };
    window.addEventListener("copy", () => {
        showMessage(result.message.copy, 6000, 9);
    });
    window.addEventListener("visibilitychange", () => {
        if (!document.hidden) showMessage(result.message.visibilitychange, 6000, 9);
    });
}
(function initModel() {    
    fetch(sanyue_path)
        .then(response => {    
            if (!response.ok) {
                throw new Error('Network response was not ok');    
            }    
            return response.json();    
        })    
        .then(result => {    
            console.log(result);
            registerEventListener(result);    
            // 如果需要显示欢迎消息，可以在这里调用  
            showMessage(welcomeMessage(result.time), 7000, 11);    
        })    
        .catch(error => {    
            console.error('There was a problem with your fetch operation:', error);    
        });    
})();
}



function initWidget() {
    const toggle = document.getElementById("sanyue-toggle");
    toggle.addEventListener("click", () => {
        toggle.classList.remove("sanyue-toggle-active");
        if (toggle.getAttribute("first-time")) {
            loadWidget(config);
            toggle.removeAttribute("first-time");
        } else {
            localStorage.removeItem("sanyue-display");
            document.getElementById("sanyue").style.display = "";
            setTimeout(() => {
                document.getElementById("sanyue").style.bottom = 0;
            }, 0);
        }
    });
    if (localStorage.getItem("sanyue-display") && Date.now() - localStorage.getItem("sanyue-display") <= 86400000) {
        toggle.setAttribute("first-time", true);
        setTimeout(() => {
            toggle.classList.add("sanyue-toggle-active");
        }, 0);
    } else {
        loadWidget();
    }
}
// 发送消息到背景脚本请求资源URL  

initWidget();
var v;
$(document).ready(() => {
        v = new Viewer("model");
});

class Viewer {
    constructor (basePath) {
        this.l2d = new L2D(basePath);

        this.canvas = $(".Canvas")
        this.app = new PIXI.Application(1280, 720,{transparent: true,});
        let width = window.innerWidth;        
        let height = (width / 16.0) * 9.0;
        // let width = 280
        // let height = 250
        this.app.view.style.width = width + "px";
        this.app.view.style.height = height + "px";
        this.app.renderer.resize(width, height);
        this.canvas.html(this.app.view);
        let name ="march_7"
        this.l2d.load(name, this);
        this.app.ticker.add((deltaTime) => {
            if (!this.model) {
                return;
            }
            this.model.update(deltaTime);
            this.model.masks.update(this.app.renderer);
        });
        window.onresize = (event) => {
            if (event === void 0) { event = null; }
            // let width = window.innerWidth;
            // let height = (width / 16.0) * 9.0;
            let width = 280
            let height = 250
            this.app.view.style.width = width + "px";
            this.app.view.style.height = height + "px";
            this.app.renderer.resize(width, height);

            if (this.model) {
                this.model.position = new PIXI.Point((width * 0.5), (height * 0.5));
                this.model.scale = new PIXI.Point((this.model.position.x * 0.06), (this.model.position.x * 0.06));
                // this.model.scale = new PIXI.Point((this.model.position.x), (this.model.position.x));
                this.model.masks.resize(this.app.view.width, this.app.view.height);
                
            }
            if(this.model.height <= 200) {
                this.model.scale = new PIXI.Point((this.model.position.x * 1.8), (this.model.position.x * 1.8));
            }
        };
        let viewWidth = window.innerWidth;
        let viewHeight = window.innerHeight;
        window.addEventListener('mousedown', (event) => {
        });
        window.addEventListener('mousemove', (event) => {

            if (this.model) {
                    this.model.inDrag = true;
                }
            
            // 使用 jQuery 选择器获取元素
            const $element = $(".Canvas");
            const element = $element[0];
            const { centerX, centerY } = getElementCenter(element);
            if (this.model) {
                
                let mouseOffsetX = event.clientX - centerX
                let mouseOffsetY = event.clientY - centerY
                // let mouse_x = this.model.position.x - event.clientX;
                // let mouse_y = this.model.position.y - event.clientY;
                this.model.pointerX = mouseOffsetX / width;
                this.model.pointerY = mouseOffsetY / height;
            }
        });
        window.addEventListener('mouseup', (event) => {
            if (!this.model) {
                return;
            }

            if (this.isClick) {
            }

            // this.isClick = false;
            this.model.inDrag = false;
        });

    }

    

    changeCanvas (model) {
        this.app.stage.removeChildren();
        model.motions.forEach((value, key) => {
            if (key != "effect") {
                let btn = document.createElement("button");
                let label = document.createTextNode(key);
                btn.appendChild(label);
                btn.className = "btn btn-secondary";
                btn.addEventListener("click", () => {
                    this.startAnimation(key, "base");
                });
                this.selectAnimation.append(btn);
            }
        });

        this.model = model;
        this.model.update = this.onUpdate; // HACK: use hacked update fn for drag support
        this.model.animator.addLayer("base", LIVE2DCUBISMFRAMEWORK.BuiltinAnimationBlenders.OVERRIDE, 1);

        this.app.stage.addChild(this.model);
        this.app.stage.addChild(this.model.masks);

        window.onresize();
    }

    onUpdate (delta) {
        let deltaTime = 0.016 * delta;
        if (!this.animator.isPlaying) {
            let m = this.motions.get("idle");
            this.animator.getLayer("base").play(m);
        }
        this._animator.updateAndEvaluate(deltaTime);

        if (this.inDrag) {
            this.addParameterValueById("ParamAngleX", this.pointerX * 30);
            this.addParameterValueById("ParamAngleY", -this.pointerY * 30);
            this.addParameterValueById("ParamBodyAngleX", this.pointerX * 10);
            this.addParameterValueById("ParamBodyAngleY", -this.pointerY * 10);
            this.addParameterValueById("ParamEyeBallX", this.pointerX);
            this.addParameterValueById("ParamEyeBallY", -this.pointerY);
        }

        if (this._physicsRig) {
            this._physicsRig.updateAndEvaluate(deltaTime);
        }

        this._coreModel.update();

        let sort = false;
        for (let m = 0; m < this._meshes.length; ++m) {
            this._meshes[m].alpha = this._coreModel.drawables.opacities[m];
            this._meshes[m].visible = Live2DCubismCore.Utils.hasIsVisibleBit(this._coreModel.drawables.dynamicFlags[m]);
            if (Live2DCubismCore.Utils.hasVertexPositionsDidChangeBit(this._coreModel.drawables.dynamicFlags[m])) {
                this._meshes[m].vertices = this._coreModel.drawables.vertexPositions[m];
                this._meshes[m].dirtyVertex = true;
            }
            if (Live2DCubismCore.Utils.hasRenderOrderDidChangeBit(this._coreModel.drawables.dynamicFlags[m])) {
                sort = true;
            }
        }

        if (sort) {
            this.children.sort((a, b) => {
                let aIndex = this._meshes.indexOf(a);
                let bIndex = this._meshes.indexOf(b);
                let aRenderOrder = this._coreModel.drawables.renderOrders[aIndex];
                let bRenderOrder = this._coreModel.drawables.renderOrders[bIndex];

                return aRenderOrder - bRenderOrder;
            });
        }

        this._coreModel.drawables.resetDynamicFlags();
    }

    startAnimation (motionId, layerId) {
        if (!this.model) {
            return;
        }

        let m = this.model.motions.get(motionId);
        if (!m) {
            return;
        }

        let l = this.model.animator.getLayer(layerId);
        if (!l) {
            return;
        }

        l.play(m);
    }

    isHit (id, posX, posY) {
        if (!this.model) {
            return false;
        }

        let m = this.model.getModelMeshById(id);
        if (!m) {
            return false;
        }

        const vertexOffset = 0;
        const vertexStep = 2;
        const vertices = m.vertices;

        let left = vertices[0];
        let right = vertices[0];
        let top = vertices[1];
        let bottom = vertices[1];

        for (let i = 1; i < 4; ++i) {
            let x = vertices[vertexOffset + i * vertexStep];
            let y = vertices[vertexOffset + i * vertexStep + 1];

            if (x < left) {
                left = x;
            }
            if (x > right) {
                right = x;
            }
            if (y < top) {
                top = y;
            }
            if (y > bottom) {
                bottom = y;
            }
        }

        let mouse_x = m.worldTransform.tx - posX;
        let mouse_y = m.worldTransform.ty - posY;
        let tx = -mouse_x / m.worldTransform.a;
        let ty = -mouse_y / m.worldTransform.d;

        return ((left <= tx) && (tx <= right) && (top <= ty) && (ty <= bottom));
    }
}
function getElementCenter(element) {  
    const rect = element.getBoundingClientRect();  
    const centerX = rect.left + rect.width / 2;  
    const centerY = rect.top + rect.height / 2;  
    return { centerX, centerY };  
}  
  

document.addEventListener('DOMContentLoaded', function() {  
    const canvasElement = document.querySelector('.Canvas'); // 确保类名大小写正确  
    if (!canvasElement) {  
        console.error('没有找到具有 .Canvas 类的元素');  
        return;  
    }  
  
    // 初始设置元素位置（如果需要的话）  
    // canvasElement.style.position = 'absolute';  
    // canvasElement.style.left = '0px'; // 或根据需要设置  
    // canvasElement.style.bottom = '1020px'; // 或根据需要设置  
  
    let active = false;  
    let currentX;  
    let currentY;  
    let initialX = canvasElement.offsetLeft;  
    let initialY = canvasElement.offsetTop;  
    let xOffset = 0;  
    let yOffset = 0;  
  
    canvasElement.addEventListener('mousedown', dragStart, false);  
    document.addEventListener('mouseup', dragEnd, false);  
    document.addEventListener('mousemove', drag, false);  
  
    function dragStart(e) {  
        if (e.target === canvasElement) {  
            active = true;  
            currentX = e.clientX - canvasElement.offsetLeft;  
            currentY = e.clientY - canvasElement.offsetTop;  
  
            if (e.preventDefault) {  
                e.preventDefault(); // 阻止默认处理（防止选择文本）  
            }  
  
            canvasElement.style.cursor = 'move';  
        }  
    }  
  
    function dragEnd(e) {  
        active = false;  
        canvasElement.style.cursor = 'default';  
        // 不需要更新 initialX 和 initialY，它们应该在 dragStart 中设置  
    }  
  
    function drag(e) {  
        if (active) {  
            e.preventDefault();  
  
            let x = e.clientX - currentX;  
            let y = e.clientY - currentY;  
  
            // 可以添加边界检查，但这里不限制元素移出屏幕  
  
            canvasElement.style.left = `${x + initialX}px`;  
            canvasElement.style.top = `${y + initialY}px`;  
  
            // 不需要更新 xOffset 和 yOffset，因为 currentX 和 currentY 会在下次 mousedown 时重新计算  
        }  
    }  
});


