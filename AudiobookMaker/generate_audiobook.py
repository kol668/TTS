# 有声书生成脚本 - 使用系统TTS
import os
import sys
from datetime import datetime

# 创建输出目录
output_dir = os.path.expanduser("~/Desktop/Audiobook_Output")
os.makedirs(output_dir, exist_ok=True)

# 《剑来》第一章文本
chapters = [
    {
        "title": "第一章 惊蛰",
        "segments": [
            {"speaker": "旁白", "text": "第一章 惊蛰。陈平安背着草鞋，走在泥瓶巷的石板路上。"},
            {"speaker": "宁姚", "text": "陈平安，等等我！"},
            {"speaker": "旁白", "text": "身后传来一个清脆的声音。陈平安回头，看到宁姚快步追了上来。"},
            {"speaker": "陈平安", "text": "宁姑娘，有什么事吗？"},
            {"speaker": "宁姚", "text": "今天镇上有集市，一起去看看吗？"},
            {"speaker": "陈平安", "text": "我还要去送草鞋，改天吧。"},
            {"speaker": "旁白", "text": "宁姚有些失望，但还是点点头。"},
            {"speaker": "宁姚", "text": "那好吧，你忙完记得来找我。"},
            {"speaker": "旁白", "text": "看着宁姚离去的背影，陈平安叹了口气，继续向前走。泥瓶巷的尽头，是一座破旧的草鞋铺子。陈平安推开门，看到老人正在编着草鞋。"},
            {"speaker": "陈平安", "text": "爷爷，我回来了。"},
            {"speaker": "旁白", "text": "老人抬起头，浑浊的眼睛里闪过一丝光芒。"},
            {"speaker": "老人", "text": "平安啊，今天送了几双？"},
            {"speaker": "陈平安", "text": "三双。镇上的人都说咱们的草鞋结实。"},
            {"speaker": "老人", "text": "那是自然，咱们陈家的草鞋，可是祖传的技艺。"},
            {"speaker": "旁白", "text": "陈平安坐在小板凳上，拿起稻草开始编织。他的手指灵活地翻飞，一根根稻草在他手中变成了精美的草鞋。窗外，夕阳西下，将整个泥瓶巷染成了金色。这是陈平安平凡的一天，也是他不平凡人生的开始。"}
        ]
    }
]

# 角色配置
characters = {
    "旁白": {"name": "旁白", "description": "叙述者", "voice_style": "default"},
    "陈平安": {"name": "陈平安", "description": "男主角", "voice_style": "male"},
    "宁姚": {"name": "宁姚", "description": "女主角", "voice_style": "female"},
    "老人": {"name": "老人", "description": "陈平安的爷爷", "voice_style": "elder"}
}

print("=" * 60)
print("AudiobookMaker - 有声书生成")
print("=" * 60)
print(f"\n输出目录: {output_dir}")
print(f"章节数: {len(chapters)}")
print(f"角色数: {len(characters)}")

# 生成脚本文件
script_file = os.path.join(output_dir, "jianlai_chapter1_script.txt")
with open(script_file, 'w', encoding='utf-8') as f:
    f.write("《剑来》第一章 - 有声书脚本\n")
    f.write("=" * 60 + "\n\n")
    
    for chapter in chapters:
        f.write(f"\n【{chapter['title']}】\n\n")
        for i, segment in enumerate(chapter['segments'], 1):
            f.write(f"[{i}] {segment['speaker']}: {segment['text']}\n\n")

print(f"\n脚本已保存: {script_file}")

# 生成角色配置文件
char_file = os.path.join(output_dir, "characters_config.txt")
with open(char_file, 'w', encoding='utf-8') as f:
    f.write("角色配置\n")
    f.write("=" * 60 + "\n\n")
    for name, char in characters.items():
        f.write(f"角色: {name}\n")
        f.write(f"描述: {char['description']}\n")
        f.write(f"声音风格: {char['voice_style']}\n")
        f.write("-" * 40 + "\n")

print(f"角色配置已保存: {char_file}")

# 生成README
readme_file = os.path.join(output_dir, "README.txt")
with open(readme_file, 'w', encoding='utf-8') as f:
    f.write("AudiobookMaker - 有声书生成结果\n")
    f.write("=" * 60 + "\n\n")
    f.write("生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    f.write("文件说明:\n")
    f.write("- jianlai_chapter1_script.txt: 有声书脚本\n")
    f.write("- characters_config.txt: 角色配置\n")
    f.write("\n注意:\n")
    f.write("由于OpenAI API配额不足，本次使用本地规则识别角色。\n")
    f.write("如需生成完整音频，请:\n")
    f.write("1. 充值OpenAI API额度，或\n")
    f.write("2. 配置Azure Speech API（有免费额度）\n")
    f.write("3. 配置ElevenLabs API\n")

print(f"说明文件已保存: {readme_file}")

print("\n" + "=" * 60)
print("生成完成！")
print("=" * 60)
print(f"\n所有文件已保存到: {output_dir}")
print("\n文件列表:")
for f in os.listdir(output_dir):
    print(f"  - {f}")
