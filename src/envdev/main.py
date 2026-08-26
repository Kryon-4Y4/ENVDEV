"""ENVDEV 入口点 —— 终端多轮对话 ChatBot（OpenAI 兼容客户端调用 DeepSeek）。"""

from pathlib import Path

from openai import OpenAI

from envdev.config import settings

# 路径定位（基于 __file__，任意 cwd 可用）
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # 项目根
SKILL_DIR = Path(__file__).resolve().parent / "skill"  # skill 目录


def build_system_prompt() -> str:
    """组装 system 提示：AGENT.md 人设 + skill 技能。"""
    rules = (PROJECT_ROOT / "AGENT.md").read_text(encoding="utf-8")
    skill = (SKILL_DIR / "hello_skill" / "skill.md").read_text(encoding="utf-8")
    return (
        f"【项目指引 AGENT.md】\n{rules}\n\n"
        f"【技能 skill.md】\n{skill}\n\n"
        "当用户意图匹配技能触发条件时，严格按技能指令执行。"
    )


def main() -> None:
    """终端多轮对话循环。"""
    if not settings.DEEPSEEK_API_KEY:
        print("请在 .env 中配置 DEEPSEEK_API_KEY")
        return

    client = OpenAI(  # DeepSeek 的 OpenAI 兼容接口
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
    )

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

        msg = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
        )
        reply = msg.choices[0].message.content

        messages.append({"role": "assistant", "content": reply})
        print(f"🤖: {reply}\n")

if __name__ == "__main__":
    main()
