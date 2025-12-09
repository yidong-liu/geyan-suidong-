import { UIcontroller } from "./lappuicontroller";
import { RequestHandler } from "./lapprequesthandler";
import { ExpressionManager } from "./lappexpressionsmanager";
import axios, { AxiosResponse } from "axios";
export class SelectionMonitor {
  private showicon: boolean = false;
  private iconElement: HTMLElement | null = null;
  private iconLeft: number = 0;
  private iconTop: number = 0;
  private _UIcontroller = new UIcontroller();
  private _requestHandler = new RequestHandler();
  private _expressionManager = new ExpressionManager();
  private _text = "";
  private _isrotate: boolean = false;
  constructor() {
    this.init();
  }

  private init(): void {
    this.getplaysvg();
    this.addMouseUpListener();
    document.addEventListener("keydown", this.handleKeyDownForExpression);
  }

  private getplaysvg(): void {
    const iconContainer = this._UIcontroller.createplayicon("icon-bofang");
    this.iconElement = iconContainer;
  }

  private addMouseUpListener(): void {
    document.addEventListener("mouseup", this.handleMouseUp.bind(this));
  }

  private handleMouseUp(): void {
    const selection = window.getSelection();
    if (selection.rangeCount > 0 && selection.toString().trim() !== "") {
      this._text = selection.toString();
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      document.addEventListener("keydown", this.handleKeyDown);
      this.updateIconPosition(rect);
      this.showIcon();
    }
  }

  private showIcon(): void {
    this.showicon = true;
    this.iconElement.style.display = "block"; // 显示图标
    this.setupIconClickListener();
  }

  private hideIcon(): void {
    this.showicon = false;
    this.iconElement.style.display = "none"; // 隐藏图标
    this.iconElement.removeEventListener("click", this.handleIconClick); // 移除点击事件监听器
  }

  private setupIconClickListener(): void {
    // 确保不会重复添加事件监听器
    this.iconElement.removeEventListener("click", this.handleIconClick);
    this.iconElement.addEventListener("click", this.handleIconClick);
  }
  private handleKeyDown = async (event: KeyboardEvent) => {
    if (event.ctrlKey && event.key === "q") {
      try {
        const response = await this._requestHandler.sendRequest(this._text);
        const blob = response.data;
        const url = URL.createObjectURL(blob);
        const audioElement = new Audio(url);
        audioElement.play().catch((error) => {
          console.error("Error playing audio:", error);
        });
        audioElement.addEventListener("ended", () => {
          URL.revokeObjectURL(url);
        });
      } catch (error) {
        console.error("Error fetching or processing audio:", error);
      }
    }
  };

  private handleIconClick = async (): Promise<void> => {
    this._UIcontroller.seticon(this.iconElement, "icon-jiazai");
    this._isrotate = true;
    this._UIcontroller.rotateicon(this.iconElement, this._isrotate);
    try {
      const response = await this._requestHandler.sendRequest(this._text);
      const blob = response.data;
      const url = URL.createObjectURL(blob);
      const audioElement = new Audio(url);
      this._isrotate = false;
      this._UIcontroller.rotateicon(this.iconElement, this._isrotate);
      this._UIcontroller.seticon(this.iconElement, "icon-bofang");
      audioElement.play().catch((error) => {
        console.error("Error playing audio:", error);
      });

      // 监听音频结束事件以释放 Blob URL（可选，但推荐）
      audioElement.addEventListener("ended", () => {
        URL.revokeObjectURL(url);
      });
      // 如果还有其他逻辑需要处理 response.data，可以在这里添加
      // 例如：this._requestHandler.playText(someOtherAudioUrl); // 注意这里应该使用正确的音频 URL
    } catch (error) {
      console.error("Error fetching or processing audio:", error);
    }
  };

  private updateIconPosition(rect: DOMRect): void {
    // this.iconLeft = rect.x + window.scrollX -20; // 根据需要调整偏移量
    // this.iconTop = rect.y + window.scrollY + 25; // 根据需要调整偏移量
    this.iconLeft = rect.x + rect.width + window.scrollX - 20; // 根据需要调整偏移量
    this.iconTop = rect.top + rect.height + window.scrollY + 25; // 根据需要调整偏移量
    if (this.iconElement) {
      this.iconElement.style.left = `${this.iconLeft}px`;
      this.iconElement.style.top = `${this.iconTop}px`;
    }
  }
  // 监听键盘事件，触发表情变化
  private handleKeyDownForExpression = (event: KeyboardEvent) => {
    let expressionlist = this._expressionManager.getlistExpressions();
    expressionlist.forEach((expression, index) => {
      if (event.ctrlKey && event.key === (index + 1).toString()) {
        this._expressionManager.setExpression(expression);
      }
    });
    if (event.ctrlKey  && event.shiftKey && event.key === "w") {
      // 获取一个表情数组 localhost: 8000
      axios
        .post("http://localhost:8000/api/v1/getNeutralExpression", {})
        .then((response: AxiosResponse) => {
          const neutralExpression = response.data.neutralExpression;
          this._expressionManager.setExpressions(neutralExpression);
        })
        .catch((error) => {
          console.error("Error fetching neutral expression:", error);
        });
    }
  };
}
