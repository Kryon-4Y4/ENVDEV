import { useState, useRef, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';
import './ChatInput.css';

export default function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }, [input]);

  function handleSubmit(e) {
    e.preventDefault();
    const message = input.trim();
    if (!message || disabled) return;
    onSend(message);
    setInput('');
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <div className="chat-input-wrapper">
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className="chat-textarea"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入消息..."
          disabled={disabled}
          rows={1}
        />
        <div className="chat-input-divider"></div>
        <div className="chat-input-toolbar">
          <button
            type="submit"
            className="send-btn"
            disabled={!input.trim() || disabled}
            title="发送"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </form>
    </div>
  );
}
