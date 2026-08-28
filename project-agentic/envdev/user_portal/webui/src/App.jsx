// 主组件：聊天界面（消息列表 + 输入框）+ SSE 流式对话逻辑
import { useState } from "react";

// SSE 流式请求：每收到一块文本就调用 onPiece（纯 JS 逻辑，从旧 index.html 迁移）
// 用相对路径 /api：开发时由 Vite 代理转发到后端 :8000，无 CORS 问题
async function streamChat(message, history, onPiece) {
  const res = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) throw new Error("后端错误 HTTP " + res.status);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // SSE 消息以 \n\n 分隔；一次 read 的字节与消息边界不对齐，需缓冲切分
    const parts = buffer.split("\n\n");
    buffer = parts.pop(); // 最后一段可能不完整，留到下一轮
    for (const p of parts) {
      if (!p.startsWith("data: ")) continue;
      const data = p.slice(6);
      if (data === "[DONE]") return;
      onPiece(JSON.parse(data).content);
    }
  }
}

// 消息气泡组件：props（role/content）由父组件传入，像函数传参
function MessageBubble({ role, content }) {
  return <div className={"msg " + role}>{content}</div>;
}

export default function App() {
  // 状态：数据一变，React 自动重新渲染界面（不再手动操作 DOM）
  const [messages, setMessages] = useState([]); // 对话历史 [{role, content}, ...]
  const [input, setInput] = useState(""); // 输入框内容
  const [busy, setBusy] = useState(false); // 是否等待回复中

  async function handleSubmit(e) {
    e.preventDefault();
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setBusy(true);

    // 先放入本轮 user 消息 + 一个空 assistant 气泡（流式内容逐块填进去）
    setMessages((msgs) => [
      ...msgs,
      { role: "user", content: message },
      { role: "assistant", content: "" },
    ]);

    try {
      let full = "";
      // 每收到一块：拼到 full，并替换最后一条（assistant）消息 → 打字机效果
      await streamChat(message, messages, (piece) => {
        full += piece;
        setMessages((msgs) => [
          ...msgs.slice(0, -1),
          { role: "assistant", content: full },
        ]);
      });
      // 防御：回复为空则撤掉空气泡（与后端空内容过滤呼应）
      if (!full) setMessages((msgs) => msgs.slice(0, -1));
    } catch (err) {
      setMessages((msgs) => [
        ...msgs.slice(0, -1),
        { role: "assistant", content: "请求失败：" + err },
      ]);
    } finally {
      setBusy(false);
    }
  }

  // 发给后端的历史：过滤空内容（防止空 assistant 消息污染 → DeepSeek 400）
  const history = messages.filter((m) => m.content);

  return (
    <div className="app">
      <header>ENVDEV ChatBot（React 版 · 流式）</header>
      <div className="chat">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入消息，回车发送…"
          autoComplete="off"
        />
        <button disabled={busy}>{busy ? "回复中…" : "发送"}</button>
      </form>
    </div>
  );
}
