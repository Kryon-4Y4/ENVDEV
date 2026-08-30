"""后端 API 端 —— FastAPI 提供 /api/chat 接口（纯 API，不托管页面）。

运行：
    python -m envdev.api_gateway.server
- API 地址：http://127.0.0.1:8001/api/chat
- API 文档：http://127.0.0.1:8001/docs（FastAPI 自动生成）
- 端口用 8001：8000 被本机 Docker 的通配监听占用（手机联调需绑 0.0.0.0，与它冲突）
- 页面需另开端：python -m envdev.user_portal.webui.front（:3000）
"""

import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from envdev.core import build_system_prompt, chat, chat_stream

# ChatBot 联系方式回复模板（硬编码，不在 system prompt 中）
CONTACT_REPLY = """你可以通过以下方式联系佬K：

1. 点击链接（复制后在浏览器打开）：
https://t.me/KuangyueHuang

2. 在 Telegram 搜索用户名：
@KuangyueHuang"""

# 用于检测模型是否泄露了 system prompt 的关键词
LEAK_KEYWORDS = ["AGENT.md", "项目指引", "技能 skill.md", "内部指引", "不要复述", "参考回复格式"]

app = FastAPI(title="ENVDEV ChatBot API")

# CORS 跨域放行：前端端（:3000）独立部署，跨端口调本 API 需浏览器放行
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",           # 本地 Vite 开发
        "http://127.0.0.1:3000",           # 本地旧端口
        "https://www.4y4.com",              # 生产前端域名
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

#定义的是一个**类**——但它是种特殊的类：**数据模型**（用来描述"请求长什么样"），里面没有方法，只有字段声明：
class ChatRequest(BaseModel):
    """请求体：本轮消息 + 历史对话。"""

    message: str
    history: list = []  # [{"role": "user"/"assistant", "content": "..."}, ...]

# @app.post("/api/chat") 是路由注册 这行叫装饰器（@ 开头），作用是给下面的函数"挂牌"： 
# 当有人向 POST http://127.0.0.1:8001/api/chat 发请求时，就调用下面的 api_chat() 函数。
@app.post("/api/chat")
def api_chat(req: ChatRequest) -> dict:
    """聊天接口：组装消息 → 调核心逻辑 → 返回模型回复。"""
    history = [m for m in req.history if m.get("content")]
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += history
    user_msg = req.message
    if any(kw in user_msg for kw in ["联系", "Telegram", "TG", "订阅", "报告"]):
        user_msg = f"{user_msg}\n\n参考回复格式：\n{CONTACT_REPLY}"
    messages.append({"role": "user", "content": user_msg})
    reply = chat(messages)
    # 后处理：如果模型泄露了 system prompt，返回固定回复
    if any(kw in reply for kw in LEAK_KEYWORDS):
        return {"reply": CONTACT_REPLY}
    return {"reply": reply}


# 流式端点：把模型的逐块输出通过 SSE（Server-Sent Events）持续推给前端，
# 前端不用等全部生成完就能看到“打字机”效果。与 /api/chat 共存，便于对比。
@app.post("/api/chat/stream")
def api_chat_stream(req: ChatRequest):
    """流式聊天接口：SSE 格式 data: {...}\n\n 逐块推送，[DONE] 表示结束。"""
    history = [m for m in req.history if m.get("content")]
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += history
    user_msg = req.message
    if any(kw in user_msg for kw in ["联系", "Telegram", "TG", "订阅", "报告"]):
        user_msg = f"{user_msg}\n\n参考回复格式：\n{CONTACT_REPLY}"
    messages.append({"role": "user", "content": user_msg})

    def generate():
        full_reply = ""
        for piece in chat_stream(messages):
            full_reply += piece
            yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
        # 流式结束后检查是否泄露，若泄露则补发正确回复
        if any(kw in full_reply for kw in LEAK_KEYWORDS):
            yield f"data: {json.dumps({'content': '\n' + CONTACT_REPLY}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"  # 结束信号（沿用 OpenAI 惯例）

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 = 监听所有网卡，允许局域网设备（如手机）访问；127.0.0.1 只接待本机。
    # Railway 动态分配 PORT；本地开发默认 8001
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
