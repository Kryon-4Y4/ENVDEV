import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import './ChatInput.css';

export default function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [input]);

  function handleSubmit(e) {
    e.preventDefault();
    const message = input.trim();
    if (!message || disabled) return;
    onSend(message);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
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
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入消息，Enter 发送，Shift+Enter 换行..."
          disabled={disabled}
          rows={1}
        />
        <button
          type="submit"
          className={`send-button ${!input.trim() || disabled ? 'send-button-disabled' : ''}`}
          disabled={!input.trim() || disabled}
        >
          {disabled ? (
            <Loader2 size={20} className="spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </form>
      <p className="chat-input-hint">
        ENVDEV AI 可能会犯错，请核实重要信息。
      </p>
    </div>
  );
}
