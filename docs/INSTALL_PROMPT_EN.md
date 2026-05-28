# AI Install Prompt (English)

Copy-paste this into any AI coding assistant (DeepSeek, GLM, Claude, GPT, Gemini, ...) and it will set up `deepseek-eyes` for you end-to-end.

---

```
You are going to install and configure the `deepseek-eyes` MCP server on my machine
so that I can paste screenshots in my MCP-capable coding client (Opencode, Claude Code,
Cursor, Cline, Continue, ...) and have text-only models see them via Qwen-VL + ModelScope.

Repository: https://github.com/290298661-pixel/deepseek-eyes

Steps to follow:

1. Check Python 3.10+ is available.

2. Clone the repo and run `pip install -e .` inside a venv.

3. Help me get a ModelScope API key:
   - URL: https://modelscope.cn → Login → Profile → Access Token
   - Free, 500 calls/day, no credit card.

4. Detect which MCP client I'm using, add a `deepseek-eyes` entry
   with the venv Python path, `-m deepseek_eyes`, and `MODELSCOPE_API_KEY`.

5. Verify: run `python -m deepseek_eyes` — should stay idle on stdin.
```
