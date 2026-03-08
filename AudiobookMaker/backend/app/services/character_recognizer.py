import os
import re
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class CharacterRecognizer:
    """角色识别器 - 支持AI识别和本地规则识别"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_ai = bool(self.openai_api_key)
    
    def recognize(self, text: str) -> List[Dict]:
        """识别文本中的角色"""
        # 使用本地规则识别
        characters = self._rule_based_recognize(text)
        
        # 如果配置了OpenAI且额度充足，可以尝试AI识别
        if self.use_ai and len(text) > 100:
            try:
                ai_characters = self._ai_recognize(text[:3000])
                # 合并AI识别的结果
                for char in ai_characters:
                    if char['name'] not in [c['name'] for c in characters]:
                        characters.append(char)
            except Exception as e:
                print(f"AI识别失败（可能是配额不足）: {e}")
                print("使用本地规则识别结果")
        
        # 确保至少有旁白
        if not characters:
            characters.append({
                'name': '旁白',
                'description': '叙述者',
                'dialogue_count': 0
            })
        
        return characters
    
    def _rule_based_recognize(self, text: str) -> List[Dict]:
        """基于规则的角色识别（不依赖API）"""
        characters = {}
        lines = text.split('\n')
        
        # 常见的角色指示词
        dialogue_indicators = ['说', '道', '问', '答', '喊', '叫', '念', '讲']
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 查找对话（引号内的内容）
            dialogue_pattern = r'["""]([^"""]+)["""]|「([^」]+)」'
            dialogues = re.findall(dialogue_pattern, line)
            
            if dialogues:
                # 提取说话人
                speaker = self._extract_speaker(line, dialogues[0][0] or dialogues[0][1])
                
                if speaker:
                    if speaker not in characters:
                        characters[speaker] = {
                            'name': speaker,
                            'description': self._guess_character_type(speaker),
                            'dialogue_count': 0
                        }
                    characters[speaker]['dialogue_count'] += len(dialogues)
        
        # 添加旁白
        characters['旁白'] = {
            'name': '旁白',
            'description': '叙述者，负责场景描述和背景介绍',
            'dialogue_count': 0
        }
        
        return list(characters.values())
    
    def _extract_speaker(self, line: str, dialogue: str) -> str:
        """从对话行提取说话人"""
        # 去除对话内容
        parts = line.split(f'"{dialogue}"')
        if len(parts) < 2:
            parts = line.split(f'「{dialogue}」')
        
        before_dialogue = parts[0].strip() if parts else ""
        
        # 常见的说话人标记模式
        patterns = [
            r'(.+?)[说道问答喊叫念讲]',
            r'(.+?):',
            r'(.+?)：',
            r'(.+?)[,，]',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, before_dialogue)
            if match:
                speaker = match.group(1).strip()
                # 清理说话人名称
                speaker = re.sub(r'[\s"""「」]', '', speaker)
                # 过滤掉过长或过短的
                if 1 < len(speaker) < 15 and not speaker.isdigit():
                    return speaker
        
        # 如果没有找到，尝试提取前面的名词
        words = before_dialogue.split()
        if words:
            last_word = words[-1].strip('，。！？"""「」')
            if 1 < len(last_word) < 10 and not last_word.isdigit():
                return last_word
        
        return None
    
    def _guess_character_type(self, name: str) -> str:
        """猜测角色类型"""
        # 基于名字猜测角色类型
        male_indicators = ['陈', '李', '王', '张', '刘', '杨', '赵', '黄', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗', '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹', '彭', '曾', '肖', '田', '董', '袁', '潘', '于', '蒋', '蔡', '余', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈', '姚', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金', '石', '廖', '贾', '夏', '韦', '付', '方', '白', '邹', '孟', '熊', '秦', '邱', '江', '尹', '薛', '闫', '段', '雷', '侯', '龙', '史', '陶', '黎', '贺', '顾', '毛', '郝', '龚', '邵', '万', '钱', '严', '覃', '武', '戴', '莫', '孔', '向', '汤']
        female_indicators = ['娜', '婷', '丽', '敏', '静', '秀', '娟', '艳', '燕', '芳', '玲', '红', '梅', '莉', '颖', '雪', '雯', '霞', '兰', '洁', '云', '凤', '琳', '华', '晶', '薇', '珍', '琴', '萍', '荣', '英', '佳', '玲', '茜', '倩', '菲', '妍', '嫣', '妮', '璐', '琪', '瑶', '珊', '妙', '姝', '婉', '娴', '婷', '妍', '嫣', '妮', '璐', '琪', '瑶', '珊', '妙', '姝', '婉', '娴']
        
        if any(name.endswith(ind) for ind in female_indicators):
            return "女性角色"
        elif any(name.startswith(ind) for ind in male_indicators):
            return "男性角色"
        else:
            return "角色"
    
    def _ai_recognize(self, text: str) -> List[Dict]:
        """使用AI识别角色（需要API配额）"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
请分析以下小说文本，识别出所有角色。
对于每个角色，提供名字和简短描述。
只返回JSON格式，不要其他文字。

文本：
{text[:2000]}

格式：
[{{"name": "角色名", "description": "描述"}}]
"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            content = response.choices[0].message.content
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                characters = json.loads(json_match.group())
                for char in characters:
                    char['dialogue_count'] = 0
                return characters
        except Exception as e:
            print(f"AI识别错误: {e}")
        
        return []
    
    def segment_by_speaker(self, text: str) -> List[Dict]:
        """按说话人分段文本"""
        segments = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 识别对话
            dialogue_pattern = r'["""]([^"""]+)["""]|「([^」]+)」'
            dialogue_matches = list(re.finditer(dialogue_pattern, line))
            
            if dialogue_matches:
                for match in dialogue_matches:
                    dialogue = match.group(1) or match.group(2)
                    speaker = self._extract_speaker(line, dialogue) or "未知角色"
                    segments.append({
                        'speaker': speaker,
                        'text': dialogue,
                        'type': 'dialogue'
                    })
            else:
                # 旁白
                segments.append({
                    'speaker': '旁白',
                    'text': line,
                    'type': 'narration'
                })
        
        return segments
