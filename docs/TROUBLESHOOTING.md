# 故障排查 / Troubleshooting

## 剪贴板问题

**"剪贴板中没有图片"**

- 确认你真的复制了一张**图片**（截图、复制图片文件不算——必须是图片的**内容**在剪贴板里）
- Windows: 用 `Win+Shift+S` 截图，或 `Alt+PrintScreen` 截当前窗口
- Linux Wayland: `wl-paste --type image/png > /dev/null` 检查剪贴板
- Linux X11: `xclip -selection clipboard -t image/png -o > /dev/null`

**Linux 上工具不存在**

```bash
# Wayland
sudo apt install wl-clipboard

# X11
sudo apt install xclip
```

## API Key 问题

**"MODELSCOPE_API_KEY is not set"**

1. 访问 https://modelscope.cn 注册/登录
2. 个人中心 → 访问令牌 → 创建令牌
3. 确保 MCP 配置中的 `env` 块包含 `MODELSCOPE_API_KEY`
4. **完全重启** MCP 客户端（不是重载，是退出再打开）

## MCP 工具不出现

**Claude Code 中看不到 deepseek-eyes 的工具**

1. 检查 `.claude/settings.json` 中 JSON 语法是否正确（不能有尾随逗号）
2. **command 必须使用 venv 中 Python 的绝对路径**，不能用相对路径
3. 手动验证：在终端中运行 `.venv\Scripts\python.exe -m deepseek_eyes`，它应该静默等待输入（不会报错）

## 模型调用失败

**"Connection refused / timeout"**

- ModelScope API 地址：`https://api-inference.modelscope.cn/v1`
- 确认网络能访问（不需要翻墙）
- 500 次/天的免费额度是否用完？等第二天重置

**返回的图片描述质量不好**

- 默认使用 `Qwen3-VL-8B-Instruct`（速度与质量平衡）
- 可在 MCP 配置中设置环境变量 `VISION_MODEL=Qwen/Qwen3-VL-235B-A22B-Instruct` 使用更强的模型
- 更强的模型 token 消耗更高，但描述质量显著提升
