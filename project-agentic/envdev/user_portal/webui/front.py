"""前端 UI 端 —— 独立托管静态聊天页面（真正的前后端分离）。

运行：
    python -m envdev.user_portal.webui.front
然后浏览器打开 http://127.0.0.1:3000
注意：需同时启动后端 API 端（python -m envdev.api_gateway.server，:8000）
"""

import functools
import http.server
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent / "static"  # 前端静态文件目录
HOST, PORT = "127.0.0.1", 3000


def main() -> None:
    """启动静态文件服务：访问 / 自动返回 static/index.html。"""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(STATIC_DIR)
    )
    with http.server.ThreadingHTTPServer((HOST, PORT), handler) as httpd:
        print(f"前端页面：http://{HOST}:{PORT}（需同时启动后端 API：:8000）")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
