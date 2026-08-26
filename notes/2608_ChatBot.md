# 调用大模型（最小示例）

通过 **OpenAI 兼容客户端**调用 DeepSeek，并把 `AGENT.md` 人设注入 system 消息。对应 `src/envdev/main.py`。

## 代码

```python
"""ENVDEV 入口点 —— 通过 OpenAI 兼容客户端调用 DeepSeek。"""
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

```

## 关键步骤

| 步骤 | 作用 |
|------|------|
| `PROJECT_ROOT` | 基于 `__file__` 定位项目根，任意目录运行都可用 |
| 读 `AGENT.md` | 模拟"工具加载文件"，取出人设文本 |
| 注入 system | 把人设塞进 system 消息，随请求发给模型 |
| `chat.completions.create` | 调用 DeepSeek 聊天接口，取回回复 |

## 要点

- 用 **OpenAI 兼容客户端**调 DeepSeek：`base_url="https://api.deepseek.com"`
- API key 从 `.env` 的 `DEEPSEEK_API_KEY` 读取（经 `settings` 单例）
- 模型名用 `settings.LLM_MODEL`，不写死
