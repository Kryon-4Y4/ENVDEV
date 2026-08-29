import { useState, useRef, useEffect } from 'react';
import Header from './components/Header';
import MessageBubble from './components/MessageBubble';
import ChatInput from './components/ChatInput';
import WelcomeScreen from './components/WelcomeScreen';
import './App.css';

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
    const parts = buffer.split("\n\n");
    buffer = parts.pop();
    for (const p of parts) {
      if (!p.startsWith("data: ")) continue;
      const data = p.slice(6);
      if (data === "[DONE]") return;
      onPiece(JSON.parse(data).content);
    }
  }
}

export default function App() {
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function handleSend(text) {
    const message = text.trim();
    if (!message || busy) return;

    setBusy(true);
    setMessages((msgs) => [
      ...msgs,
      { role: "user", content: message },
    ]);

    try {
      let full = "";
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "" },
      ]);

      await streamChat(message, messages, (piece) => {
        full += piece;
        setMessages((msgs) => [
          ...msgs.slice(0, -1),
          { role: "assistant", content: full },
        ]);
      });

      if (!full) {
        setMessages((msgs) => msgs.slice(0, -1));
      }
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "请求失败：" + err.message },
      ]);
    } finally {
      setBusy(false);
    }
  }

  function handleSuggestionClick(prompt) {
    handleSend(prompt);
  }

  const hasMessages = messages.length > 0;

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        {!hasMessages ? (
          <WelcomeScreen onSuggestionClick={handleSuggestionClick} />
        ) : (
          <div className="chat-area">
            <div className="messages-container">
              {messages.map((m, i) => (
                m.content ? <MessageBubble key={i} role={m.role} content={m.content} /> : null
              ))}
              <div ref={chatEndRef} />
            </div>
          </div>
        )}
      </main>
      <ChatInput onSend={handleSend} disabled={busy} />
    </div>
  );
}
