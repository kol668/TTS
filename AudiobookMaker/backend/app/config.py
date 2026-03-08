# 配置文件
import os
from dotenv import load_dotenv

load_dotenv()

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

# 应用配置
APP_NAME = "AudiobookMaker"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# 文件路径
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
TEMP_DIR = "temp"

# 音频配置
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_BITRATE = "128k"
DEFAULT_AUDIO_FORMAT = "mp3"

# 角色声音映射（预设）
DEFAULT_CHARACTER_VOICES = {
    "旁白": "narrator",
    "男主角": "male",
    "女主角": "default",
}
