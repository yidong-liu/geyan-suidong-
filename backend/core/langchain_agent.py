"""
LangChain表情生成代理模块
基于AI (Google Gemini / OpenAI) 生成Live2D表情参数
"""
from typing import Dict, List, Any, Optional
import json
import logging
import os
from dotenv import load_dotenv

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
logger = logging.getLogger(__name__)


class Live2DExpression(BaseModel):
    """Live2D表情参数模型"""
    eye_open: float = Field(
        description="左眼睁开程度 (0-1)",
        ge=0.0,
        le=1.0
    )
    eye_open_r: float = Field(
        description="右眼睁开程度 (0-1)",
        ge=0.0,
        le=1.0
    )
    eyebrow_height: float = Field(
        description="左眉毛高度 (0-1)",
        ge=0.0,
        le=1.0
    )
    eyebrow_height_r: float = Field(
        description="右眉毛高度 (0-1)",
        ge=0.0,
        le=1.0
    )
    mouth_open: float = Field(
        description="嘴巴张开程度 (0-1)",
        ge=0.0,
        le=1.0
    )
    mouth_form: float = Field(
        description="嘴型 (0=悲伤, 0.5=中性, 1=微笑)",
        ge=0.0,
        le=1.0
    )
    cheek: float = Field(
        description="脸红程度 (0-1)",
        ge=0.0,
        le=1.0
    )
    body_angle_x: float = Field(
        description="身体X轴角度 (-1 to 1)",
        ge=-1.0,
        le=1.0
    )
    body_angle_y: float = Field(
        description="身体Y轴角度 (-1 to 1)",
        ge=-1.0,
        le=1.0
    )
    breath: float = Field(
        description="呼吸强度 (0-1)",
        ge=0.0,
        le=1.0
    )


class ExpressionAgentV2:
    """基于LangChain的表情生成代理"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        use_copilot: bool = False,
        use_gemini: bool = True
    ):
        """
        初始化表情代理

        Args:
            api_key: API密钥 (如未提供则从环境变量读取)
            api_base: API基础URL (可选，仅OpenAI使用)
            model_name: 使用的模型名称
            temperature: 创造性参数 (0-2)
            max_tokens: 最大输出token数
            use_copilot: 是否使用 GitHub Copilot API (已废弃)
            use_gemini: 是否使用 Google Gemini API (默认: True)
        """
        # 获取 API 配置
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            # Google Gemini配置
            self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
            self.model_name = model_name or os.getenv('GOOGLE_MODEL', 'gemini-1.5-flash')
            self.api_base = None
        else:
            # OpenAI兼容API配置
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.model_name = model_name or os.getenv('OPENAI_MODEL', 'gpt-4o-mini') 
            self.api_base = api_base or os.getenv('OPENAI_API_BASE', 'https://apiproxy.top/')
            
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.use_copilot = use_copilot  

        # 验证API密钥
        if not self.api_key:
            error_msg = (
                "未找到 API 密钥。"
                "请设置环境变量: "
                "GOOGLE_API_KEY (使用Gemini) 或 OPENAI_API_KEY (使用OpenAI)"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(
            f"初始化表情生成代理 - "
            f"引擎: {'Gemini' if self.use_gemini else 'OpenAI'}, "
            f"模型: {self.model_name}"
        )
        
        # 初始化 LLM
        try:
            self._initialize_llm()
        except Exception as e:
            logger.error(f"LLM 初始化失败: {str(e)}", exc_info=True)
            raise ValueError(f"LLM 初始化失败: {str(e)}")

        # Live2D参数映射
        self.live2d_params = {
            'eye_open': 'ParamEyeLOpen',
            'eye_open_r': 'ParamEyeROpen',
            'eyebrow_height': 'ParamEyeBrowLY',
            'eyebrow_height_r': 'ParamEyeBrowRY',
            'mouth_open': 'ParamMouthOpenY',
            'mouth_form': 'ParamMouthForm',
            'cheek': 'ParamCheek',
            'body_angle_x': 'ParamBodyAngleX',
            'body_angle_y': 'ParamBodyAngleY',
            'breath': 'ParamBreath'
        }

        # 初始化 Prompt 和 Parser
        self._setup_chain()

    def _initialize_llm(self):
        """初始化LLM实例"""
        if self.use_gemini:
            # 使用 Google Gemini
            llm_kwargs = {
                "model": self.model_name,
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
                "google_api_key": self.api_key,
            }
            self.llm = ChatGoogleGenerativeAI(**llm_kwargs)
            logger.info(f"Google Gemini LLM 初始化成功: {self.model_name}")
        else:
            # 使用 OpenAI 兼容 API
            llm_kwargs = {
                "model": self.model_name,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "api_key": self.api_key,
            }
            
            if self.api_base:
                llm_kwargs["base_url"] = self.api_base
            
            self.llm = ChatOpenAI(**llm_kwargs)
            logger.info(f"OpenAI LLM 初始化成功: {self.model_name}, base_url: {self.api_base}")

    def _setup_chain(self):
        """设置 LangChain 链"""
        # 系统提示词
        system_template = """你是一个专业的Live2D表情参数生成专家。
你需要根据音乐的特征（节奏、能量、音高、情感等）生成对应的Live2D角色表情参数。

Live2D参数说明：
- eye_open, eye_open_r: 眼睛睁开程度，0=闭眼，1=完全睁开
- eyebrow_height, eyebrow_height_r: 眉毛高度，0=低垂，0.5=正常，1=扬起
- mouth_open: 嘴巴张开程度，0=闭合，1=大张
- mouth_form: 嘴型，0=向下(悲伤)，0.5=中性，1=上扬(微笑)
- cheek: 脸红程度，0=无，1=最红
- body_angle_x: 身体左右倾斜，-1=左倾，0=居中，1=右倾
- body_angle_y: 身体前后倾斜，-1=后仰，0=居中，1=前倾
- breath: 呼吸强度，0=平缓，1=急促

音乐特征解释：
- tempo: 节拍速度(BPM)，影响动作频率
- energy: 能量强度(0-1)，高能量需要更夸张的表情
- pitch: 音高(Hz)，高音可能表现激动，低音可能表现沉稳
- spectral_centroid: 频谱质心(0-1)，反映音色明亮度
- emotion_scores: 情感分数，包含 happy, sad, energetic, calm 等

生成规则：
1. 高能量音乐 -> 眼睛睁大、嘴巴张开、身体摆动
2. 快节奏 -> 增加眨眼频率、身体律动
3. 欢快情感 -> 微笑、脸红、眉毛上扬
4. 悲伤情感 -> 眉毛下垂、嘴角下垂、眼睛半闭
5. 平静情感 -> 参数接近中性值

请返回严格的JSON格式，所有参数值必须在指定范围内。"""

        human_template = """基于以下音乐特征，生成Live2D表情参数：

时间戳: {timestamp} 秒
节拍(BPM): {tempo}
能量强度: {energy}
频谱质心: {spectral_centroid}
音高: {pitch} Hz
情感分数: {emotion_scores}

请生成合适的Live2D表情参数（JSON格式）："""

        # 创建 Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])

        # 输出解析器
        self.parser = JsonOutputParser(pydantic_object=Live2DExpression)

    def generate_expression(
        self,
        timestamp: float,
        tempo: float,
        energy: float,
        spectral_centroid: float,
        pitch: float,
        emotion_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        基于音乐特征生成表情参数 - 完全AI驱动

        Args:
            timestamp: 时间戳（秒）
            tempo: 节拍（BPM）
            energy: 能量级别（0-1）
            spectral_centroid: 频谱质心（0-1）
            pitch: 音高（Hz）
            emotion_scores: 情感分数字典

        Returns:
            Dict: Live2D表情参数
        """
        logger.info(f"生成表情参数: 时间点={timestamp}s, BPM={tempo}, 能量={energy:.2f}")

        try:
            # 准备输入
            input_data = {
                "timestamp": timestamp,
                "tempo": tempo,
                "energy": energy,
                "spectral_centroid": spectral_centroid,
                "pitch": pitch,
                "emotion_scores": json.dumps(emotion_scores, ensure_ascii=False)
            }

            logger.debug(f"调用 LLM - 输入数据: {input_data}")

            # 构建链
            chain = self.prompt | self.llm | self.parser

            # 执行生成
            try:
                result = chain.invoke(input_data)
                logger.debug(f"LLM 返回结果: {result}")
            except Exception as llm_error:
                logger.error(f"LLM API 调用失败: {str(llm_error)}", exc_info=True)
                raise RuntimeError(f"AI API 调用失败: {str(llm_error)}")
            
            # 验证结果
            expression_params = self._validate_params(result)
            
            logger.info(f"AI生成成功: {expression_params}")
            return expression_params

        except RuntimeError:
            raise
        except Exception as e:
            logger.error(f"AI生成失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"表情生成失败: {str(e)}")

    def _validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """验证并修正参数范围"""
        validated = {}
        
        # 定义参数范围
        param_ranges = {
            'eye_open': (0.0, 1.0),
            'eye_open_r': (0.0, 1.0),
            'eyebrow_height': (0.0, 1.0),
            'eyebrow_height_r': (0.0, 1.0),
            'mouth_open': (0.0, 1.0),
            'mouth_form': (0.0, 1.0),
            'cheek': (0.0, 1.0),
            'body_angle_x': (-1.0, 1.0),
            'body_angle_y': (-1.0, 1.0),
            'breath': (0.0, 1.0)
        }
        
        for key, (min_val, max_val) in param_ranges.items():
            value = params.get(key, 0.5)
            # 确保值在范围内
            validated[key] = max(min_val, min(max_val, float(value)))
        
        return validated

    def batch_generate_expressions(
        self,
        feature_timeline: List[Dict[str, Any]],
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        批量生成表情参数

        Args:
            feature_timeline: 特征时间线列表
            use_cache: 是否使用缓存（相似特征复用结果）

        Returns:
            List[Dict]: 表情参数列表
        """
        expressions = []
        cache = {} if use_cache else None

        for i, features in enumerate(feature_timeline):
            # 生成缓存键
            if use_cache:
                cache_key = self._generate_cache_key(features)
                if cache_key in cache:
                    logger.debug(f"使用缓存结果: 帧 {i}")
                    expressions.append({
                        'timestamp': features.get('timestamp', 0),
                        'parameters': cache[cache_key].copy()
                    })
                    continue

            # 生成表情
            expression = self.generate_expression(
                timestamp=features.get('timestamp', 0),
                tempo=features.get('tempo', 100),
                energy=features.get('energy', 0.5),
                spectral_centroid=features.get('spectral_centroid', 0.5),
                pitch=features.get('pitch', 0),
                emotion_scores=features.get('emotion_scores', {})
            )

            result = {
                'timestamp': features.get('timestamp', 0),
                'parameters': expression
            }
            expressions.append(result)

            # 存入缓存
            if use_cache:
                cache[cache_key] = expression.copy()

        logger.info(f"批量生成完成: {len(expressions)} 个关键帧")
        return expressions

    def _generate_cache_key(self, features: Dict[str, Any]) -> str:
        """生成缓存键（量化特征）"""
        # 量化特征以便相似的特征可以复用
        energy_bucket = int(features.get('energy', 0.5) * 10)
        tempo_bucket = int(features.get('tempo', 100) / 20)
        
        emotion_scores = features.get('emotion_scores', {})
        happy = int(emotion_scores.get('happy', 0) * 10)
        sad = int(emotion_scores.get('sad', 0) * 10)
        
        return f"{energy_bucket}_{tempo_bucket}_{happy}_{sad}"
