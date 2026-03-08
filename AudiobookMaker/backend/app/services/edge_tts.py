import os
import re
import json
import subprocess
from typing import List, Dict, Optional

class EdgeTTSSynthesizer:
    """使用 Edge 浏览器语音合成（免费，无需API密钥）"""
    
    def __init__(self):
        # Edge TTS 支持的中文语音
        self.voices = {
            'default': {
                'name': 'zh-CN-XiaoxiaoNeural',
                'display_name': '晓晓（女声）',
                'gender': 'Female'
            },
            'xiaoxiao': {
                'name': 'zh-CN-XiaoxiaoNeural',
                'display_name': '晓晓（女声）',
                'gender': 'Female'
            },
            'xiaoyi': {
                'name': 'zh-CN-XiaoyiNeural',
                'display_name': '晓伊（女声）',
                'gender': 'Female'
            },
            'yunxi': {
                'name': 'zh-CN-YunxiNeural',
                'display_name': '云希（男声）',
                'gender': 'Male'
            },
            'yunjian': {
                'name': 'zh-CN-YunjianNeural',
                'display_name': '云健（男声）',
                'gender': 'Male'
            },
            'xiaochen': {
                'name': 'zh-CN-XiaochenNeural',
                'display_name': '晓辰（女声）',
                'gender': 'Female'
            },
            'xiaohan': {
                'name': 'zh-CN-XiaohanNeural',
                'display_name': '晓涵（女声）',
                'gender': 'Female'
            },
            'xiaomeng': {
                'name': 'zh-CN-XiaomengNeural',
                'display_name': '晓梦（女声）',
                'gender': 'Female'
            },
            'xiaomo': {
                'name': 'zh-CN-XiaomoNeural',
                'display_name': '晓墨（男声）',
                'gender': 'Male'
            },
            'xiaoxuan': {
                'name': 'zh-CN-XiaoxuanNeural',
                'display_name': '晓萱（女声）',
                'gender': 'Female'
            },
            'xiaoyan': {
                'name': 'zh-CN-XiaoyanNeural',
                'display_name': '晓颜（女声）',
                'gender': 'Female'
            },
            'xiaoyou': {
                'name': 'zh-CN-XiaoyouNeural',
                'display_name': '晓悠（童声）',
                'gender': 'Female'
            },
            'yunfeng': {
                'name': 'zh-CN-YunfengNeural',
                'display_name': '云峰（男声）',
                'gender': 'Male'
            },
            'yunhao': {
                'name': 'zh-CN-YunhaoNeural',
                'display_name': '云浩（男声）',
                'gender': 'Male'
            },
            'yunxia': {
                'name': 'zh-CN-YunxiaNeural',
                'display_name': '云夏（男声）',
                'gender': 'Male'
            },
            'yunye': {
                'name': 'zh-CN-YunyeNeural',
                'display_name': '云野（男声）',
                'gender': 'Male'
            },
            'yunyang': {
                'name': 'zh-CN-YunyangNeural',
                'display_name': '云扬（男声）',
                'gender': 'Male'
            }
        }
        
        # 检查 edge-tts 是否安装
        self._check_edge_tts()
    
    def _check_edge_tts(self):
        """检查 edge-tts 是否已安装"""
        try:
            subprocess.run(['edge-tts', '--version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("正在安装 edge-tts...")
            subprocess.run(['pip', 'install', 'edge-tts'], check=True)
            print("edge-tts 安装完成")
    
    def get_voices(self) -> List[Dict]:
        """获取可用声音列表"""
        voices = []
        for key, voice in self.voices.items():
            voices.append({
                'id': key,
                'name': voice['display_name'],
                'gender': voice['gender'],
                'language': 'zh-CN',
                'provider': 'edge-tts'
            })
        return voices
    
    def synthesize(self, text: str, voice_id: str = 'default', 
                   output_path: Optional[str] = None) -> str:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            voice_id: 声音ID
            output_path: 输出文件路径（可选）
        
        Returns:
            输出文件路径
        """
        if not output_path:
            import tempfile
            output_path = tempfile.mktemp(suffix='.mp3')
        
        # 获取声音名称
        voice_name = self.voices.get(voice_id, self.voices['default'])['name']
        
        # 清理文本（移除可能导致问题的字符）
        text = self._clean_text(text)
        
        # 构建命令
        cmd = [
            'edge-tts',
            '--voice', voice_name,
            '--text', text,
            '--write-media', output_path
        ]
        
        # 执行命令
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                raise Exception(f"TTS 失败: {result.stderr}")
            return output_path
        except subprocess.TimeoutExpired:
            raise Exception("TTS 超时")
        except Exception as e:
            raise Exception(f"TTS 错误: {e}")
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除可能导致问题的字符"""
        # 移除控制字符
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        # 规范化空白字符
        text = ' '.join(text.split())
        return text.strip()
    
    def synthesize_long_text(self, text: str, voice_id: str = 'default',
                            output_dir: str = 'outputs') -> List[str]:
        """
        合成长文本（自动分段）
        
        Args:
            text: 长文本
            voice_id: 声音ID
            output_dir: 输出目录
        
        Returns:
            生成的音频文件列表
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 分段（每段约500字符）
        max_length = 500
        segments = self._split_text(text, max_length)
        
        output_files = []
        for i, segment in enumerate(segments):
            output_path = os.path.join(output_dir, f'segment_{i:03d}.mp3')
            try:
                self.synthesize(segment, voice_id, output_path)
                output_files.append(output_path)
                print(f"已生成: {output_path}")
            except Exception as e:
                print(f"生成失败 {i}: {e}")
        
        return output_files
    
    def _split_text(self, text: str, max_length: int = 500) -> List[str]:
        """将长文本分段"""
        segments = []
        current_segment = ""
        
        # 按句子分割
        sentences = re.split(r'([。！？.!?])', text)
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]  # 加上标点
            
            if len(current_segment) + len(sentence) <= max_length:
                current_segment += sentence
            else:
                if current_segment:
                    segments.append(current_segment)
                current_segment = sentence
        
        if current_segment:
            segments.append(current_segment)
        
        return segments if segments else [text]

# 角色声音映射（用于有声书）
CHARACTER_VOICE_MAP = {
    '旁白': 'xiaoxiao',
    '陈平安': 'yunxi',
    '宁姚': 'xiaoyi',
    '老人': 'yunjian',
    '爷爷': 'yunjian',
    '男主角': 'yunxi',
    '女主角': 'xiaoyi',
    '男': 'yunxi',
    '女': 'xiaoxiao',
    'default': 'xiaoxiao'
}

def get_voice_for_character(character_name: str) -> str:
    """根据角色名获取推荐声音"""
    for key, voice in CHARACTER_VOICE_MAP.items():
        if key in character_name:
            return voice
    return 'default'

# 测试代码
if __name__ == '__main__':
    tts = EdgeTTSSynthesizer()
    
    print("可用声音列表：")
    for voice in tts.get_voices()[:5]:
        print(f"  - {voice['name']} ({voice['id']})")
    
    print("\n测试语音合成...")
    test_text = "你好，这是测试语音。陈平安背着草鞋，走在泥瓶巷的石板路上。"
    output_file = tts.synthesize(test_text, 'yunxi')
    print(f"已生成: {output_file}")
