#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《剑来》第一章有声书生成脚本
使用 Edge TTS（免费，国内可用）
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.text_parser import TextParser
from app.services.character_recognizer import CharacterRecognizer
from app.services.voice_synthesizer import VoiceSynthesizer

def main():
    print("=" * 70)
    print("《剑来》第一章 - 有声书生成")
    print("=" * 70)
    
    # 1. 读取文本
    print("\n[1/4] 读取文本...")
    text_file = os.path.join(os.path.dirname(__file__), 'backend', 'test_book.txt')
    
    if not os.path.exists(text_file):
        print(f"错误: 找不到文件 {text_file}")
        return
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"✓ 文本长度: {len(text)} 字符")
    
    # 2. 识别角色
    print("\n[2/4] 识别角色...")
    recognizer = CharacterRecognizer()
    characters = recognizer.recognize(text)
    
    print(f"✓ 识别到 {len(characters)} 个角色:")
    for char in characters:
        print(f"  - {char['name']}: {char['description']} (对话: {char['dialogue_count']}次)")
    
    # 3. 分段文本
    print("\n[3/4] 分段文本...")
    segments = recognizer.segment_by_speaker(text)
    print(f"✓ 分成 {len(segments)} 个片段")
    
    # 显示前5个片段
    print("\n片段预览:")
    for i, seg in enumerate(segments[:5], 1):
        preview = seg['text'][:40] + "..." if len(seg['text']) > 40 else seg['text']
        print(f"  [{i}] {seg['speaker']}: {preview}")
    
    # 4. 生成有声书
    print("\n[4/4] 生成有声书...")
    print("注意: 使用 Edge TTS（免费，国内可用）")
    print("正在生成音频，请稍候...\n")
    
    # 创建输出目录
    output_dir = os.path.expanduser("~/Desktop/Audiobook_Output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "剑来_第一章_惊蛰.mp3")
    
    try:
        # 初始化语音合成器
        synthesizer = VoiceSynthesizer()
        
        # 生成有声书
        result_path = synthesizer.synthesize_audiobook(segments, output_file)
        
        print("\n" + "=" * 70)
        print("✓ 有声书生成成功！")
        print("=" * 70)
        print(f"\n文件位置: {result_path}")
        print(f"文件大小: {os.path.getsize(result_path) / 1024 / 1024:.2f} MB")
        
        # 生成说明文件
        readme_path = os.path.join(output_dir, "有声书说明.txt")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("《剑来》第一章 - 有声书\n")
            f.write("=" * 70 + "\n\n")
            f.write("生成信息:\n")
            f.write(f"- 文件名: 剑来_第一章_惊蛰.mp3\n")
            f.write(f"- 片段数: {len(segments)}\n")
            f.write(f"- 角色数: {len(characters)}\n")
            f.write(f"- 使用服务: Edge TTS（免费）\n\n")
            f.write("角色配音:\n")
            for char in characters:
                f.write(f"- {char['name']}: {char['description']}\n")
        
        print(f"说明文件: {readme_path}")
        
    except Exception as e:
        print(f"\n✗ 生成失败: {e}")
        print("\n可能的原因:")
        print("1. 未安装 edge-tts: pip install edge-tts")
        print("2. 网络连接问题")
        print("3. 文本过长")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
    input("\n按回车键退出...")
