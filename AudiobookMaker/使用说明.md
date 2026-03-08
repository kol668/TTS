# AudiobookMaker 使用说明

## 快速开始

### 1. 配置API密钥

复制 `backend/.env.example` 为 `backend/.env`，并填入你的API密钥：

```bash
cd backend
copy .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=你的OpenAI_API密钥
ELEVENLABS_API_KEY=你的ElevenLabs_API密钥（可选）
AZURE_SPEECH_KEY=你的Azure语音密钥（可选）
```

获取API密钥：
- **OpenAI**: https://platform.openai.com/api-keys
- **ElevenLabs**: https://elevenlabs.io/app/sign-up
- **Azure Speech**: https://azure.microsoft.com/zh-cn/services/cognitive-services/speech-to-text/

### 2. 启动应用

双击运行 `start.bat`，或手动执行：

```bash
# 启动后端
cd backend
pip install -r requirements.txt
python -m app.main

# 启动前端（新终端）
cd frontend
npm install
npm start
```

### 3. 使用应用

1. 打开浏览器访问 http://localhost:3000
2. 上传书籍文件（TXT/EPUB/PDF）
3. AI自动识别角色
4. 为每个角色选择声音
5. 点击生成有声书
6. 下载生成的MP3文件

## 功能说明

### 支持的文件格式
- **TXT**: 纯文本文件
- **EPUB**: 电子书格式
- **PDF**: PDF文档

### 角色识别
- 自动识别对话和旁白
- 提取说话人名称
- AI分析角色特征

### 语音合成
- 支持多种声音（男声/女声）
- 支持Azure语音服务
- 支持ElevenLabs高质量语音（需API密钥）

### 音频处理
- 自动合并音频片段
- 添加段落间隔
- 标准化音量

## 示例：《剑来》

1. 准备《剑来》的TXT文件
2. 上传到应用
3. AI会识别出：陈平安、宁姚、齐静春等角色
4. 为陈平安选择男声，宁姚选择女声
5. 生成有声书

## 注意事项

1. **API费用**: 使用OpenAI和语音合成API会产生费用，请注意控制使用量
2. **文件大小**: 建议上传文件不超过10MB，大文件可以分章节处理
3. **网络连接**: 需要稳定的网络连接以调用API服务

## 技术架构

- **后端**: Python + FastAPI
- **前端**: HTML5 + JavaScript
- **AI**: OpenAI GPT-3.5
- **语音**: Azure Speech / ElevenLabs
- **音频处理**: pydub

## 自定义开发

### 添加新的语音提供商

编辑 `backend/app/services/voice_synthesizer.py`，添加新的合成方法。

### 修改角色识别逻辑

编辑 `backend/app/services/character_recognizer.py`，调整识别规则。

### 自定义前端样式

编辑 `frontend/index.html`，修改CSS样式。

## 常见问题

**Q: 为什么生成速度很慢？**
A: 语音合成需要调用API，速度取决于网络状况和文本长度。

**Q: 可以免费使用吗？**
A: 可以，使用Azure免费额度或本地TTS引擎，但音质可能不如付费API。

**Q: 支持哪些语言？**
A: 目前主要支持中文，可通过修改配置支持其他语言。

## 许可证

MIT License
