# ENVDEV Chatbot UI 实现提示词

## 设计美学原则

### 极简主义 (Minimalism)
- 去除一切不必要的装饰元素
- 每个像素都应有其存在的理由
- 通过留白创造呼吸感，而非填充内容

### 留白艺术 (Whitespace)
- 消息区域保持充足的上下间距
- 组件之间使用 16-24px 的标准间距
- 页面边缘保留 24-32px 的呼吸空间

### 色彩理论 (Color Theory)
- 深色背景创造沉浸感
- 青色 (Cyan) 作为唯一强调色，引导视觉焦点
- 功能色仅在必要时出现（错误、成功状态）

### 字体层次 (Typography Hierarchy)
- 消息内容使用 16px，行高 1.6，确保可读性
- 标题使用 600 字重，正文使用 400 字重
- 代码使用等宽字体，与正文形成对比

---

## 项目设计规范

### 配色方案

```css
/* 主色 - 赛博青 */
--primary: #00E5FF;
--primary-hover: #00B8D4;
--primary-active: #00838F;

/* 背景层次 */
--bg-base: #0A0E17;        /* 页面底色 */
--bg-elevated: #111827;    /* 卡片、面板 */
--bg-surface: #1A2332;     /* 输入框 */

/* 文字层次 */
--text-primary: #F0F4F8;   /* 主文字 */
--text-secondary: #94A3B8; /* 次要文字 */
--text-muted: #64748B;     /* 禁用、占位 */

/* 消息气泡 */
--bubble-user: #1E40AF;    /* 用户消息 */
--bubble-ai: #111827;      /* AI 消息 */
```

### 字体规范

```css
/* 主字体 */
font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif;

/* 字号层级 */
--text-display: 28px;  /* 欢迎标题 */
--text-h1: 22px;       /* 页面标题 */
--text-body: 16px;     /* 消息内容 */
--text-small: 14px;    /* 辅助文字 */
--text-caption: 12px;  /* 标签 */
```

---

## 项目概述

ENVDEV Chatbot Web UI 是一个基于 React 19 + Vite 的 AI 对话界面，连接 DeepSeek 大模型后端。用户可以进行流式对话，体验实时的打字机输出效果。

### 核心功能

1. **流式对话**：AI 回复逐字显示，模拟打字机效果
2. **消息历史**：展示完整的对话记录
3. **深色主题**：赛博朋克风格的沉浸式界面
4. **响应式布局**：适配桌面和平板设备

### 技术栈

- React 19
- Vite 7
- CSS Modules（或纯 CSS）
- Lucide React（图标）
- 已有后端 API：`/api/chat/stream`（SSE）

---

## 实现任务

### 任务 1：创建 CSS 变量文件

创建 `src/styles/variables.css`，包含所有设计系统的 CSS 变量。

### 任务 2：创建全局样式

创建 `src/styles/global.css`，包含：
- 重置样式
- 基础排版
- 滚动条样式（深色主题）
- 动画关键帧

### 任务 3：实现 Header 组件

创建 `src/components/Header.jsx`：
- 左侧：Logo 图标 + "ENVDEV" 标题
- 右侧：连接状态指示器（绿色脉冲点）
- 半透明毛玻璃背景效果
- 固定在页面顶部

### 任务 4：实现消息气泡组件

创建 `src/components/MessageBubble.jsx`：
- 根据 `role` 区分用户/AI 消息样式
- 用户消息：右对齐，蓝色背景，右下角圆角小
- AI 消息：左对齐，深色卡片背景，左下角圆角小
- 支持 Markdown 内容渲染（可选）
- 新消息出现时有淡入动画

### 任务 5：实现输入区域组件

创建 `src/components/ChatInput.jsx`：
- 圆角输入框，深色背景
- 聚焦时边框发光效果
- 发送按钮：青色渐变背景，hover 时发光
- 等待回复时禁用输入和按钮
- 支持 Enter 发送，Shift+Enter 换行

### 任务 6：实现欢迎页面

创建 `src/components/WelcomeScreen.jsx`：
- 无消息时显示
- 中央：Logo 图标 + "开始对话" 标题 + 副标题
- 可选：3-4 个快捷提问建议卡片

### 任务 7：实现主应用组件

重写 `src/App.jsx`：
- 组合 Header + 消息区 + 输入区
- 管理对话状态（messages, input, busy）
- 实现 SSE 流式请求逻辑
- 自动滚动到最新消息
- 空状态显示 WelcomeScreen

### 任务 8：实现加载动画

创建 `src/components/TypingIndicator.jsx`：
- 三个圆点的跳动动画
- 青色发光效果
- AI 正在思考时显示

---

## 文件结构

```
src/
├── components/
│   ├── Header.jsx
│   ├── MessageBubble.jsx
│   ├── ChatInput.jsx
│   ├── WelcomeScreen.jsx
│   └── TypingIndicator.jsx
├── styles/
│   ├── variables.css
│   └── global.css
├── App.jsx
├── App.css
├── main.jsx
└── index.css
```

---

## 关键交互细节

### 发送消息流程
1. 用户输入内容，点击发送或按 Enter
2. 输入框清空，按钮变为禁用状态
3. 用户消息出现在消息区
4. 显示加载动画（TypingIndicator）
5. AI 回复逐字出现
6. 回复完成，恢复输入状态

### 自动滚动
- 新消息出现时自动滚动到底部
- 用户手动上滚时不强制滚动
- 使用 `scrollIntoView` 或 `scrollTop` 实现

### 错误处理
- 网络错误时显示错误卡片
- 错误消息使用红色边框
- 提供"重试"按钮

---

## 视觉参考要点

### 发光效果
- 按钮 hover：`box-shadow: 0 0 15px rgba(0, 229, 255, 0.4)`
- 输入框 focus：`box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2)`
- 状态指示点：`box-shadow: 0 0 8px #10B981`

### 毛玻璃效果
```css
backdrop-filter: blur(12px);
background: rgba(17, 24, 39, 0.8);
```

### 渐变按钮
```css
background: linear-gradient(135deg, #00E5FF, #00B8D4);
```

---

## 验收标准

- [ ] 页面加载后显示深色背景，无白色闪烁
- [ ] Header 固定在顶部，滚动时内容不穿透
- [ ] 用户消息右对齐，蓝色背景
- [ ] AI 消息左对齐，深色卡片背景
- [ ] 流式输出流畅，无明显卡顿
- [ ] 输入框聚焦时有青色发光效果
- [ ] 发送按钮 hover 时有发光效果
- [ ] 空状态显示欢迎页面
- [ ] 移动端布局正常，无横向滚动
- [ ] 键盘导航（Tab、Enter）工作正常
