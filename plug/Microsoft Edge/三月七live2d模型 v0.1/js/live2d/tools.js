
function showHitokoto() {
    // 增加 hitokoto.cn 的 API
    fetch("https://v1.hitokoto.cn")
        .then(response => response.json())
        .then(result => {
            const text = `这句一言来自 <span>「${result.from}」</span>，是 <span>${result.creator}</span> 在 hitokoto.cn 投稿的。`;
            showMessage(result.hitokoto, 6000, 9);
            setTimeout(() => {
                showMessage(text, 4000, 9);
            }, 6000);
        });
}

const tools = {
    "hitokoto": {
        icon: "fas fa-comment",
        callback: showHitokoto
    },
    "asteroids": {
        icon: "fas fa_paper_plane",
        callback: () => {
            if (window.Asteroids) {
                if (!window.ASTEROIDSPLAYERS) window.ASTEROIDSPLAYERS = [];
                window.ASTEROIDSPLAYERS.push(new Asteroids());
            } else {
                const script = document.createElement("script");
                script.src = "https://fastly.jsdelivr.net/gh/stevenjoezhang/asteroids/asteroids.js";
                document.head.appendChild(script);
            }
        }
    },
    "switch-model": {
        icon: "fas fa_user_circle",
        callback: () => {}
    },
    "switch-texture": {
        icon: "fas fa_street_view",
        callback: () => {}
    },
    "photo": {
        icon: "fas fa_camera_retro",
        callback: () => {
            showMessage("照好了嘛，是不是很可爱呢？", 6000, 9);
            Live2D.captureName = "photo.png";
            Live2D.captureFrame = true;
        }
    },
    "info": {
        icon: "fas fa_info_circle",
        callback: () => {
            open("https://github.com/stevenjoezhang/live2d-widget");
        }
    },
    "quit": {
        icon: "fas fa_xmark",
        callback: () => {
            localStorage.setItem("sanyue-display", Date.now());
            showMessage("愿你有一天能与重要的人重逢。", 2000, 11);
            document.getElementById("sanyue").style.bottom = "-500px";
            setTimeout(() => {
                document.getElementById("sanyue").style.display = "none";
                document.getElementById("sanyue-toggle").classList.add("sanyue-toggle-active");
            }, 3000);
        }
    }
};

