"""注册表 MIME 污染回归测试。

背景：Windows 上 mimetypes 读注册表猜 Content-Type，若 HKCR\\.js 被第三方
软件改成 text/plain，浏览器会拒绝执行 module script，前端整页白屏。
app/main.py 导入时写死前端常用扩展名的映射，本测试守住这条防线。
"""
from __future__ import annotations

import mimetypes


def test_前端关键扩展名映射正确():
    import app.main  # noqa: F401 — 导入即应用覆盖

    assert mimetypes.guess_type("app.js")[0] == "text/javascript"
    assert mimetypes.guess_type("app.mjs")[0] == "text/javascript"
    assert mimetypes.guess_type("app.css")[0] == "text/css"
    assert mimetypes.guess_type("index.html")[0] == "text/html"
    assert mimetypes.guess_type("icon.svg")[0] == "image/svg+xml"
