from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
from typing import List, Optional

from app.models import BookUploadResponse, Character, AudioGenerationRequest, AudioGenerationResponse
from app.services.text_parser import TextParser
from app.services.character_recognizer import CharacterRecognizer
from app.services.voice_synthesizer import VoiceSynthesizer
from app.services.audio_processor import AudioProcessor

app = FastAPI(title="AudiobookMaker API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
text_parser = TextParser()
character_recognizer = CharacterRecognizer()
voice_synthesizer = VoiceSynthesizer()
audio_processor = AudioProcessor()

# 存储上传的文件
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "AudiobookMaker API 运行中", "version": "1.0.0"}

@app.post("/api/upload", response_model=BookUploadResponse)
async def upload_book(file: UploadFile = File(...)):
    """上传书籍文件"""
    try:
        # 生成唯一ID
        book_id = str(uuid.uuid4())
        
        # 保存文件
        file_path = os.path.join(UPLOAD_DIR, f"{book_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 解析文本
        text_content = text_parser.parse(file_path)
        
        # 识别角色
        characters = character_recognizer.recognize(text_content)
        
        return BookUploadResponse(
            book_id=book_id,
            filename=file.filename,
            characters=characters,
            preview=text_content[:1000]  # 返回前1000字预览
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate", response_model=AudioGenerationResponse)
async def generate_audiobook(request: AudioGenerationRequest):
    """生成有声书"""
    try:
        book_id = request.book_id
        character_voices = request.character_voices
        
        # 获取文本内容
        file_path = os.path.join(UPLOAD_DIR, f"{book_id}_*")
        import glob
        files = glob.glob(file_path)
        if not files:
            raise HTTPException(status_code=404, detail="书籍文件未找到")
        
        text_content = text_parser.parse(files[0])
        
        # 分段生成音频
        segments = character_recognizer.segment_by_speaker(text_content)
        audio_segments = []
        
        for segment in segments:
            speaker = segment['speaker']
            text = segment['text']
            voice_id = character_voices.get(speaker, 'default')
            
            # 生成语音
            audio_data = voice_synthesizer.synthesize(text, voice_id)
            audio_segments.append(audio_data)
        
        # 合并音频
        output_path = os.path.join(OUTPUT_DIR, f"{book_id}_audiobook.mp3")
        audio_processor.merge_audio(audio_segments, output_path)
        
        return AudioGenerationResponse(
            book_id=book_id,
            status="completed",
            download_url=f"/api/download/{book_id}",
            duration=audio_processor.get_duration(output_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{book_id}")
async def download_audiobook(book_id: str):
    """下载有声书"""
    file_path = os.path.join(OUTPUT_DIR, f"{book_id}_audiobook.mp3")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="音频文件未找到")
    
    return FileResponse(file_path, filename=f"audiobook_{book_id}.mp3")

@app.get("/api/voices")
async def get_available_voices():
    """获取可用声音列表"""
    return voice_synthesizer.get_voices()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
