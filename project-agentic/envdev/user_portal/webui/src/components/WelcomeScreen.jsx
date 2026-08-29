import './WelcomeScreen.css';

const suggestions = [
  '分析 2025 赛季 F1 车手积分榜走势',
  '对比红牛和法拉利赛车的空气动力学设计差异',
  '预测下一站 F1 大奖赛的冠军归属',
];

export default function WelcomeScreen({ onSuggestionClick }) {
  return (
    <div className="welcome-screen">
      <h1 className="welcome-title">I'm A-K</h1>
      <p className="welcome-subtitle">I'm A-K, assistant to Kuangyue Huang, F1 Analyst.</p>
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
