# 测试 OpenAI API 连接
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key 已配置: {'是' if api_key else '否'}")
print(f"API Key 前10位: {api_key[:10]}..." if api_key else "")

# 测试 API 调用
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    # 简单的测试请求
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个 helpful assistant."},
            {"role": "user", "content": "你好，请用一句话介绍自己"}
        ],
        max_tokens=50
    )
    
    print("\n✅ API 测试成功！")
    print(f"回复: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ API 测试失败: {e}")
