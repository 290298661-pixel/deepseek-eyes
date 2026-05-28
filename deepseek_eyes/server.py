"""deepseek-eyes MCP Server — 给 DeepSeek 装上眼睛

通过通义千问VL (Qwen-VL via ModelScope) 为无视觉能力的文本模型
提供图片理解能力。支持剪贴板直接读取和文件路径两种方式。

Tools: clipboard-first (analyze_clipboard, extract_text_from_clipboard, ...)
       file-path (analyze_image, extract_text, ...)
"""

from __future__ import annotations

import asyncio
import base64
import os
from pathlib import Path
from typing import Any

import aiofiles
from openai import AsyncOpenAI
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .clipboard import ClipboardError, save_clipboard_image

SERVER_NAME = "deepseek-eyes"
SERVER_VERSION = "1.0.0"

# ModelScope API 配置
MODELSCOPE_BASE_URL = "https://api-inference.modelscope.cn/v1"
DEFAULT_MODEL = "Qwen/Qwen3-VL-8B-Instruct"
VISION_MODEL = os.environ.get("VISION_MODEL", DEFAULT_MODEL)

# 安全检查
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
MAX_IMAGE_BYTES = 20 * 1024 * 1024
IMAGE_MAGIC_PREFIXES = (
    b"\x89PNG\r\n\x1a\n",
    b"\xff\xd8\xff",
    b"GIF87a",
    b"GIF89a",
    b"RIFF",
    b"BM",
)


def _validate_image_path(path_str: str) -> Path:
    """校验图片路径，拒绝非图片文件和超大文件。"""
    p = Path(path_str).resolve()
    if not p.is_file():
        raise ValueError(f"不是一个文件: {path_str}")
    if p.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"拒绝读取 '{p.suffix}' —— 仅允许图片格式 "
            f"({', '.join(sorted(ALLOWED_EXTENSIONS))})。"
        )
    size = p.stat().st_size
    if size > MAX_IMAGE_BYTES:
        raise ValueError(f"图片过大: {size} 字节 (最大 {MAX_IMAGE_BYTES})。")
    return p


def _validate_magic(data: bytes) -> None:
    """校验文件魔数。"""
    if not any(data.startswith(m) for m in IMAGE_MAGIC_PREFIXES):
        raise ValueError("文件内容不像是支持的图片格式。")


server = Server(SERVER_NAME)


class VisionClient:
    """通义千问VL 视觉客户端 (via ModelScope OpenAI-compatible API)"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=MODELSCOPE_BASE_URL)

    async def analyze(self, image_path: str, prompt: str) -> str:
        p = _validate_image_path(image_path)
        async with aiofiles.open(p, "rb") as f:
            data = await f.read()
        _validate_magic(data)
        b64 = base64.b64encode(data).decode("utf-8")

        response = await self.client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""


vision_client: VisionClient | None = None


PROMPTS: dict[str, str] = {
    "analyze": "请详细描述这张图片的内容。包括所有相关元素、上下文，以及任何对看不到图片的人有用的信息。",
    "extract_text": "提取这张图片中的全部文字。只返回文字内容，保留排版和换行，不做任何评论。",
    "describe_ui": (
        "分析这张 UI 截图。描述：1) 整体布局 2) 组件（按钮、表单、导航、输入框）"
        "3) 可见文字和标签 4) 状态（错误提示、激活标签页、弹窗等）。"
    ),
    "diagnose_error": (
        "分析这张错误截图。返回：1) 精确的错误信息 2) 可能的原因 "
        "3) 具体的修复步骤 4) 如何避免再次发生。"
    ),
    "understand_diagram": (
        "解读这张图表。返回：1) 图表类型 2) 组成部分及其作用 "
        "3) 关系/流程 4) 整体目的。"
    ),
    "analyze_chart": (
        "分析这张数据图表。返回：1) 图表类型 2) 坐标轴和标签 "
        "3) 关键趋势 4) 值得注意的数据点 5) 洞察。"
    ),
    "code_from_screenshot": (
        "从这张截图中提取全部代码。返回：1) 编程语言 2) 格式化的代码块，保留缩进。"
    ),
}


def _image_tool(name: str, zh: str, en: str) -> Tool:
    return Tool(
        name=name,
        description=f"{zh} / {en}",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "图片文件的绝对路径 / Absolute path to the image file.",
                }
            },
            "required": ["image_path"],
        },
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_clipboard",
            description=(
                "读取系统剪贴板中的图片并分析。当用户说'看看这个'、'剪贴板里有什么'、"
                "或粘贴截图时使用。可选参数 prompt 可自定义提问。"
                " / Analyze the image in system clipboard."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "自定义问题 / Custom question."}
                },
                "required": [],
            },
        ),
        Tool(
            name="extract_text_from_clipboard",
            description="从剪贴板图片中提取文字(OCR) / Extract text from clipboard image (OCR).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="describe_ui_from_clipboard",
            description="描述剪贴板中 UI 截图的布局、组件和状态 / Describe UI from clipboard screenshot.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="diagnose_error_from_clipboard",
            description="诊断剪贴板中错误截图的原因和修复方案 / Diagnose error screenshot from clipboard.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="code_from_clipboard",
            description="从剪贴板代码截图中提取可编辑的代码 / Extract code from clipboard screenshot.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="analyze_image",
            description="分析磁盘上的图片文件 / Analyze an image file on disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "图片路径"},
                    "prompt": {"type": "string", "description": "自定义问题"},
                },
                "required": ["image_path"],
            },
        ),
        _image_tool("extract_text", "从磁盘图片中提取文字(OCR)", "OCR an image file on disk"),
        _image_tool("describe_ui", "描述磁盘上 UI 截图文件", "Describe a UI screenshot file"),
        _image_tool("diagnose_error", "诊断磁盘上错误截图文件", "Diagnose an error screenshot file"),
        _image_tool("understand_diagram", "解读流程图/架构图等图表", "Interpret a diagram image file"),
        _image_tool("analyze_chart", "分析数据图表中的趋势和洞察", "Analyze a chart image file"),
        _image_tool("code_from_screenshot", "从磁盘代码截图提取代码", "Extract code from a screenshot file"),
    ]


async def _run(prompt_key: str, image_path: str, override: str | None = None) -> str:
    assert vision_client is not None
    prompt = override or PROMPTS[prompt_key]
    return await vision_client.analyze(image_path, prompt)


async def _run_clipboard(prompt_key: str, override: str | None = None) -> str:
    try:
        path = save_clipboard_image()
    except ClipboardError as e:
        return f"剪贴板错误: {e}"
    try:
        return await _run(prompt_key, path, override)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if vision_client is None:
        return [
            TextContent(
                type="text",
                text="❌ 未设置 MODELSCOPE_API_KEY 环境变量。\n\n"
                "获取免费 API Key（每天2000次，单模型500次）：\n"
                "1. 打开 https://modelscope.cn/my/myaccesstoken\n"
                "2. 登录 → 首次使用需绑定阿里云账号\n"
                "3. 点击「新建访问令牌」→ 命名 → 生成 → 复制\n"
                "4. ⚠️ 令牌格式为 ms-xxxxxxxx，使用时去掉 ms- 前缀！\n"
                "5. 将去掉前缀后的 Key 设置到 MCP 配置的 env 中\n\n"
                "MODELSCOPE_API_KEY not set. "
                "Get a free key at https://modelscope.cn/my/myaccesstoken "
                "(2000 calls/day, remove ms- prefix).",
            )
        ]

    try:
        if name == "analyze_clipboard":
            text = await _run_clipboard("analyze", arguments.get("prompt"))
        elif name == "extract_text_from_clipboard":
            text = await _run_clipboard("extract_text")
        elif name == "describe_ui_from_clipboard":
            text = await _run_clipboard("describe_ui")
        elif name == "diagnose_error_from_clipboard":
            text = await _run_clipboard("diagnose_error")
        elif name == "code_from_clipboard":
            text = await _run_clipboard("code_from_screenshot")
        elif name == "analyze_image":
            text = await _run("analyze", arguments["image_path"], arguments.get("prompt"))
        elif name == "extract_text":
            text = await _run("extract_text", arguments["image_path"])
        elif name == "describe_ui":
            text = await _run("describe_ui", arguments["image_path"])
        elif name == "diagnose_error":
            text = await _run("diagnose_error", arguments["image_path"])
        elif name == "understand_diagram":
            text = await _run("understand_diagram", arguments["image_path"])
        elif name == "analyze_chart":
            text = await _run("analyze_chart", arguments["image_path"])
        elif name == "code_from_screenshot":
            text = await _run("code_from_screenshot", arguments["image_path"])
        else:
            text = f"未知工具: {name}"
        return [TextContent(type="text", text=text)]
    except Exception as e:
        return [TextContent(type="text", text=f"错误: {e}")]


async def main() -> None:
    global vision_client
    api_key = os.environ.get("MODELSCOPE_API_KEY")
    if api_key:
        vision_client = VisionClient(api_key)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run() -> None:
    """入口: python -m deepseek_eyes"""
    asyncio.run(main())


if __name__ == "__main__":
    run()
