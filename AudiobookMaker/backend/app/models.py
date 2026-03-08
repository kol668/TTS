from pydantic import BaseModel
from typing import List, Dict, Optional

class Character(BaseModel):
    name: str
    description: str
    dialogue_count: int
    voice_id: Optional[str] = None

class BookUploadResponse(BaseModel):
    book_id: str
    filename: str
    characters: List[Character]
    preview: str

class AudioGenerationRequest(BaseModel):
    book_id: str
    character_voices: Dict[str, str]  # 角色名 -> 声音ID
    speed: Optional[float] = 1.0
    pitch: Optional[float] = 1.0

class AudioGenerationResponse(BaseModel):
    book_id: str
    status: str
    download_url: str
    duration: float

class Voice(BaseModel):
    id: str
    name: str
    gender: str
    language: str
    preview_url: Optional[str] = None
