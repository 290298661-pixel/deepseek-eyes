# deepseek-eyes 👁️

<p align="center">
  <b>给 DeepSeek 装上眼睛。</b><br>
  截图 → 剪贴板 → MCP → 通义千问VL → 文字描述 → DeepSeek 也能"看见"
</p>

<p align="center">
  <b><i>Give DeepSeek the ability to see.</i></b><br>
  <i>Screenshot → clipboard → Qwen-VL → text → your text-only model can "see"</i>
</p>

<p align="center">
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-为什么需要">为什么需要</a> ·
  <a href="#-工作原理">工作原理</a> ·
  <a href="#-客户端配置">客户端配置</a> ·
  <a href="README_EN.md">English</a>
</p>

---

## 🇨🇳 中文

### ⚡ 快速开始

```bash
# 1. 克隆
git clone https://github.com/290298661-pixel/deepseek-eyes.git
cd deepseek-eyes

# 2. 安装
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .

# 3. 获取免费 API Key
# 访问 https://modelscope.cn → 登录 → 个人中心 → 访问令牌 → 创建令牌

# 4. 测试剪贴板（复制一张图片后运行）
python examples/smoke_test.py
# 预期: ✅ 成功: 剪贴板图片已保存到 ...\clip_xxx.png

# 5. 配置 MCP 客户端（见下方）
```

### 🎯 为什么需要？

DeepSeek V4 / GLM 等文本模型的 API **没有视觉能力** ——你粘贴一张截图，它只能告诉你"我看见了文件路径"。

**deepseek-eyes** 填补了这个缺口：

```
你截了一张图
        │
        ▼
  ┌─────────────────┐
  │ deepseek-eyes    │
  │ 读取剪贴板图片    │
  │ → 发给通义千问VL  │
  │ → 返回文字描述   │
  └────────┬────────┘
           ▼
  DeepSeek: "这是一个登录页面，有用户名和密码两个输入框..."
```

**和同类工具的对比：**

| | deepseek-eyes | 原版 clipboard-vision-mcp | ErlichLiu/deepseek-vision |
|---|---|---|---|
| 视觉后端 | 通义千问VL | Groq（需翻墙） | 自选 |
| 免费额度 | 500次/天 | Groq 免费层 | 取决于后端 |
| 语言 | 🇨🇳 中文优先 | 英文 | 🇨🇳 中文 |
| 方式 | MCP stdio | MCP stdio | HTTP 代理 |

### 🔧 工作原理

```
┌──────────────────┐   MCP    ┌──────────────────┐   HTTPS   ┌───────────────────┐
│  Claude Code /    │ ──────▶ │  deepseek-eyes   │ ────────▶│  ModelScope API    │
│  Opencode         │         │  (Python)        │          │  Qwen3-VL-8B       │
│  (DeepSeek API)   │         │                  │          │  (国内直连, 免费)   │
└──────────────────┘         └──────────────────┘          └───────────────────┘
                                    │
                                    ▼
                          读取系统剪贴板 (PIL)
                          → base64 → 发送 → 返回中文描述 → 删除临时文件
```

### 📋 MCP 工具列表

| 工具 | 功能 |
|------|------|
| `analyze_clipboard` | 分析剪贴板中的图片 |
| `extract_text_from_clipboard` | 剪贴板图片 OCR 提取文字 |
| `describe_ui_from_clipboard` | 分析剪贴板 UI 截图 |
| `diagnose_error_from_clipboard` | 诊断剪贴板错误截图 |
| `code_from_clipboard` | 从剪贴板代码截图提取代码 |
| `analyze_image` | 分析磁盘图片文件 |
| `extract_text` | 磁盘图片 OCR |
| `describe_ui` | 分析磁盘 UI 截图 |
| `diagnose_error` | 诊断磁盘错误截图 |
| `understand_diagram` | 解读流程图/架构图 |
| `analyze_chart` | 分析数据图表 |
| `code_from_screenshot` | 磁盘代码截图提取代码 |

### 🔌 客户端配置

**Claude Code**（`.claude/settings.json`）：

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "D:\\GitHub\\deepseek-eyes\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "MODELSCOPE_API_KEY": "你的_API_Key"
      }
    }
  }
}
```

> ⚠️ `command` 必须使用 venv 中 Python 的**绝对路径**。

**Opencode**（`%APPDATA%\opencode\opencode.json`）：

```json
{
  "mcp": {
    "deepseek-eyes": {
      "type": "local",
      "command": ["D:\\GitHub\\deepseek-eyes\\.venv\\Scripts\\python.exe", "-m", "deepseek_eyes"],
      "enabled": true,
      "environment": {
        "MODELSCOPE_API_KEY": "你的_API_Key"
      }
    }
  }
}
```

### 🤖 AI 一键安装

把 [安装提示词](docs/INSTALL_PROMPT_CN.md) 粘贴给 Claude Code / DeepSeek，让它帮你自动完成安装。

### ❓ 常见问题

见 [故障排查指南](docs/TROUBLESHOOTING.md)

### 🛡️ 安全

- 本地 stdio 进程运行，不开放任何网络端口
- 临时剪贴板文件分析完成后**自动删除**
- 仅接受图片格式（`.png .jpg .jpeg .gif .webp .bmp`），防止 LLM 注入后读取任意文件
- 文件大小限制 20MB，魔数校验
- 图片经 base64 编码发送至 ModelScope API，参阅其[隐私政策](https://modelscope.cn/privacy)

### 🗺️ 路线图

- [ ] 支持 DashScope（阿里云官方）作为备用后端
- [ ] 多 API Key 轮询
- [ ] 视频关键帧提取 + 分析

---

## 🇬🇧 English

See [README_EN.md](README_EN.md) for the full English version.

---

## 🙏 致谢

- 基于 [Capetlevrai/clipboard-vision-mcp](https://github.com/Capetlevrai/clipboard-vision-mcp) (MIT)
- 视觉模型：通义千问VL / Qwen-VL via [ModelScope](https://modelscope.cn)

## 📄 License

MIT © Shaohan He
