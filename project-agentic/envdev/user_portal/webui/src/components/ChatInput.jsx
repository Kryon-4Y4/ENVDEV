import { useState } from 'react';
import { Plus, Paperclip, ArrowUp } from 'lucide-react';
import './ChatInput.css';

export default function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');

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
          <div className="toolbar-left">
            <button type="button" className="toolbar-icon-btn" disabled={disabled}>
              <Plus size={18} />
            </button>
            <button type="button" className="toolbar-icon-btn" disabled={disabled}>
              <Paperclip size={18} />
            </button>
          </div>
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
