# 📚 文档索引 v1.0

歌颜随动项目完整文档导航。

---

## 🎯 快速导航

### 新用户入门

1. **[README.md](../README.md)** - 项目概览和快速开始
2. **[用户使用指南](USER_GUIDE.md)** - 详细使用教程

### 开发者文档

1. **[开发者指南](DEVELOPER_GUIDE.md)** - 开发环境配置和架构说明
2. **[API接口文档](API_REFERENCE.md)** - 完整API接口说明
3. **[表情格式说明](EXPRESSION_FORMAT.md)** - 表情文件格式详解

---

## 📖 文档详情

### 用户文档

#### 📘 用户使用指南 (USER_GUIDE.md)

**适合**: 使用者、内容创作者

**内容**:
- 快速开始指南
- 功能介绍
- 详细使用教程
- 参数配置说明
- 常见问题解答
- 最佳实践

**章节**:
1. 🚀 快速开始
   - 系统要求
   - 安装步骤
   - 启动服务
2. ✨ 功能介绍
   - 核心功能
   - 支持格式
3. 📚 使用教程
   - 上传音频
   - 配置参数
   - 开始处理
   - 预览表情
   - 导出结果
4. 🎨 表情映射规则
5. ❓ 常见问题
6. 🎯 最佳实践

---

### 开发者文档

#### 💻 开发者指南 (DEVELOPER_GUIDE.md)

**适合**: 开发者、贡献者

**内容**:
- 技术架构详解
- 开发环境配置
- 代码结构说明
- 开发规范
- 测试指南
- 部署说明

**章节**:
1. 🏗️ 技术架构
   - 整体架构图
   - 技术栈
2. 🔧 环境配置
   - 基础环境
   - API密钥
   - 目录初始化
3. 📁 代码结构
   - 目录结构
   - 核心模块
4. 🛠️ 开发指南
   - API开发
   - 前端开发
   - 功能扩展
5. 🧪 测试规范
6. 🚀 部署说明
7. 📊 性能优化
8. 📝 代码规范

#### 🔌 API接口文档 (API_REFERENCE.md)

**适合**: API集成开发者

**内容**:
- 完整API接口列表
- 请求/响应格式
- 错误码说明
- 代码示例

**接口列表**:
1. `GET /health` - 健康检查
2. `POST /api/v1/upload` - 文件上传
3. `POST /api/v1/analyze` - 音频分析
4. `POST /api/v1/expression/generate` - 表情生成
5. `GET /api/v1/expression/{id}` - 获取表情数据

**特色**:
- cURL示例
- Python示例代码
- JavaScript示例代码
- 完整工作流程
- 性能指标参考

#### 📄 表情格式说明 (EXPRESSION_FORMAT.md)

**适合**: Live2D开发者、数据集成者

**内容**:
- 表情文件JSON格式详解
- Live2D参数说明
- 使用示例代码
- 版本兼容性

**核心内容**:
1. JSON结构说明
   - metadata（元数据）
   - audio_features（音频特征）
   - keyframes（关键帧数组）
2. Live2D参数列表
   - 眼部参数
   - 眉毛参数
   - 嘴部参数
   - 身体参数
3. 使用示例
   - Python读取示例
   - JavaScript读取示例
   - Live2D集成示例

---

## 🗂️ 文档分类

### 按角色分类

#### 👤 普通用户

- ✅ README.md
- ✅ USER_GUIDE.md

#### 👨‍💻 开发者

- ✅ README.md
- ✅ DEVELOPER_GUIDE.md
- ✅ API_REFERENCE.md
- ✅ EXPRESSION_FORMAT.md

#### 🎨 Live2D创作者

- ✅ USER_GUIDE.md
- ✅ EXPRESSION_FORMAT.md

#### 🔧 系统集成者

- ✅ API_REFERENCE.md
- ✅ DEVELOPER_GUIDE.md

### 按主题分类

#### 📦 安装部署

- README.md - 快速开始
- DEVELOPER_GUIDE.md - 详细配置
- DEVELOPER_GUIDE.md - Docker部署

#### 🎵 音频处理

- USER_GUIDE.md - 支持格式
- API_REFERENCE.md - 分析接口
- DEVELOPER_GUIDE.md - 音频模块

#### 🎭 表情生成

- USER_GUIDE.md - 表情映射规则
- API_REFERENCE.md - 生成接口
- EXPRESSION_FORMAT.md - 文件格式
- DEVELOPER_GUIDE.md - 生成器模块

#### 🔌 API集成

- API_REFERENCE.md - 完整接口文档
- DEVELOPER_GUIDE.md - API开发

#### 🧪 测试调试

- DEVELOPER_GUIDE.md - 测试规范
- DEVELOPER_GUIDE.md - 调试技巧

---

## 📊 文档版本

| 文档名称 | 版本 | 更新日期 | 状态 |
|---------|------|---------|------|
| README.md | v1.0 | 2024-12 | ✅ 最新 |
| USER_GUIDE.md | v1.0 | 2024-12 | ✅ 最新 |
| DEVELOPER_GUIDE.md | v1.0 | 2024-12 | ✅ 最新 |
| API_REFERENCE.md | v1.0 | 2024-12 | ✅ 最新 |
| EXPRESSION_FORMAT.md | v1.0 | 2024-12 | ✅ 最新 |
| DOC_INDEX.md | v1.0 | 2024-12 | ✅ 最新 |

---

## 🔍 快速查找

### 常见任务对应文档

| 任务 | 文档 | 章节 |
|-----|------|------|
| 第一次使用系统 | USER_GUIDE.md | 快速开始 |
| 上传并处理音频 | USER_GUIDE.md | 使用教程 |
| 调整表情参数 | USER_GUIDE.md | 参数配置 |
| 遇到问题 | USER_GUIDE.md | 常见问题 |
| 配置开发环境 | DEVELOPER_GUIDE.md | 环境配置 |
| 了解代码架构 | DEVELOPER_GUIDE.md | 技术架构 |
| 添加新功能 | DEVELOPER_GUIDE.md | 开发指南 |
| 调用API | API_REFERENCE.md | 接口列表 |
| 理解表情文件 | EXPRESSION_FORMAT.md | JSON结构 |
| 集成Live2D | EXPRESSION_FORMAT.md | 使用示例 |

### 关键词索引

- **安装**: README.md, DEVELOPER_GUIDE.md
- **API密钥**: README.md, DEVELOPER_GUIDE.md
- **上传**: USER_GUIDE.md, API_REFERENCE.md
- **分析**: USER_GUIDE.md, API_REFERENCE.md
- **表情生成**: USER_GUIDE.md, API_REFERENCE.md
- **参数配置**: USER_GUIDE.md, EXPRESSION_FORMAT.md
- **Live2D**: EXPRESSION_FORMAT.md
- **错误处理**: API_REFERENCE.md
- **测试**: DEVELOPER_GUIDE.md
- **部署**: DEVELOPER_GUIDE.md
- **Docker**: DEVELOPER_GUIDE.md
- **性能优化**: DEVELOPER_GUIDE.md

---

## 📱 文档获取方式

### 在线查看

- **GitHub**: https://github.com/yidong-liu/geyan-suidong-/tree/main/docs
- **本地**: 在 `docs/` 目录查看Markdown文件

### 离线阅读

1. 克隆项目获取所有文档
   ```bash
   git clone https://github.com/yidong-liu/geyan-suidong-.git
   cd geyan-suidong-/docs
   ```

2. 使用Markdown阅读器打开
   - VS Code + Markdown Preview
   - Typora
   - MacDown
   - 任何支持Markdown的编辑器

### 生成PDF（可选）

使用Pandoc转换为PDF：

```bash
# 安装pandoc
# macOS: brew install pandoc
# Ubuntu: sudo apt install pandoc

# 转换单个文档
pandoc USER_GUIDE.md -o USER_GUIDE.pdf

# 批量转换
for file in *.md; do
  pandoc "$file" -o "${file%.md}.pdf"
done
```

---

## 🆘 获取帮助

### 文档相关问题

如果您在文档中发现：
- ❌ 错误或过时信息
- ❓ 不清楚的说明
- 💡 改进建议

请：
1. 提交[GitHub Issue](https://github.com/yidong-liu/geyan-suidong-/issues)
2. 标注 `documentation` 标签
3. 说明具体文档和位置

### 功能使用问题

- 查阅 USER_GUIDE.md 的"常见问题"章节
- 提交GitHub Issue描述问题
- 查看已有Issue是否有解决方案

### 开发相关问题

- 查阅 DEVELOPER_GUIDE.md
- 查看API_REFERENCE.md的错误码说明
- 检查日志文件
- 提交Issue附带错误日志

---

## 📝 贡献文档

欢迎贡献文档改进！

### 贡献流程

1. Fork项目
2. 创建分支 `git checkout -b doc/improve-xxx`
3. 修改文档
4. 提交更改 `git commit -m 'docs: improve xxx'`
5. 推送分支 `git push origin doc/improve-xxx`
6. 创建Pull Request

### 文档规范

- 使用Markdown格式
- 遵循现有文档结构
- 添加代码示例时确保可运行
- 更新相关的索引和链接
- 中英文之间添加空格

---

## 🔄 更新日志

### v1.0.0 (2024-12)

**新增**:
- ✨ 创建完整的v1.0文档体系
- ✨ USER_GUIDE.md - 用户使用指南
- ✨ DEVELOPER_GUIDE.md - 开发者指南
- ✨ API_REFERENCE.md - API接口文档
- ✨ EXPRESSION_FORMAT.md - 表情格式说明
- ✨ DOC_INDEX.md - 文档索引

**废弃**:
- ⚠️ architecture.md（内容整合到DEVELOPER_GUIDE.md）
- ⚠️ development.md（内容整合到DEVELOPER_GUIDE.md）
- ⚠️ backend_guide.md（内容整合到DEVELOPER_GUIDE.md）
- ⚠️ frontend_guide.md（内容整合到DEVELOPER_GUIDE.md）
- ⚠️ BACKEND_API.md（被API_REFERENCE.md替代）
- ⚠️ FRONTEND_GUIDE.md（内容整合到USER_GUIDE.md）

---

**版本**: v1.0.0  
**更新日期**: 2024-12  
**维护**: [@yidong-liu](https://github.com/yidong-liu)

🎵✨ 让文档更清晰，让开发更简单！
