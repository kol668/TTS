import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# 导入各种 TTS 服务
from app.services.edge_tts import EdgeTTSSynthesizer, get_voice_for_character
from app.services.tencent_tts import TencentCloudTTS, get_tencent_voice_for_character

load_dotenv()

class VoiceSynthesizer:
    """语音合成器 - 支持多种TTS服务（国内优先）"""
    
    def __init__(self):
        # 各种API密钥
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.azure_key = os.getenv("AZURE_SPEECH_KEY")
        self.azure_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.tencent_secret_id = os.getenv("TENCENT_SECRET_ID")
        self.tencent_secret_key = os.getenv("TENCENT_SECRET_KEY")
        
        # 初始化各种TTS服务
        self.edge_tts = EdgeTTSSynthesizer()
        self.tencent_tts = TencentCloudTTS(self.tencent_secret_id, self.tencent_secret_key)
        
        # 默认使用国内服务（Edge TTS）
        self.default_provider = 'edge'
    
    def get_voices(self) -> List[Dict]:
        """获取所有可用声音列表"""
        voices = []
        
        # 1. Edge TTS（国内可用，免费，无需注册）
        edge_voices = self.edge_tts.get_voices()
        for v in edge_voices:
            v['provider'] = 'edge'
        voices.extend(edge_voices)
        
        # 2. 腾讯云 TTS（国内服务，需要密钥）
        if self.tencent_secret_id and self.tencent_secret_key:
            try:
                tencent_voices = self.tencent_tts.get_voices()
                for v in tencent_voices:
                    v['provider'] = 'tencent'
                voices.extend(tencent_voices)
            except Exception as e:
                print(f"获取腾讯云声音失败: {e}")
        
        # 3. Azure（国外服务）
        if self.azure_key:
            # 添加Azure默认声音
            azure_voices = [
                {'id': 'azure:xiaoxiao', 'name': 'Azure 晓晓', 'gender': 'Female', 'provider': 'azure'},
                {'id': 'azure:yunxi', 'name': 'Azure 云希', 'gender': 'Male', 'provider': 'azure'},
            ]
            voices.extend(azure_voices)
        
        # 4. ElevenLabs（国外服务，高质量）
        if self.elevenlabs_key:
            try:
                eleven_voices = self._get_elevenlabs_voices()
                voices.extend(eleven_voices)
            except Exception as e:
                print(f"获取ElevenLabs声音失败: {e}")
        
        return voices
    
    def _get_elevenlabs_voices(self) -> List[Dict]:
        """获取ElevenLabs声音列表"""
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": self.elevenlabs_key}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        voices = []
        
        for voice in data.get('voices', []):
            voices.append({
                'id': f"elevenlabs:{voice['voice_id']}",
                'name': f"ElevenLabs {voice['name']}",
                'gender': 'Unknown',
                'language': 'multi',
                'provider': 'elevenlabs'
            })
        
        return voices
    
    def synthesize(self, text: str, voice_id: str, 
                   output_path: Optional[str] = None) -> str:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            voice_id: 声音ID（格式：provider:voice_id 或直接 voice_id）
            output_path: 输出路径（可选）
        
        Returns:
            输出文件路径
        """
        # 解析 provider
        if ':' in voice_id:
            provider, actual_voice_id = voice_id.split(':', 1)
        else:
            provider = 'edge'  # 默认使用 Edge TTS
            actual_voice_id = voice_id
        
        # 根据 provider 调用对应服务
        if provider == 'tencent':
            # 腾讯云
            return self.tencent_tts.synthesize(text, actual_voice_id, output_path)
        
        elif provider == 'azure':
            # Azure
            if not self.azure_key:
                raise ValueError("Azure Speech Key未配置")
            return self._synthesize_azure(text, actual_voice_id, output_path)
        
        elif provider == 'elevenlabs':
            # ElevenLabs
            if not self.elevenlabs_key:
                raise ValueError("ElevenLabs API Key未配置")
            return self._synthesize_elevenlabs(text, actual_voice_id, output_path)
        
        else:
            # 默认 Edge TTS（国内可用，免费）
            return self.edge_tts.synthesize(text, voice_id, output_path)
    
    def synthesize_segment(self, text: str, speaker: str,
                          output_dir: str = 'outputs') -> str:
        """
        为特定说话人合成语音（自动选择合适的声音）
        
        Args:
            text: 文本内容
            speaker: 说话人名称
            output_dir: 输出目录
        
        Returns:
            输出文件路径
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 优先使用腾讯云（如果配置了）
        if self.tencent_secret_id and self.tencent_secret_key:
            voice_id = get_tencent_voice_for_character(speaker)
            provider = 'tencent'
        else:
            # 使用 Edge TTS
            voice_id = get_voice_for_character(speaker)
            provider = 'edge'
        
        # 生成文件名
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        safe_speaker = "".join(c for c in speaker if c.isalnum() or c in (' ', '-', '_')).strip()
        output_path = os.path.join(output_dir, f"{safe_speaker}_{text_hash}.mp3")
        
        # 合成
        full_voice_id = f"{provider}:{voice_id}" if provider != 'edge' else voice_id
        return self.synthesize(text, full_voice_id, output_path)
    
    def synthesize_audiobook(self, segments: List[Dict], 
                            output_path: str = 'outputs/audiobook.mp3') -> str:
        """
        合成完整有声书
        
        Args:
            segments: 文本片段列表，每个包含 'speaker' 和 'text'
            output_path: 输出文件路径
        
        Returns:
            输出文件路径
        """
        from pydub import AudioSegment
        import tempfile
        
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 临时目录
        temp_dir = tempfile.mkdtemp()
        
        # 合成每个片段
        audio_segments = []
        for i, segment in enumerate(segments):
            speaker = segment.get('speaker', '旁白')
            text = segment.get('text', '')
            
            if not text.strip():
                continue
            
            try:
                # 合成语音
                audio_path = self.synthesize_segment(text, speaker, temp_dir)
                audio_segments.append(audio_path)
                print(f"[{i+1}/{len(segments)}] 已合成: {speaker}")
            except Exception as e:
                print(f"[{i+1}/{len(segments)}] 合成失败 {speaker}: {e}")
        
        # 合并音频
        if audio_segments:
            print(f"\n正在合并 {len(audio_segments)} 个音频片段...")
            combined = AudioSegment.from_mp3(audio_segments[0])
            
            # 添加间隔
            silence = AudioSegment.silent(duration=500)
            
            for audio_path in audio_segments[1:]:
                combined += silence
                audio = AudioSegment.from_mp3(audio_path)
                combined += audio
            
            # 导出
            combined.export(output_path, format="mp3", bitrate="128k")
            print(f"有声书已生成: {output_path}")
            
            # 清理临时文件
            import shutil
            shutil.rmtree(temp_dir)
            
            return output_path
        else:
            raise Exception("没有成功生成任何音频片段")
    
    def _synthesize_azure(self, text: str, voice_id: str, 
                         output_path: Optional[str] = None) -> str:
        """使用Azure语音合成"""
        if not output_path:
            import tempfile
            output_path = tempfile.mktemp(suffix='.mp3')
        
        url = f"https://{self.azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
        }
        
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
            <voice name='{voice_id}'>
                {text}
            </voice>
        </speak>
        """
        
        response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    def _synthesize_elevenlabs(self, text: str, voice_id: str,
                              output_path: Optional[str] = None) -> str:
        """使用ElevenLabs语音合成"""
        if not output_path:
            import tempfile
            output_path = tempfile.mktemp(suffix='.mp3')
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
