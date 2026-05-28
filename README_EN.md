# clipboard-vision-mcp

> 🇫🇷 **[Version française disponible → README.fr.md](README.fr.md)**

> Add vision to text-only models in Opencode (**DeepSeek V4**, **GLM 5.1**) — **see the image in your clipboard directly**, no manual file saving.

**Tested on Windows 11 + Opencode + DeepSeek V4 Pro.** Multi-OS clipboard support (Windows / macOS / Linux X11 / Linux Wayland).

Forked from [itcomgroup/vision-mcp-server](https://github.com/itcomgroup/vision-mcp-server) — rewritten around clipboard-first tools, security hardening, cross-platform clipboard extraction, and one-prompt AI install.

---

## The problem

Cheap/fast text-only models like **DeepSeek V4** and **GLM 5.1** are great for code, but they cannot read images. Every time you paste a screenshot, the model asks you to save it to disk and provide a path.

## The fix

This MCP server exposes `*_from_clipboard` tools. When the LLM needs to see your screenshot, it calls `analyze_clipboard` — the server reads the clipboard image, sends it to a real vision model (**Groq + Llama-4 Scout, free tier**), and returns a text description the text model can reason about.

Result: **paste → ask → done.** No file shuffling.

---

## 🤖 One-prompt install via AI (recommended)

Instead of running the steps below manually, paste one of these prompts into any coding assistant (DeepSeek, GLM, Claude, GPT, ...) and it will set everything up for you end-to-end — clone, venv, deps, MCP config, keybindings:

- 🇬🇧 **[docs/INSTALL_PROMPT_EN.md](docs/INSTALL_PROMPT_EN.md)**
- 🇫🇷 **[docs/INSTALL_PROMPT_FR.md](docs/INSTALL_PROMPT_FR.md)**

Prefer doing it yourself? Keep reading.

---

## Features

- 🖼️ **Clipboard-first** — `analyze_clipboard`, `extract_text_from_clipboard`, `diagnose_error_from_clipboard`, `describe_ui_from_clipboard`, `code_from_clipboard`.
- 📁 **File path fallback** — same tools available for images already on disk.
- 🆓 **Free vision backend** — Groq's free tier with Llama-4 Scout (17B, multimodal).
- 🖥️ **Multi-OS** — Windows, macOS, Linux (X11 + Wayland).
- 🔒 **Security hardened** — extension/size/magic-byte validation, auto-delete of clipboard temp files after analysis.
- 🔌 **MCP standard** — works with Opencode, Claude Code, Cursor, Cline, Continue, or any MCP-capable client.

---

## Requirements

- **Python 3.10+**
- **Groq API key** (free, 30 seconds sign-up): https://console.groq.com/keys
- An MCP-capable client (Opencode, Claude Code, Cursor, Cline, Continue, ...)

### Python dependencies (installed automatically via `pip install -e .`)

| Package | Purpose |
|---|---|
| `mcp>=1.0.0` | MCP protocol server |
| `groq>=0.11.0` | Groq API client (Llama-4 Scout vision) |
| `aiofiles>=23.0.0` | Async file I/O |
| `Pillow>=10.0.0` | Clipboard image extraction (Windows/macOS), PNG encoding |

### OS-specific clipboard dependencies

| OS | Command | Why |
|---|---|---|
| **Windows** | *nothing extra* | Pillow + pywin32 handle the clipboard natively. |
| **macOS** | `brew install pngpaste` *(optional fallback)* | Pillow works in most cases; pngpaste as backup. |
| **Linux — Wayland** | `sudo apt install wl-clipboard` | Provides `wl-paste`. |
| **Linux — X11** | `sudo apt install xclip` | Or your distro equivalent. |

---

## Quick start

### 1. Get a free Groq API key
https://console.groq.com/keys

### 2. Install

```bash
git clone https://github.com/Capetlevrai/clipboard-vision-mcp.git
cd clipboard-vision-mcp
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -e .
```

### 3. Smoke test (no Groq needed)

Copy any screenshot, then:

```bash
python examples/smoke_test.py
```

Expected: `OK: clipboard image saved to <path>`.

### 4. Wire to your MCP client

See [docs/OPENCODE.md](docs/OPENCODE.md) for Opencode (Windows-tested) or [docs/CLIENTS.md](docs/CLIENTS.md) for Claude Code / Cursor / Cline / Continue.

**Opencode** (`%APPDATA%\opencode\opencode.json` on Windows, `~/.config/opencode/opencode.json` on Linux/macOS):

```json
{
  "mcp": {
    "clipboard-vision": {
      "type": "local",
      "command": [
        "C:\\path\\to\\clipboard-vision-mcp\\.venv\\Scripts\\python.exe",
        "-m",
        "clipboard_vision_mcp"
      ],
      "enabled": true,
      "environment": {
        "GROQ_API_KEY": "gsk_your_key_here"
      }
    }
  }
}
```

> 💡 **Use the absolute path to the venv's Python.** This guarantees the MCP starts with the right dependencies regardless of shell, cwd, or active venv.

### 5. ⚠️ Opencode keybindings for pasting images

Opencode does **not** bind image-paste to `Ctrl+V` / `Alt+V` by default. Without this step, copying a screenshot and hitting paste will insert nothing (or plain text).

Edit your Opencode `keybinds.json` or the `keybinds` section of `opencode.json`:

```json
{
  "keybinds": {
    "input_paste": "ctrl+v",
    "input_paste_image": "alt+v"
  }
}
```

Restart Opencode after editing.

### 6. Does it auto-start after a Windows reboot?

**Yes.** Opencode re-reads `opencode.json` at every launch and auto-spawns any MCP server with `"type": "local"` and `"enabled": true`. Because the command uses the **absolute path to the venv's Python**, it doesn't matter which shell or working directory Opencode is launched from.

Reboot → open Opencode → `clipboard-vision` tools are listed. No manual step.

---

## Usage

```
You: (copy a screenshot to clipboard, then type)
     "Look at what I just copied and tell me what's wrong with this error."

LLM (DeepSeek, GLM, Claude, ...): [calls diagnose_error_from_clipboard]
     → "The error says `ECONNREFUSED 127.0.0.1:5432`. Postgres isn't
        running on port 5432. Start it with: ..."
```

The text-only model never sees pixels — it reads the description returned by Llama-4 Scout and reasons over it.

### Tool reference

| Tool | Input | Use when |
|---|---|---|
| `analyze_clipboard` | optional `prompt` | Generic description, Q&A on the clipboard image. |
| `extract_text_from_clipboard` | — | Pure OCR. |
| `describe_ui_from_clipboard` | — | UI/UX review, component inventory. |
| `diagnose_error_from_clipboard` | — | Error screenshot → cause + fix. |
| `code_from_clipboard` | — | Extract code from a screenshot. |
| `analyze_image` | `image_path`, optional `prompt` | Image already on disk. |
| `extract_text`, `describe_ui`, `diagnose_error`, `understand_diagram`, `analyze_chart`, `code_from_screenshot` | `image_path` | Same as above for files. |

---

## Security

This server runs as a **local stdio process** — it does not open any network port and only talks to the MCP client over stdin/stdout and to the Groq API over HTTPS.

Hardening in place:

- **File type allow-list.** `analyze_image` and the other file-path tools only accept `.png .jpg .jpeg .gif .webp .bmp`. This prevents a prompt-injected LLM from asking the server to read arbitrary local files (`~/.ssh/id_rsa`, `.env`, ...) and exfiltrate them as base64 to Groq.
- **Magic-byte check.** File content is validated against known image headers before upload.
- **Size cap.** 20 MB max per image.
- **Auto-delete clipboard temp files** after each analysis. Screenshots may contain secrets (tokens, chats, credentials) — the server writes them to `$TMPDIR/clipboard_vision_mcp/` and unlinks them on completion.
- **No telemetry.** No analytics, no phone-home.

### What this project cannot protect you from

- **Your API key lives in your MCP client config in plain text.** That is how MCP clients work today. Keep that config file non-world-readable and never commit it. If you accidentally expose a key (chat, screenshot, git push), **rotate it** at https://console.groq.com/keys.
- **Groq receives the images you analyze.** Check their [privacy policy](https://groq.com/privacy-policy/) before sending anything sensitive.
- **Any MCP tool is executed at the direction of the LLM.** If you connect a prompt-injected model to this server and feed it untrusted input, the model can choose what to analyze. The allow-list above reduces blast radius but cannot eliminate it.

### Found an issue?

Please open a [private security advisory](https://github.com/Capetlevrai/clipboard-vision-mcp/security/advisories/new) rather than a public issue.

---

## How it works

```
┌──────────────┐   MCP   ┌─────────────────┐   HTTPS   ┌─────────────────┐
│  Opencode    │ ──────▶ │  clipboard-     │ ────────▶ │  Groq API       │
│  (DeepSeek)  │         │  vision-mcp     │           │  Llama-4 Scout  │
└──────────────┘         └─────────────────┘           └─────────────────┘
                              │
                              ▼
                     reads system clipboard
                     (PIL / wl-paste / xclip)
                     → validate → base64 → send → delete
```

---

## Troubleshooting

- **"Clipboard does not contain an image."** — Copy an actual image, not a file icon or text. On Linux, verify `wl-paste --type image/png` or `xclip -selection clipboard -t image/png -o | file -` works outside the MCP.
- **"GROQ_API_KEY is not set."** — Check the `environment` block in your client config, then **fully restart** the client.
- **Tools don't appear in Opencode.** — Check Opencode's MCP logs. Run `python -m clipboard_vision_mcp` manually — it should start and wait silently on stdin.
- **"Refusing to read '<ext>' — only image files are allowed."** — You (or the LLM) passed a non-image path. This is the security guard doing its job.

---

## Credits

- Forked from [itcomgroup/vision-mcp-server](https://github.com/itcomgroup/vision-mcp-server) — original Groq + Llama-4 Scout MCP integration.
- Vision model: [Llama-4 Scout 17B](https://groq.com/) served by Groq.

## License

MIT — see [LICENSE](LICENSE).
