"""业务核心 —— prompt 组装 + LLM 调用（各端共用）。"""

import sys
from pathlib import Path

from openai import OpenAI

from envdev.config import settings

# 打包模式（PyInstaller）：配置目录 = 可执行文件同目录（.env/AGENT.md/skill 外置）；
# 若身处 macOS .app 包内（三层深），跳到 .app 所在目录。开发模式保持源码路径定位。
FROZEN = getattr(sys, "frozen", False)


def _config_dir() -> Path:
    base = Path(sys.executable).resolve().parent
    # 找出 .app 包目录（如 ENVDEV.app），跳到其所在目录（目录名以 .app 结尾）
    app_idx = next((i for i, p in enumerate(base.parts) if p.endswith(".app")), None)
    if app_idx is not None:
        base = Path(*base.parts[: app_idx + 1]).parent
    return base


PROJECT_ROOT = (
    _config_dir()
    if FROZEN
    else Path(__file__).resolve().parents[2]  # 项目根 = project-agentic/（AGENT.md 所在处）
)
SKILL_DIR = (
    PROJECT_ROOT / "skill"  # 打包后：.app 旁的 skill/ 目录
    if FROZEN
    else Path(__file__).resolve().parent / "skill"
)

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
