"""ENVDEV 入口点 —— 终端多轮对话 ChatBot（CLI 交互式 REPL）。"""

from envdev.config import settings
from envdev.core import build_system_prompt, chat_stream


def main() -> None:
    """终端对话循环：读输入 → 调模型 → 打印结果 → 循环（REPL）。"""
    if not settings.DEEPSEEK_API_KEY:
        print("请在 .env 中配置 DEEPSEEK_API_KEY")
        return

    # 对话历史：system 人设常驻，user/assistant 逐轮累积（多轮记忆的关键）
    messages = [{"role": "system", "content": build_system_prompt()}]

    print(f"=== envdev chatbot（模型: {settings.LLM_MODEL}）===")
    print("输入 exit / quit / q 退出\n")

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C 优雅退出
            print("\n再见！")
            break

        if not user_input:  # 跳过空输入
            continue
        if user_input.lower() in {"exit", "quit", "q"}:
            print("再见！")
            break

        messages.append({"role": "user", "content": user_input})
        # 流式输出：边收边打印（flush 不等换行立即刷出），同时拼接完整回复存历史
        print("🤖: ", end="", flush=True)
        reply = ""
        for piece in chat_stream(messages):  # 核心流式调用（与 web / API 端共用）
            print(piece, end="", flush=True)
            reply += piece
        print("\n")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
