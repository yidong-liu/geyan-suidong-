

let messageTimer;

function showMessage(text, timeout, priority) {
    if (!text || (sessionStorage.getItem("sanyue-text") && sessionStorage.getItem("sanyue-text") > priority)) return;
    if (messageTimer) {
        clearTimeout(messageTimer);
        messageTimer = null;
    }
    text = randomSelection(text);
    sessionStorage.setItem("sanyue-text", priority);
    const tips = document.getElementById("sanyue-tips");
    tips.innerHTML = text;
    tips.classList.add("sanyue-tips-active");
    messageTimer = setTimeout(() => {
        sessionStorage.removeItem("sanyue-text");
        tips.classList.remove("sanyue-tips-active");
    }, timeout);
}

