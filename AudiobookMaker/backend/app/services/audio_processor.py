import os
from typing import List
from pydub import AudioSegment
import io

class AudioProcessor:
    """音频处理器 - 处理和合并音频"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
    
    def merge_audio(self, audio_segments: List[bytes], output_path: str):
        """合并多个音频片段"""
        if not audio_segments:
            raise ValueError("没有音频片段需要合并")
        
        # 将第一个片段作为基础
        combined = AudioSegment.from_mp3(io.BytesIO(audio_segments[0]))
        
        # 添加间隔
        silence = AudioSegment.silent(duration=500)  # 500ms间隔
        
        # 合并其他片段
        for segment in audio_segments[1:]:
            combined += silence
            audio = AudioSegment.from_mp3(io.BytesIO(segment))
            combined += audio
        
        # 导出
        combined.export(output_path, format="mp3", bitrate="128k")
    
    def add_background_music(self, voice_path: str, music_path: str, output_path: str, 
                            voice_volume: int = 0, music_volume: int = -20):
        """添加背景音乐"""
        voice = AudioSegment.from_mp3(voice_path)
        music = AudioSegment.from_mp3(music_path)
        
        # 调整音量
        voice = voice + voice_volume
        music = music + music_volume
        
        # 循环背景音乐以匹配语音长度
        while len(music) < len(voice):
            music += music
        
        music = music[:len(voice)]
        
        # 混合
        combined = voice.overlay(music)
        combined.export(output_path, format="mp3")
    
    def adjust_speed(self, audio_path: str, output_path: str, speed: float = 1.0):
        """调整播放速度"""
        audio = AudioSegment.from_mp3(audio_path)
        
        # 调整速度（同时改变音调）
        if speed != 1.0:
            # 使用帧率调整速度
            new_frame_rate = int(audio.frame_rate * speed)
            audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
            audio = audio.set_frame_rate(16000)
        
        audio.export(output_path, format="mp3")
    
    def get_duration(self, audio_path: str) -> float:
        """获取音频时长（秒）"""
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0  # 转换为秒
    
    def split_audio(self, audio_path: str, segment_length: int = 600) -> List[str]:
        """将音频分割成多个片段（默认10分钟一段）"""
        audio = AudioSegment.from_mp3(audio_path)
        duration = len(audio) / 1000  # 总时长（秒）
        
        segments = []
        base_name = os.path.splitext(audio_path)[0]
        
        for i in range(0, int(duration), segment_length):
            start = i * 1000
            end = min((i + segment_length) * 1000, len(audio))
            segment = audio[start:end]
            
            segment_path = f"{base_name}_part{i//segment_length + 1}.mp3"
            segment.export(segment_path, format="mp3")
            segments.append(segment_path)
        
        return segments
    
    def normalize_audio(self, audio_path: str, output_path: str, target_db: float = -20.0):
        """标准化音频音量"""
        audio = AudioSegment.from_mp3(audio_path)
        
        # 计算当前dBFS
        current_db = audio.dBFS
        
        # 调整音量
        change_in_db = target_db - current_db
        normalized = audio.apply_gain(change_in_db)
        
        normalized.export(output_path, format="mp3")
