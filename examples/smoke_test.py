"""剪贴板冒烟测试 — 无需 ModelScope API Key。

使用方法:
  1. 复制任意图片到剪贴板（如截图）。
  2. python examples/smoke_test.py

Quick local sanity check — does NOT require ModelScope API Key.
"""

from deepseek_eyes.clipboard import save_clipboard_image, ClipboardError


def main() -> None:
    try:
        path = save_clipboard_image()
    except ClipboardError as e:
        print(f"❌ 失败: {e} / FAIL: {e}")
        return
    print(f"✅ 成功: 剪贴板图片已保存到 {path} / OK: clipboard image saved to {path}")


if __name__ == "__main__":
    main()
