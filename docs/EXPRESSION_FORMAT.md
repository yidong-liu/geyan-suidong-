# 表情文件格式说明 v1.0

本文档详细说明歌颜随动系统生成的Live2D表情文件格式。

## 📄 文件概述

### 基本信息

- **格式**: JSON
- **编码**: UTF-8
- **扩展名**: `.json`
- **存储位置**: `data/expressions/`

### 文件命名

```
{expression_id}.json
```

示例: `a1b2c3d4-e5f6-7890-abcd-ef1234567890.json`

---

## 📋 JSON结构

### 顶层结构

```json
{
  "metadata": { },
  "audio_features": { },
  "keyframes": [ ]
}
```

---

## 🔍 字段详解

### 1. metadata（元数据）

包含表情文件的基本信息。

```json
{
  "metadata": {
    "version": "1.0",
    "model_name": "default",
    "duration": 180.5,
    "keyframe_count": 1805,
    "time_resolution": 0.1,
    "smoothing_enabled": true,
    "sensitivity": 1.0,
    "created_at": "2024-12-10T03:45:00Z",
    "generator": "geyan-suidong-v1.0"
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|-------|------|------|
| version | string | 表情格式版本 |
| model_name | string | 目标Live2D模型名称 |
| duration | float | 音频总时长（秒） |
| keyframe_count | integer | 关键帧总数 |
| time_resolution | float | 时间分辨率（秒） |
| smoothing_enabled | boolean | 是否启用平滑处理 |
| sensitivity | float | 表情敏感度 |
| created_at | string | 创建时间（ISO 8601格式） |
| generator | string | 生成工具标识 |

### 2. audio_features（音频特征）

包含音频分析的核心特征数据。

```json
{
  "audio_features": {
    "tempo": 120.0,
    "beat_count": 360,
    "emotion_scores": {
      "happy": 0.65,
      "sad": 0.15,
      "energetic": 0.75,
      "calm": 0.20,
      "angry": 0.05
    },
    "energy_stats": {
      "mean": 0.68,
      "max": 0.95,
      "min": 0.12,
      "std": 0.18
    },
    "pitch_stats": {
      "mean": 440.0,
      "max": 880.0,
      "min": 220.0
    },
    "spectral_stats": {
      "mean": 2500.0,
      "max": 8000.0,
      "min": 500.0
    }
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|-------|------|------|
| tempo | float | 音乐节拍（BPM） |
| beat_count | integer | 检测到的节拍总数 |
| emotion_scores | object | 情感分数（0-1） |
| energy_stats | object | 能量统计信息 |
| pitch_stats | object | 音高统计信息（Hz） |
| spectral_stats | object | 频谱统计信息（Hz） |

### 3. keyframes（关键帧数组）

包含所有时间点的表情参数。

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "parameters": {
        "ParamEyeLOpen": 1.0,
        "ParamEyeROpen": 1.0,
        "ParamEyeBrowLY": 0.0,
        "ParamEyeBrowRY": 0.0,
        "ParamMouthOpenY": 0.2,
        "ParamMouthForm": 0.0,
        "ParamCheek": 0.0,
        "ParamBodyAngleX": 0.0,
        "ParamBodyAngleY": 0.0,
        "ParamBodyAngleZ": 0.0
      },
      "emotion": "neutral",
      "energy": 0.5,
      "description": "开始状态，平静表情"
    },
    {
      "timestamp": 0.1,
      "parameters": {
        "ParamEyeLOpen": 0.9,
        "ParamEyeROpen": 0.9,
        "ParamMouthOpenY": 0.3
      },
      "emotion": "happy",
      "energy": 0.6
    }
  ]
}
```

**关键帧字段说明**

| 字段名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| timestamp | float | 是 | 时间戳（秒） |
| parameters | object | 是 | Live2D参数值 |
| emotion | string | 否 | 当前情感标签 |
| energy | float | 否 | 当前能量级别（0-1） |
| description | string | 否 | 描述信息 |

---

## 🎭 Live2D参数说明

### 参数命名规范

Live2D标准参数遵循以下命名规则：

```
Param{部位}{动作}{方向}
```

### 常用参数列表

| 参数名 | 范围 | 说明 |
|-------|------|------|
| **眼部参数** | | |
| ParamEyeLOpen | 0.0 - 1.0 | 左眼开合度（0=闭眼，1=睁眼） |
| ParamEyeROpen | 0.0 - 1.0 | 右眼开合度 |
| ParamEyeLSmile | 0.0 - 1.0 | 左眼笑眯程度 |
| ParamEyeRSmile | 0.0 - 1.0 | 右眼笑眯程度 |
| ParamEyeBallX | -1.0 - 1.0 | 眼球左右移动 |
| ParamEyeBallY | -1.0 - 1.0 | 眼球上下移动 |
| **眉毛参数** | | |
| ParamEyeBrowLY | -1.0 - 1.0 | 左眉上下移动（负=下，正=上） |
| ParamEyeBrowRY | -1.0 - 1.0 | 右眉上下移动 |
| ParamEyeBrowLX | -1.0 - 1.0 | 左眉内外移动 |
| ParamEyeBrowRX | -1.0 - 1.0 | 右眉内外移动 |
| ParamEyeBrowLAngle | -1.0 - 1.0 | 左眉角度 |
| ParamEyeBrowRAngle | -1.0 - 1.0 | 右眉角度 |
| **嘴部参数** | | |
| ParamMouthOpenY | 0.0 - 1.0 | 嘴部开合度 |
| ParamMouthForm | -1.0 - 1.0 | 嘴型（负=不悦，正=微笑） |
| ParamMouthSmile | 0.0 - 1.0 | 嘴角上扬程度 |
| **脸颊参数** | | |
| ParamCheek | 0.0 - 1.0 | 脸颊红晕 |
| **身体参数** | | |
| ParamBodyAngleX | -10.0 - 10.0 | 身体左右倾斜角度 |
| ParamBodyAngleY | -10.0 - 10.0 | 身体前后倾斜角度 |
| ParamBodyAngleZ | -10.0 - 10.0 | 身体旋转角度 |

### 参数值约定

- **范围**: 大部分参数在 `[0.0, 1.0]` 或 `[-1.0, 1.0]` 范围
- **中性值**: 通常为 `0.0`（双向参数）或 `1.0`（单向参数）
- **过渡**: 建议使用平滑插值避免突变

---

## 💡 使用示例

### 读取表情文件

#### Python

```python
import json

def load_expression(file_path):
    """加载表情文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 使用示例
expression = load_expression('data/expressions/xxx.json')
print(f"时长: {expression['metadata']['duration']}秒")
print(f"关键帧数: {len(expression['keyframes'])}")

# 获取特定时间的表情参数
def get_expression_at_time(expression, time):
    """获取指定时间的表情参数"""
    keyframes = expression['keyframes']
    
    for i, kf in enumerate(keyframes):
        if kf['timestamp'] > time:
            if i == 0:
                return keyframes[0]['parameters']
            
            # 线性插值
            prev = keyframes[i - 1]
            curr = kf
            
            ratio = (time - prev['timestamp']) / (curr['timestamp'] - prev['timestamp'])
            
            params = {}
            for key in prev['parameters']:
                prev_val = prev['parameters'][key]
                curr_val = curr['parameters'].get(key, prev_val)
                params[key] = prev_val + (curr_val - prev_val) * ratio
            
            return params
    
    return keyframes[-1]['parameters']

# 在2.5秒时的表情
params = get_expression_at_time(expression, 2.5)
print(f"眼睛开合度: {params['ParamEyeLOpen']}")
```

#### JavaScript

```javascript
// 加载表情文件
async function loadExpression(filePath) {
  const response = await fetch(filePath);
  const data = await response.json();
  return data;
}

// 获取指定时间的表情参数
function getExpressionAtTime(expression, time) {
  const keyframes = expression.keyframes;
  
  for (let i = 0; i < keyframes.length; i++) {
    if (keyframes[i].timestamp > time) {
      if (i === 0) return keyframes[0].parameters;
      
      const prev = keyframes[i - 1];
      const curr = keyframes[i];
      
      const ratio = (time - prev.timestamp) / (curr.timestamp - prev.timestamp);
      
      const params = {};
      for (const key in prev.parameters) {
        const prevVal = prev.parameters[key];
        const currVal = curr.parameters[key] ?? prevVal;
        params[key] = prevVal + (currVal - prevVal) * ratio;
      }
      
      return params;
    }
  }
  
  return keyframes[keyframes.length - 1].parameters;
}

// 使用示例
const expression = await loadExpression('/data/expressions/xxx.json');
const params = getExpressionAtTime(expression, 2.5);
console.log('眼睛开合度:', params.ParamEyeLOpen);
```

### 应用到Live2D模型

#### JavaScript + pixi-live2d-display

```javascript
import * as PIXI from 'pixi.js';
import { Live2DModel } from 'pixi-live2d-display';

// 创建应用
const app = new PIXI.Application({
  view: document.getElementById('canvas'),
  autoStart: true,
  transparent: true
});

// 加载Live2D模型
const model = await Live2DModel.from('/models/hiyori/hiyori.model3.json');
app.stage.addChild(model);

// 加载表情数据
const expression = await loadExpression('/data/expressions/xxx.json');

// 同步音频播放
const audio = new Audio('/data/uploads/xxx.mp3');
audio.play();

// 实时更新表情
app.ticker.add(() => {
  const currentTime = audio.currentTime;
  const params = getExpressionAtTime(expression, currentTime);
  
  // 更新模型参数
  for (const [paramId, value] of Object.entries(params)) {
    model.internalModel.coreModel.setParameterValueById(paramId, value);
  }
});
```

---

## 🔄 版本兼容性

### v1.0格式

- **发布日期**: 2024-12
- **兼容性**: Live2D Cubism SDK 3.0+
- **向后兼容**: 否（首个版本）

### 未来版本规划

- v1.1: 添加音素（Phoneme）支持
- v1.2: 添加物理模拟参数
- v2.0: 支持多模型联动

---

## 📊 文件大小参考

| 音频时长 | 时间分辨率 | 关键帧数 | 文件大小 |
|---------|-----------|---------|---------|
| 30秒 | 0.1s | ~300 | ~50KB |
| 1分钟 | 0.1s | ~600 | ~100KB |
| 3分钟 | 0.1s | ~1800 | ~300KB |
| 5分钟 | 0.1s | ~3000 | ~500KB |
| 5分钟 | 0.05s | ~6000 | ~1MB |

---

## ⚠️ 注意事项

1. **参数范围验证**
   - 确保所有参数值在有效范围内
   - 超出范围可能导致渲染异常

2. **时间戳顺序**
   - 关键帧必须按时间戳升序排列
   - 不能有重复的时间戳

3. **参数完整性**
   - 首个关键帧应包含所有参数
   - 后续关键帧可只包含变化的参数

4. **文件编码**
   - 必须使用UTF-8编码
   - 避免使用BOM标记

5. **性能考虑**
   - 过多关键帧会影响渲染性能
   - 建议时间分辨率不低于0.05秒

---

## 🔗 相关资源

- **用户指南**: [USER_GUIDE.md](USER_GUIDE.md)
- **API文档**: [API_REFERENCE.md](API_REFERENCE.md)
- **Live2D官方文档**: https://docs.live2d.com/

---

**版本**: v1.0.0  
**更新日期**: 2024-12
