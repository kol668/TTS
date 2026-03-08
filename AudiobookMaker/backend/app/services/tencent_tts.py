import os
import json
import hashlib
import hmac
import base64
import time
import requests
from typing import List, Dict, Optional
from urllib.parse import urlencode

class TencentCloudTTS:
    """腾讯云语音合成（长文本）"""
    
    def __init__(self, secret_id: str = None, secret_key: str = None):
        self.secret_id = secret_id or os.getenv('TENCENT_SECRET_ID')
        self.secret_key = secret_key or os.getenv('TENCENT_SECRET_KEY')
        self.region = os.getenv('TENCENT_REGION', 'ap-guangzhou')
        self.service = 'tts'
        self.host = 'tts.tencentcloudapi.com'
        self.endpoint = f'https://{self.host}'
        
        # 腾讯云中文语音列表
        self.voices = {
            'xiaoyan': {
                'voice_type': 0,  # 标准音色
                'name': 'xiaoyan',
                'display_name': '小燕（女声）',
                'gender': 'Female'
            },
            'xiaoyou': {
                'voice_type': 1,  # 标准音色
                'name': 'xiaoyou',
                'display_name': '小游（童声）',
                'gender': 'Female'
            },
            'xiaoyao': {
                'voice_type': 2,  # 标准音色
                'name': 'xiaoyao',
                'display_name': '逍遥（男声）',
                'gender': 'Male'
            },
            'xiaoxi': {
                'voice_type': 4,  # 标准音色
                'name': 'xiaoxi',
                'display_name': '小希（女声）',
                'gender': 'Female'
            },
            'xiaonan': {
                'voice_type': 5,  # 标准音色
                'name': 'xiaonan',
                'display_name': '小南（男声）',
                'gender': 'Male'
            },
            'xiaochen': {
                'voice_type': 6,  # 标准音色
                'name': 'xiaochen',
                'display_name': '小晨（女声）',
                'gender': 'Female'
            },
            'xiaojing': {
                'voice_type': 1001,  # 精品音色
                'name': 'xiaojing',
                'display_name': '小婧（女声）',
                'gender': 'Female'
            },
            'xiaomei': {
                'voice_type': 1002,  # 精品音色
                'name': 'xiaomei',
                'display_name': '小美（女声）',
                'gender': 'Female'
            },
            'xiaoyu': {
                'voice_type': 1003,  # 精品音色
                'name': 'xiaoyu',
                'display_name': '小宇（男声）',
                'gender': 'Male'
            },
            'xiaoyue': {
                'voice_type': 1004,  # 精品音色
                'name': 'xiaoyue',
                'display_name': '小悦（女声）',
                'gender': 'Female'
            },
            'xiaolin': {
                'voice_type': 1005,  # 精品音色
                'name': 'xiaolin',
                'display_name': '小琳（女声）',
                'gender': 'Female'
            },
            'xiaowu': {
                'voice_type': 1007,  # 精品音色
                'name': 'xiaowu',
                'display_name': '小武（男声）',
                'gender': 'Male'
            }
        }
    
    def _sign(self, params: dict) -> str:
        """生成签名"""
        # 1. 拼接规范请求串
        http_request_method = 'POST'
        canonical_uri = '/'
        canonical_querystring = ''
        
        # 头部信息
        timestamp = str(int(time.time()))
        date = time.strftime('%Y-%m-%d', time.gmtime())
        
        payload = json.dumps(params)
        payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        canonical_headers = f'content-type:application/json\nhost:{self.host}\n'
        signed_headers = 'content-type;host'
        
        canonical_request = (http_request_method + '\n' +
                           canonical_uri + '\n' +
                           canonical_querystring + '\n' +
                           canonical_headers + '\n' +
                           signed_headers + '\n' +
                           payload_hash)
        
        # 2. 拼接待签名字符串
        algorithm = 'TC3-HMAC-SHA256'
        credential_scope = date + '/tts/tc3_request'
        
        string_to_sign = (algorithm + '\n' +
                         timestamp + '\n' +
                         credential_scope + '\n' +
                         hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())
        
        # 3. 计算签名
        secret_date = hmac.new(('TC3' + self.secret_key).encode('utf-8'),
                              date.encode('utf-8'), hashlib.sha256).digest()
        secret_service = hmac.new(secret_date, self.service.encode('utf-8'),
                                 hashlib.sha256).digest()
        secret_signing = hmac.new(secret_service, 'tc3_request'.encode('utf-8'),
                                 hashlib.sha256).digest()
        signature = hmac.new(secret_signing, string_to_sign.encode('utf-8'),
                            hashlib.sha256).hexdigest()
        
        # 4. 拼接 Authorization
        authorization = (algorithm + ' ' +
                        'Credential=' + self.secret_id + '/' + credential_scope + ', ' +
                        'SignedHeaders=' + signed_headers + ', ' +
                        'Signature=' + signature)
        
        return authorization, timestamp
    
    def synthesize(self, text: str, voice_id: str = 'xiaoyan',
                   output_path: Optional[str] = None) -> str:
        """
        合成语音
        
        Args:
            text: 要合成的文本（最长600字符）
            voice_id: 声音ID
            output_path: 输出路径
        
        Returns:
            输出文件路径
        """
        if not self.secret_id or not self.secret_key:
            raise ValueError("腾讯云 SecretId 和 SecretKey 未配置")
        
        if not output_path:
            import tempfile
            output_path = tempfile.mktemp(suffix='.mp3')
        
        # 获取声音配置
        voice_config = self.voices.get(voice_id, self.voices['xiaoyan'])
        
        # 准备请求参数
        params = {
            'Text': text,
            'SessionId': str(int(time.time())),
            'ModelType': 1,  # 长文本模型
            'VoiceType': voice_config['voice_type'],
            'Volume': 0,  # 音量 [-10, 10]
            'Speed': 0,   # 语速 [-2, 2]
        }
        
        # 生成签名
        authorization, timestamp = self._sign(params)
        
        # 发送请求
        headers = {
            'Content-Type': 'application/json',
            'Host': self.host,
            'X-TC-Action': 'TextToVoice',
            'X-TC-Version': '2019-08-23',
            'X-TC-Timestamp': timestamp,
            'X-TC-Region': self.region,
            'Authorization': authorization
        }
        
        response = requests.post(self.endpoint, 
                                headers=headers, 
                                json=params,
                                timeout=30)
        
        response_data = response.json()
        
        if 'Response' in response_data and 'Audio' in response_data['Response']:
            # 解码Base64音频数据
            audio_data = base64.b64decode(response_data['Response']['Audio'])
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            return output_path
        else:
            error = response_data.get('Response', {}).get('Error', {})
            raise Exception(f"腾讯云TTS错误: {error}")
    
    def get_voices(self) -> List[Dict]:
        """获取可用声音列表"""
        voices = []
        for key, voice in self.voices.items():
            voices.append({
                'id': key,
                'name': voice['display_name'],
                'gender': voice['gender'],
                'language': 'zh-CN',
                'provider': 'tencent'
            })
        return voices

# 角色声音映射
CHARACTER_VOICE_MAP_TENCENT = {
    '旁白': 'xiaoyan',
    '陈平安': 'xiaowu',      # 男声
    '宁姚': 'xiaomei',       # 女声
    '老人': 'xiaoyao',       # 成熟男声
    '爷爷': 'xiaoyao',
    '男主角': 'xiaowu',
    '女主角': 'xiaomei',
    '男': 'xiaowu',
    '女': 'xiaoyan',
    'default': 'xiaoyan'
}

def get_tencent_voice_for_character(character_name: str) -> str:
    """根据角色名获取腾讯云推荐声音"""
    for key, voice in CHARACTER_VOICE_MAP_TENCENT.items():
        if key in character_name:
            return voice
    return 'default'

# 测试代码
if __name__ == '__main__':
    # 测试（需要配置密钥）
    tts = TencentCloudTTS()
    
    print("腾讯云可用声音列表：")
    for voice in tts.get_voices()[:5]:
        print(f"  - {voice['name']} ({voice['id']})")
    
    # 如果有密钥，测试合成
    if tts.secret_id and tts.secret_key:
        print("\n测试语音合成...")
        test_text = "你好，这是腾讯云语音合成测试。"
        try:
            output_file = tts.synthesize(test_text, 'xiaoyan')
            print(f"已生成: {output_file}")
        except Exception as e:
            print(f"合成失败: {e}")
    else:
        print("\n未配置腾讯云密钥，跳过测试")
