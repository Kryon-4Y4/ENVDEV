"""后端 API 端 —— FastAPI 提供 /api/chat 接口（纯 API，不托管页面）。

运行：
    python -m envdev.api_gateway.server
- API 地址：http://127.0.0.1:8001/api/chat
- API 文档：http://127.0.0.1:8001/docs（FastAPI 自动生成）
- 端口用 8001：8000 被本机 Docker 的通配监听占用（手机联调需绑 0.0.0.0，与它冲突）
- 页面需另开端：python -m envdev.user_portal.webui.front（:3000）
"""

import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from envdev.core import build_system_prompt, chat, chat_stream

app = FastAPI(title="ENVDEV ChatBot API")

# CORS 跨域放行：前端端（:3000）独立部署，跨端口调本 API 需浏览器放行
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",           # 本地 Vite 开发
        "http://127.0.0.1:3000",           # 本地旧端口
        "https://envdev-tau.vercel.app",   # Vercel 生产前端
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
    """系统提示词+用户历史消息+用户最新消息"""
    # 防御：过滤空内容消息（DeepSeek 要求 assistant 消息必须有 content，否则 400）
    history = [m for m in req.history if m.get("content")]
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += history
    messages.append({"role": "user", "content": req.message})
    return {"reply": chat(messages)}


# 流式端点：把模型的逐块输出通过 SSE（Server-Sent Events）持续推给前端，
# 前端不用等全部生成完就能看到“打字机”效果。与 /api/chat 共存，便于对比。
@app.post("/api/chat/stream")
def api_chat_stream(req: ChatRequest):
    """流式聊天接口：SSE 格式 data: {...}\n\n 逐块推送，[DONE] 表示结束。"""
    # 防御：过滤空内容消息（同 /api/chat）
    history = [m for m in req.history if m.get("content")]
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += history
    messages.append({"role": "user", "content": req.message})

    def generate():
        # SSE 每条消息格式：data: <内容>\n\n（前端按 \n\n 切分）
        for piece in chat_stream(messages):
            yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"  # 结束信号（沿用 OpenAI 惯例）

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 = 监听所有网卡，允许局域网设备（如手机）访问；127.0.0.1 只接待本机。
    # 端口 8001：8000 被 Docker 占用（它监听通配地址，与 0.0.0.0 绑定冲突）
    uvicorn.run(app, host="0.0.0.0", port=8001)
