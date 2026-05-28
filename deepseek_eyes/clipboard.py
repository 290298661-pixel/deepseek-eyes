"""跨平台剪贴板图片提取 / Cross-platform clipboard image extraction.

Windows: PIL.ImageGrab（原生支持）.
macOS:   PIL.ImageGrab, 回退到 `pngpaste`.
Linux:   `wl-paste` (Wayland) 或 `xclip` (X11).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import uuid
from pathlib import Path


class ClipboardError(RuntimeError):
    """剪贴板中无图片时抛出 / Raised when no image can be read from the clipboard."""


def _temp_path() -> Path:
    d = Path(tempfile.gettempdir()) / "deepseek_eyes"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"clip_{uuid.uuid4().hex}.png"


def save_clipboard_image() -> str:
    """将剪贴板中的图片保存为临时 PNG 并返回路径。
    如果剪贴板中没有图片则抛出 ClipboardError。

    Save the current clipboard image to a temp PNG and return its path.
    Raises ClipboardError if the clipboard does not contain an image.
    """
    out = _temp_path()
    platform = sys.platform

    if platform == "win32":
        _grab_with_pil(out)
    elif platform == "darwin":
        try:
            _grab_with_pil(out)
        except ClipboardError:
            _grab_macos_pngpaste(out)
    else:
        _grab_linux(out)

    if not out.exists() or out.stat().st_size == 0:
        raise ClipboardError("剪贴板中没有图片 / Clipboard does not contain an image.")
    return str(out)


def _grab_with_pil(out: Path) -> None:
    try:
        from PIL import ImageGrab, Image
    except ImportError as e:
        raise ClipboardError(
            "需要安装 Pillow: pip install Pillow"
        ) from e

    img = ImageGrab.grabclipboard()
    if img is None:
        raise ClipboardError("剪贴板中没有图片 / No image found in clipboard.")

    # Windows: 如果用户从资源管理器复制了文件，PIL 返回文件路径列表
    if isinstance(img, list):
        if not img:
            raise ClipboardError("剪贴板中没有图片 / No image found in clipboard.")
        src = img[0]
        Image.open(src).save(out, "PNG")
        return

    img.save(out, "PNG")


def _grab_macos_pngpaste(out: Path) -> None:
    try:
        result = subprocess.run(
            ["pngpaste", str(out)], capture_output=True, timeout=10
        )
    except FileNotFoundError:
        raise ClipboardError(
            "剪贴板中无图片。安装 pngpaste: brew install pngpaste"
        )
    if result.returncode != 0:
        raise ClipboardError("剪贴板中无图片(pngpaste 失败) / No image in clipboard.")


def _grab_linux(out: Path) -> None:
    attempts = [
        (["wl-paste", "--type", "image/png"], "wl-clipboard"),
        (["xclip", "-selection", "clipboard", "-t", "image/png", "-o"], "xclip"),
    ]
    errors: list[str] = []
    for cmd, pkg in attempts:
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=10)
        except FileNotFoundError:
            errors.append(f"未安装 {pkg}")
            continue
        if result.returncode == 0 and result.stdout:
            out.write_bytes(result.stdout)
            return
        errors.append(f"{pkg} 返回空图片")
    raise ClipboardError(
        "剪贴板中无图片。请安装 wl-clipboard(Wayland) 或 xclip(X11)。"
        f"尝试结果: {', '.join(errors)}"
    )
