"""GUI 端 —— 桌面窗口聊天（Tkinter 标准库，零依赖，流式输出）。

运行：
    python -m envdev.user_portal.gui.main
与 CLI 同属本地直调端：直接调 core，无需启动 API 端。
"""

import multiprocessing
import queue
import threading
import tkinter as tk

from envdev.config import settings
from envdev.core import build_system_prompt, chat_stream


def run_gui() -> None:
    if not settings.DEEPSEEK_API_KEY:
        print("请在 .env 中配置 DEEPSEEK_API_KEY")
        return

    window = tk.Tk()
    window.title("ENVDEV ChatBot（GUI 版 · 流式）")
    window.geometry("640x720")

    text = tk.Text(window, wrap="word", state="disabled", font=("PingFang SC", 14))
    text.pack(fill="both", expand=True, padx=10, pady=(10, 4))

    bar = tk.Frame(window)
    bar.pack(fill="x", padx=10, pady=(0, 10))
    entry = tk.Entry(bar, font=("PingFang SC", 14))
    entry.pack(side="left", fill="x", expand=True)
    send = tk.Button(bar, text="发送", width=8)
    send.pack(side="right", padx=(8, 0))

    messages = [{"role": "system", "content": build_system_prompt()}]
    stream_queue = queue.Queue()  # 后台线程 → 主线程（Tkinter 只允许主线程操作控件）
    reply_full = ""
    busy = False

    def insert(s: str) -> None:
        text.configure(state="normal")
        text.insert("end", s)
        text.configure(state="disabled")
        text.see("end")

    def poll_stream() -> None:
        """主线程每 50ms 轮询：把流式增量追加到消息区（打字机效果）。"""
        nonlocal reply_full, busy
        while True:
            try:
                piece = stream_queue.get_nowait()
            except queue.Empty:
                break
            if piece is None:  # 结束信号
                if reply_full:  # 空回复不存历史（防历史污染）
                    messages.append({"role": "assistant", "content": reply_full})
                reply_full, busy = "", False
                send.configure(state="normal")
                insert("\n\n")
                continue
            reply_full += piece
            insert(piece)
        window.after(50, poll_stream)

    def worker() -> None:
        """后台线程消费流：网络请求不能阻塞 UI 主线程。"""
        try:
            for piece in chat_stream(messages):
                stream_queue.put(piece)
        except Exception as err:
            stream_queue.put(f"[请求失败: {err}]")
        finally:
            stream_queue.put(None)

    def on_send(event=None) -> None:
        nonlocal busy
        user_input = entry.get().strip()
        if not user_input or busy:
            return
        entry.delete(0, "end")
        busy = True
        send.configure(state="disabled")
        messages.append({"role": "user", "content": user_input})
        insert(f"🧑 你: {user_input}\n🤖: ")
        threading.Thread(target=worker, daemon=True).start()

    send.configure(command=on_send)
    entry.bind("<Return>", on_send)
    window.after(50, poll_stream)
    window.mainloop()


if __name__ == "__main__":
    multiprocessing.freeze_support()  # PyInstaller 打包兼容（防子进程重复拉起）
    run_gui()
