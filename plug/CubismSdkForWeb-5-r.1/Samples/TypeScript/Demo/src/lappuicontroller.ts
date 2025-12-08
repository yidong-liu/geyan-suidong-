/**
 * 用户界面控制器
 */
/**
 * 我需要一个类，实现图标对象的生成，这个图标对象是一个htmldocument元素
 */
abstract class Icon {
    abstract createsvgElement(name: string): HTMLDivElement;
    abstract hideIcon(useElement: HTMLDivElement): void;
}

class StaticIcon extends Icon {
    public createsvgElement(name: string): HTMLDivElement {
        const iconContainer = document.createElement('div');
        iconContainer.style.position = 'fixed';
        iconContainer.style.display = 'block';
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");
        svg.classList.add("icon")
        svg.setAttribute("viewBox", "0 0 24 24");
        const useElement = document.createElementNS(svgNS, "use");
        useElement.setAttribute("href", `#${name}`); // 使用模板字符串
        svg.appendChild(useElement);
        iconContainer.appendChild(svg);
        document.body.appendChild(iconContainer);
        return iconContainer;
    }
    public hideIcon(useElement: HTMLDivElement): void {
        useElement.style.display = 'none';
    }
}
class DynamicIcon extends Icon {
    public createsvgElement(name: string): HTMLDivElement {
        const iconContainer = document.createElement('div');
        iconContainer.style.position = 'absolute';
        iconContainer.style.display = 'none';
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");
        svg.classList.add("icon")
        svg.setAttribute("viewBox", "0 0 24 24");
        const useElement = document.createElementNS(svgNS, "use");
        useElement.setAttribute("href", `#${name}`); // 使用模板字符串
        svg.appendChild(useElement);
        iconContainer.appendChild(svg);
        document.body.appendChild(iconContainer);
        return iconContainer;
    }
    public changeIcon(useElement: HTMLDivElement,name: String): void {
        useElement.setAttribute("href", `#${name}`);
    }
    public hideIcon(useElement: HTMLDivElement): void {
        useElement.style.display = 'none';
    }
}

export class UIcontroller {
    constructor() {
        this.initializeUI()
    }
    public initializeUI(): void {
        const icon =this.createsettleicon("icon-siyecao")
        icon.classList.add("icon-settle")
    }
    public createsettleicon(name:String): HTMLDivElement {
        const svg = new StaticIcon();
        const iconcontainer= svg.createsvgElement(`${name}`);
        return iconcontainer;
    }

    public createplayicon(name:String): HTMLDivElement {
        const svg = new DynamicIcon();
        const iconcontainer= svg.createsvgElement(`${name}`);
        return iconcontainer;
    }
    public seticon(icon: HTMLElement, name: string): void {
        const svg = icon.firstChild as SVGSVGElement; 
        const useElement = svg.firstChild as SVGUseElement;
        if (useElement) {
            useElement.setAttribute('href', `#${name}`);
        }
    }
    public rotateicon(icon: HTMLElement,isrotate:boolean):void{
        const svg = icon.firstChild as SVGSVGElement;
        const useElement = svg.firstChild as SVGUseElement;
        if(isrotate){
            useElement.classList.add('rotate')
        }else{
            useElement.classList.remove('rotate')
        }
    }
}

