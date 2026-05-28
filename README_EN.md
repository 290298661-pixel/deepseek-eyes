# deepseek-eyes 👁️

> Give DeepSeek the ability to see. Screenshot → clipboard → Qwen-VL → text → your text-only model can "see" images.

[中文 README](README.md) | [Install Prompt](docs/INSTALL_PROMPT_EN.md) | [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## Quick Start

```bash
git clone https://github.com/290298661-pixel/deepseek-eyes.git
cd deepseek-eyes
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -e .

# Get a free API key (2000 calls/day, 500 per model):
# ① https://modelscope.cn → Register/Login
# ② Avatar → Profile → Access Token
#    or directly: https://modelscope.cn/my/myaccesstoken
# ③ First time: bind your Alibaba Cloud account (required)
# ④ "Create Access Token" → name it → generate → copy
# ⑤ Token format: ms-xxxxxxxxxxxx → remove the ms- prefix!

## Why?

Text-only models like **DeepSeek V4** and **GLM 5.1** have no vision capability. Paste a screenshot and they can't see it.

**deepseek-eyes** bridges this gap — an MCP server that reads your clipboard image, sends it to Qwen-VL (a powerful vision model via ModelScope), and returns a text description your LLM can reason about.

## How It Works

```
Claude Code / Opencode (DeepSeek API)
        │  MCP
        ▼
deepseek-eyes (Python MCP Server)
        │
        ├── reads system clipboard (PIL)
        ├── encodes image as base64
        ├── sends to Qwen-VL via ModelScope API
        ├── returns text description
        └── deletes temp file
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `analyze_clipboard` | Analyze image in system clipboard |
| `extract_text_from_clipboard` | OCR text from clipboard image |
| `describe_ui_from_clipboard` | Describe UI layout from clipboard |
| `diagnose_error_from_clipboard` | Diagnose error screenshot from clipboard |
| `code_from_clipboard` | Extract code from clipboard screenshot |
| `analyze_image` | Analyze image file on disk |
| `extract_text` | OCR image file |
| `describe_ui` | Describe UI screenshot file |
| `diagnose_error` | Diagnose error screenshot file |
| `understand_diagram` | Interpret diagram/flowchart |
| `analyze_chart` | Analyze data chart |
| `code_from_screenshot` | Extract code from screenshot file |

## Client Configuration

**Claude Code** (`.claude/settings.json`):

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "ABSOLUTE_PATH\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": { "MODELSCOPE_API_KEY": "your_key" }
    }
  }
}
```

## Security

- Runs as local stdio process — no network ports exposed
- Clipboard temp files auto-deleted after analysis
- Image-only allowlist prevents arbitrary file reads
- 20 MB size limit, magic-byte validation

## Credits

Forked from [Capetlevrai/clipboard-vision-mcp](https://github.com/Capetlevrai/clipboard-vision-mcp) (MIT). Vision backend replaced with Qwen-VL via ModelScope. Full Chinese localization added.

## License

MIT © Shaohan He
