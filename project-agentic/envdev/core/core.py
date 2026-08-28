"""业务核心 —— prompt 组装 + LLM 调用（终端 / Gradio / 前后端分离三端共用）。"""

from pathlib import Path

from openai import OpenAI

from envdev.config import settings

# 路径定位（基于 __file__，任意 cwd 可用）
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # 项目根 = project/（AGENT.md 所在处）
SKILL_DIR = Path(__file__).resolve().parent / "skill"  # skill 目录

# DeepSeek 的 OpenAI 兼容客户端（模块级单例，三端复用）
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


def build_system_prompt() -> str:
    """组装 system 提示：AGENT.md 人设 + skill 技能。"""
    rules = (PROJECT_ROOT / "AGENT.md").read_text(encoding="utf-8")
    skill = (SKILL_DIR / "hello_skill" / "skill.md").read_text(encoding="utf-8")
    return (
        f"【项目指引 AGENT.md】\n{rules}\n\n"
        f"【技能 skill.md】\n{skill}\n\n"
        "当用户意图匹配技能触发条件时，严格按技能指令执行。"
    )


def chat(messages: list) -> str:
    """调用 LLM 并返回模型回复。

    messages 为完整对话历史（含 system 人设），由调用方负责维护。
    """
    msg = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
    )
    return msg.choices[0].message.content


def chat_stream(messages: list):
    """流式调用 LLM：逐块 yield 模型生成的文本片段（打字机效果）。

    关键：stream=True 后，返回值从“完整消息”变为生成器，
    增量文本在每个 chunk.choices[0].delta.content 里。
    调用方如需完整回复，自行拼接（历史库存完整文本）。
    """
    stream = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        if delta:
            yield delta
