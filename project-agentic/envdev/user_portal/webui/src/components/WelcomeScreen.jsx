import './WelcomeScreen.css';

const suggestions = [
  '帮我用 Python 写一个快速排序算法',
  '什么是 Agentic AI？用简单的语言解释',
  '给我 5 个关于 AI 学习项目的创意',
];

export default function WelcomeScreen({ onSuggestionClick }) {
  return (
    <div className="welcome-screen">
      <h1 className="welcome-title">I'm A-K</h1>
      <p className="welcome-subtitle">Assistant to Kuangyue Huang</p>
      <div className="suggestions">
        {suggestions.map((s, i) => (
          <button
            key={i}
            className="suggestion-btn"
            onClick={() => onSuggestionClick(s)}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
