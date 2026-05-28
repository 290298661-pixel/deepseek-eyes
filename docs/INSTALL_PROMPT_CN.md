# AI 安装提示词 / AI Install Prompt

把下面的提示词直接粘贴给 Claude Code / DeepSeek / ChatGPT，让它帮你完成 deepseek-eyes 的安装和配置。

---

## 🇨🇳 中文（推荐）

```
请帮我安装 deepseek-eyes，这是一个为 DeepSeek 等无视觉能力的模型
提供图片理解能力的 MCP 服务器（使用通义千问VL + 剪贴板）。

安装步骤：

1. 克隆仓库：
   git clone https://github.com/290298661-pixel/deepseek-eyes.git
   cd deepseek-eyes

2. 创建虚拟环境并安装：
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. 获取 ModelScope API Key（免费，每天500次）：
   打开浏览器访问 https://modelscope.cn
   登录 → 右上角头像 → 个人中心 → 访问令牌 → 创建令牌
   复制生成的 API Key

4. 测试剪贴板是否正常：
   复制一张图片到剪贴板（可以按 Win+Shift+S 截图）
   运行 python examples/smoke_test.py
   应该看到 "✅ 成功" 的输出

5. 配置 Claude Code 的 MCP：
   在项目的 .claude/settings.json 中添加：

   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "完整的deepseek-eyes目录路径\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "步骤3获取的API Key"
         }
       }
     }
   }

   注意：command 必须使用 venv 中 Python 的绝对路径！

6. 重启 Claude Code，然后测试：
   按 Win+Shift+S 截图，Ctrl+C 复制
   在对话框中粘贴截图，然后输入："analyze_clipboard 看看这是什么"
```

---

## 🇬🇧 English

```
Please help me install deepseek-eyes, an MCP server that adds vision
capabilities to text-only models (DeepSeek, GLM, etc.) by reading
clipboard images and analyzing them with Qwen-VL via ModelScope.

Installation steps:

1. Clone the repo:
   git clone https://github.com/290298661-pixel/deepseek-eyes.git
   cd deepseek-eyes

2. Create venv and install:
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. Get ModelScope API Key (free, 500 calls/day):
   Visit https://modelscope.cn
   Login → Profile → Access Token → Create Token
   Copy the API Key

4. Test clipboard:
   Copy an image to clipboard (Win+Shift+S to screenshot)
   Run: python examples/smoke_test.py
   Should see "OK: clipboard image saved to..."

5. Configure Claude Code MCP in .claude/settings.json:

   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "ABSOLUTE_PATH\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "your_api_key_from_step_3"
         }
       }
     }
   }

   Use the absolute path to the venv's Python!

6. Restart Claude Code and test:
   Take a screenshot, copy it to clipboard
   Ask: "analyze_clipboard - what's in this image?"
```
