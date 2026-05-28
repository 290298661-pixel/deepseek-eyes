# Opencode 配置指南

## 安装

```bash
git clone https://github.com/290298661-pixel/deepseek-eyes.git
cd deepseek-eyes
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e .
```

## 获取 ModelScope API Key

访问 https://modelscope.cn → 登录 → 个人中心 → 访问令牌 → 创建令牌（免费，每天500次）

## 配置 Opencode

编辑 `%APPDATA%\opencode\opencode.json`：

```json
{
  "mcp": {
    "deepseek-eyes": {
      "type": "local",
      "command": ["D:\\GitHub\\deepseek-eyes\\.venv\\Scripts\\python.exe", "-m", "deepseek_eyes"],
      "enabled": true,
      "environment": {
        "MODELSCOPE_API_KEY": "your_key_here"
      }
    }
  }
}
```

> ⚠️ 使用 venv 中 Python 的绝对路径。

## 键盘快捷键

```json
{
  "keybinds": {
    "input_paste": "ctrl+v",
    "input_paste_image": "alt+v"
  }
}
```

## 测试

1. 重启 Opencode → 截图 (Win+Shift+S) → Alt+V 粘贴
2. 输入：`analyze_clipboard 这张图里有什么？`
3. DeepSeek 应该能描述图片内容

## 故障排查

- **工具不出现**：运行 `python -m deepseek_eyes` 确认无报错
- **临时文件**：`%TEMP%\deepseek_eyes\`，自动删除
