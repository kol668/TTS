# AudiobookMaker - AI有声书制作工具

一个智能有声书制作应用，可以自动识别文本中的角色并为每个角色分配不同的声音。

## 功能特性

- 📚 导入文本文件（TXT、EPUB、PDF）
- 🤖 AI自动识别角色和对话
- 🎙️ 为不同角色分配不同声音
- 🔊 生成高质量有声书音频
- ✂️ 音频编辑和合并

## 项目结构

```
AudiobookMaker/
├── backend/              # Python后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI主应用
│   │   ├── models.py    # 数据模型
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── text_parser.py      # 文本解析
│   │   │   ├── character_recognizer.py  # 角色识别
│   │   │   ├── voice_synthesizer.py     # 语音合成
│   │   │   └── audio_processor.py       # 音频处理
│   │   └── api/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── requirements.txt
│   └── config.py
├── frontend/             # React前端
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── public/
└── README.md
```

## 安装和运行

### 后端
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### 前端
```bash
cd frontend
npm install
npm start
```

## API配置

在使用前，需要配置以下API密钥：
- OpenAI API Key（用于角色识别）
- ElevenLabs API Key（用于语音合成）
- Azure Speech API Key（备选语音合成）

在 `backend/.env` 文件中配置：
```
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

## 使用说明

1. 上传文本文件
2. AI自动分析角色
3. 为每个角色选择声音
4. 生成有声书
5. 下载音频文件
