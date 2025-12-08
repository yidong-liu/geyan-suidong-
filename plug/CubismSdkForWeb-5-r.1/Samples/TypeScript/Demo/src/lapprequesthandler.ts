import axios, { AxiosResponse } from 'axios';

// 定义请求数据的接口
interface RequestData
{
    text: string;
    speaker_id: number;
    sdp_ratio: number;
    noise: number;
    noisew: number;
    length: number;
    auto_translate: boolean;
    auto_split: boolean;
    emotion: string;
    style_text: string;
    style_weight: number;
}

interface ResponseData
{
    audio_url: string;
}
// 使用 CloudFlare
export class RequestHandler
{
    private readonly apiUrl = 'https://sanyue.yidongliu5.workers.dev/?https://www.tts-webui.com/api/gen';
    private readonly headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Priority': 'u=1, i',
        'Content-Type': 'application/json'
    };

    public async sendRequest(text: string): Promise<AxiosResponse<Blob>>
    {
        const data: RequestData = {
            text: text,
            speaker_id: 0,
            sdp_ratio: 0.2,
            noise: 0.2,
            noisew: 0.9,
            length: 1,
            auto_translate: false,
            auto_split: true,
            emotion: 'Happy',
            style_text: '',
            style_weight: 0.7
        };

        try
        {
            const response = await axios.post<Blob>(this.apiUrl, data, { headers: this.headers, responseType: 'blob' });
            return response;
        } catch (error)
        {
            console.error('Error sending request:', error);
            throw error; // 重新抛出错误以便调用者可以处理它
        }
    }
    public recieveResponse(): void
    {

    }
    public playText(audioUrl: string): void
    {
        console.log('Playing audio at:', audioUrl);
    }
}

