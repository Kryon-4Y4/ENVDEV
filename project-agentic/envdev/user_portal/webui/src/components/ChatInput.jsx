import { useState } from 'react';
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
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <input
        className="chat-input"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="输入消息..."
        disabled={disabled}
      />
      <button type="submit" disabled={!input.trim() || disabled}>
        {disabled ? '发送中' : '发送'}
      </button>
    </form>
  );
}
