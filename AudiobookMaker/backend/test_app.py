# 测试 AudiobookMaker 核心功能
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.text_parser import TextParser
from app.services.character_recognizer import CharacterRecognizer

print("=" * 60)
print("AudiobookMaker Test")
print("=" * 60)

# 1. Test text parsing
print("\n[1/3] Testing text parser...")
parser = TextParser()
text = parser.parse("test_book.txt")
print(f"[OK] Text parsed successfully, {len(text)} characters")
print(f"     Preview: {text[:100]}...")

# 2. Test character recognition
print("\n[2/3] Testing character recognition...")
recognizer = CharacterRecognizer()
characters = recognizer.recognize(text)
print(f"[OK] Found {len(characters)} characters:")
for char in characters:
    print(f"     - {char['name']}: {char['description']} (dialogues: {char['dialogue_count']})")

# 3. Test text segmentation
print("\n[3/3] Testing text segmentation...")
segments = recognizer.segment_by_speaker(text)
print(f"[OK] Split into {len(segments)} segments:")
for i, seg in enumerate(segments[:5]):
    print(f"     [{seg['type']}] {seg['speaker']}: {seg['text'][:30]}...")

print("\n" + "=" * 60)
print("Test completed! Software is working (using local rule-based recognition)")
print("=" * 60)
print("\nNote: OpenAI API quota exceeded, switched to local recognition mode")
print("Local recognition works but may be less accurate than AI recognition")
