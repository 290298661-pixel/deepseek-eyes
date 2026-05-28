# MCP 客户端配置 / MCP Client Configuration

## Claude Code

在 `.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "D:\\GitHub\\deepseek-eyes\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "MODELSCOPE_API_KEY": "your_key_here"
      }
    }
  }
}
```

> ⚠️ `command` 必须使用 venv 中 Python 的**绝对路径**。

## Cursor

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "python",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "MODELSCOPE_API_KEY": "your_key_here"
      }
    }
  }
}
```

## Cline / Continue

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "python",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "MODELSCOPE_API_KEY": "your_key_here"
      }
    }
  }
}
```

## 手动验证

```bash
python -m deepseek_eyes
# 应该静默等待输入，Ctrl+C 退出
```
