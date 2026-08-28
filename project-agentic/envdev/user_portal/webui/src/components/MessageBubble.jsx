import { User, Bot } from 'lucide-react';
import './MessageBubble.css';

export default function MessageBubble({ role, content }) {
  const isUser = role === 'user';

  return (
    <div className={`message-row ${isUser ? 'message-row-user' : 'message-row-assistant'}`}>
      <div className={`message-avatar ${isUser ? 'avatar-user' : 'avatar-ai'}`}>
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>
      <div className={`message-bubble ${isUser ? 'bubble-user' : 'bubble-ai'}`}>
        <div className="message-content">{content}</div>
      </div>
    </div>
  );
}
