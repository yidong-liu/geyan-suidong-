
import { LAppLive2DManager } from "./lapplive2dmanager";
export class ExpressionManager
{
    private _listExpressions: string[];
    constructor()
    {
        this._listExpressions = [];
        this.getlist();
    }
    public getlist()
    {
        // const fileUrl = chrome.runtime.getURL("js/model/march_7/march_7.model3.json");
        const fileUrl = "./model/march_7/march_7.model3.json"
        fetch(fileUrl)
            .then(response =>
            {
                // 检查响应是否成功
                if (!response.ok)
                {
                    throw new Error('Network response was not ok');
                }
                // 返回JSON对象
                return response.json();
            })
            .then(data =>
            {
                data.FileReferences.Expressions.forEach((element: any) =>
                {
                    this._listExpressions.push(element.Name);
                });
            })
            .catch(error =>
            {
                // 处理错误
                console.error('There was a problem with the fetch operation:', error);
            });
    }
    public setExpression(expression: string): void
    {
        const model = LAppLive2DManager.getInstance().getModel(0);
        if (model)
        {
            model.setExpression(expression);
        }
    }
    public setrandomExpression(): void
    {
        const model = LAppLive2DManager.getInstance().getModel(0);
        if (model)
        {
            const randomIndex = Math.floor(Math.random() * this._listExpressions.length);
            const randomExpression = this._listExpressions[randomIndex];
            model.setExpression(randomExpression);
        }
    }
    public getlistExpressions(): string[]
    {
        return this._listExpressions;
    }
    public stopExpression()
    {
        const model = LAppLive2DManager.getInstance().getModel(0);
        if (model)
        {
            model.stopExpression();
        }
    }
}   
