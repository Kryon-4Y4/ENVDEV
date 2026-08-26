"""最简 Web UI —— 用 Gradio 给 ChatBot 套一个网页界面。

运行：
    python -m envdev.web_ui
然后浏览器打开 http://127.0.0.1:7860
"""

import gradio as gr
from openai import OpenAI

from envdev.config import settings
from envdev.main import build_system_prompt

# 复用终端版同一套 DeepSeek 客户端配置
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


def chat(user_message: str, history: list) -> str:
    """Gradio 回调：接收当前消息 + 历史，返回模型回复。

    history 已是 messages 格式 [{"role":..., "content":...}, ...]，直接拼接即可。
    """
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    msg = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
    )
    return msg.choices[0].message.content


demo = gr.ChatInterface(
    fn=chat,
    title="ENVDEV ChatBot",
    description="基于 DeepSeek 的多轮对话助手（AGENT.md 人设 + skill 已注入）",
)

if __name__ == "__main__":
    demo.launch()
