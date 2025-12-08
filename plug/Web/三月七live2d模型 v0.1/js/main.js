const sanyue_path= "./js/sanyue-tips.json"
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

initWidget();
