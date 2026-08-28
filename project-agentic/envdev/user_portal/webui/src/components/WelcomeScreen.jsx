import { Sparkles, Code, BookOpen, Lightbulb } from 'lucide-react';
import './WelcomeScreen.css';

const suggestions = [
  {
    icon: <Code size={20} />,
    title: '编写代码',
    prompt: '帮我用 Python 写一个快速排序算法',
  },
  {
    icon: <BookOpen size={20} />,
    title: '解释概念',
    prompt: '什么是 Agentic AI？用简单的语言解释',
  },
  {
    icon: <Lightbulb size={20} />,
    title: '头脑风暴',
    prompt: '给我 5 个关于 AI 学习项目的创意',
  },
];

export default function WelcomeScreen({ onSuggestionClick }) {
  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <div className="welcome-logo">
          <Sparkles size={40} strokeWidth={1.5} />
        </div>
        <h1 className="welcome-title">开始对话</h1>
        <p className="welcome-subtitle">
          我是 ENVDEV AI 助手，有什么可以帮你的？
        </p>
      </div>
      <div className="suggestions-grid">
        {suggestions.map((s, i) => (
          <button
            key={i}
            className="suggestion-card"
            onClick={() => onSuggestionClick(s.prompt)}
          >
            <div className="suggestion-icon">{s.icon}</div>
            <span className="suggestion-title">{s.title}</span>
            <span className="suggestion-prompt">{s.prompt}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
