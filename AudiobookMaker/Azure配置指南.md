# Azure Speech API 配置指南

## 免费额度
- 每月 50万字符免费
- 支持中文语音合成
- 多种声音可选

## 配置步骤

### 1. 注册 Azure 账户
1. 访问 https://azure.microsoft.com/zh-cn/free/
2. 使用微软账户登录
3. 新用户有 12个月免费试用 + 200美元额度

### 2. 创建 Speech 服务
1. 登录 Azure Portal: https://portal.azure.com
2. 点击 "创建资源" (Create a resource)
3. 搜索 "Speech" 或 "语音服务"
4. 点击 "创建" (Create)
5. 填写信息：
   - 订阅：选择你的订阅
   - 资源组：创建新的（如 "audiobook-rg"）
   - 区域：选择 "East Asia"（东亚）或 "China East 2"（中国东部2）
   - 名称：audiobook-speech
   - 定价层：选择 "Free F0"（免费层）
6. 点击 "审阅并创建" → "创建"

### 3. 获取 API 密钥
1. 等待部署完成，点击 "转到资源"
2. 在左侧菜单点击 "密钥和终结点" (Keys and Endpoint)
3. 复制以下信息：
   - KEY 1 或 KEY 2（任选一个）
   - 位置/区域（如 eastasia）

### 4. 配置到 AudiobookMaker
1. 打开文件 `backend/.env`
2. 填入以下信息：
```
OPENAI_API_KEY=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
ELEVENLABS_API_KEY=
AZURE_SPEECH_KEY=你的Azure密钥
AZURE_SPEECH_REGION=eastasia
DEBUG=True
```

### 5. 重启服务
1. 关闭之前的命令行窗口
2. 重新运行 `start.bat`

## Azure 中文语音列表

### 女声
- zh-CN-XiaoxiaoNeural - 晓晓（默认，自然女声）
- zh-CN-XiaoyiNeural - 晓伊（温柔女声）
- zh-CN-XiaochenNeural - 晓辰（活泼女声）
- zh-CN-XiaohanNeural - 晓涵（成熟女声）

### 男声
- zh-CN-YunxiNeural - 云希（年轻男声）
- zh-CN-YunjianNeural - 云健（成熟男声）
- zh-CN-YunxiaNeural - 云夏（少年男声）

### 老年声音
- zh-CN-YunxiNeural（调整语速和音调）

## 角色声音推荐配置

| 角色 | 推荐声音 | 说明 |
|------|----------|------|
| 旁白 | XiaoxiaoNeural | 自然女声，适合叙述 |
| 陈平安 | YunxiNeural | 年轻男声 |
| 宁姚 | XiaoyiNeural | 温柔女声 |
| 老人 | YunjianNeural | 成熟男声，可调整语速 |

## 故障排除

### 问题：API 返回 401 错误
解决：检查密钥是否正确复制，不要包含空格

### 问题：语音合成失败
解决：
1. 检查区域是否正确（如 eastasia）
2. 检查网络连接
3. 查看 Azure 配额使用情况

### 问题：声音不自然
解决：
- 使用 SSML 标签调整语速、音调
- 尝试不同的声音

## 监控使用情况
1. 登录 Azure Portal
2. 进入 Speech 资源
3. 点击 "监控" → "指标"
4. 查看 "Total Calls" 和 "Total Characters"

## 注意事项
- 免费层每月限制 50万字符
- 超出后会返回错误，需要等待下月重置或升级到付费层
- 建议定期检查使用情况
