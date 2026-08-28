import { Bot } from 'lucide-react';
import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <div className="header-logo">
          <Bot size={24} strokeWidth={2} />
        </div>
        <span className="header-title">ENVDEV</span>
        <span className="header-subtitle">AI Chat</span>
      </div>
      <div className="header-right">
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span className="status-text">已连接</span>
        </div>
      </div>
    </header>
  );
}
