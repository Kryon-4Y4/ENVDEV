# ENVDEV Chatbot UI 设计系统

## 设计理念

**赛博极简 (Cyber Minimalism)**：在深色画布上，用克制的发光元素和精确的排版构建科技感。
灵感来源：终端界面的效率 + 科幻 UI 的视觉张力 + 现代 SaaS 产品的易用性。

---

## 1. 色彩系统 (Color Palette)

### 1.1 主色 (Primary)

| 名称 | 色值 | 用途 |
|------|------|------|
| Cyan Glow | `#00E5FF` | 主色调，按钮、链接、聚焦态 |
| Cyan Deep | `#00B8D4` | hover 状态、次要强调 |
| Cyan Dark | `#00838F` | 按下状态、深色变体 |

### 1.2 背景色 (Backgrounds)

| 名称 | 色值 | 用途 |
|------|------|------|
| Void Black | `#0A0E17` | 页面主背景 |
| Deep Space | `#111827` | 卡片/面板背景 |
| Dark Surface | `#1A2332` | 输入框、次级面板 |
| Elevated | `#243044` | hover 状态、弹出层 |

### 1.3 文字色 (Text)

| 名称 | 色值 | 用途 |
|------|------|------|
| Star White | `#F0F4F8` | 主文字 |
| Moon Gray | `#94A3B8` | 次要文字、占位符 |
| Nebula Gray | `#64748B` | 禁用文字、分割线 |

### 1.4 功能色 (Functional)

| 名称 | 色值 | 用途 |
|------|------|------|
| Success Green | `#10B981` | 成功状态、连接正常 |
| Error Red | `#EF4444` | 错误提示 |
| Warning Amber | `#F59E0B` | 警告提示 |
| Info Blue | `#3B82F6` | 信息提示 |

### 1.5 用户消息色 (User Message)

| 名称 | 色值 | 用途 |
|------|------|------|
| User Bubble | `#1E40AF` | 用户消息气泡背景 |
| User Bubble Hover | `#1E3A8A` | hover 变体 |

### 1.6 发光效果 (Glow Effects)

```css
/* 主色发光 */
--glow-primary: 0 0 20px rgba(0, 229, 255, 0.3);
--glow-primary-strong: 0 0 30px rgba(0, 229, 255, 0.5);

/* 按钮发光 */
--glow-button: 0 0 15px rgba(0, 229, 255, 0.4);

/* 输入框聚焦发光 */
--glow-input-focus: 0 0 0 2px rgba(0, 229, 255, 0.2);
```

---

## 2. 字体系统 (Typography)

### 2.1 字体族 (Font Families)

```css
/* 主字体：系统字体栈，确保跨平台一致性 */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC',
             'Microsoft YaHei', 'Segoe UI', sans-serif;

/* 等宽字体：代码、技术内容 */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
```

### 2.2 字号层级 (Type Scale)

| 层级 | 大小 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| Display | 28px | 1.3 | 700 | 欢迎页标题 |
| H1 | 22px | 1.4 | 600 | 页面标题 |
| H2 | 18px | 1.4 | 600 | 区域标题 |
| Body Large | 16px | 1.6 | 400 | 消息内容 |
| Body | 15px | 1.6 | 400 | 常规文字 |
| Body Small | 14px | 1.5 | 400 | 次要文字 |
| Caption | 12px | 1.4 | 400 | 标签、时间戳 |

### 2.3 文字样式示例

```css
/* 消息正文 */
.message-text {
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.6;
  color: var(--star-white);
}

/* 代码块 */
.code-block {
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.5;
  color: var(--cyan-glow);
}
```

---

## 3. 组件样式 (Component Styles)

### 3.1 按钮 (Buttons)

#### 主要按钮 (Primary Button)

```css
.btn-primary {
  background: linear-gradient(135deg, var(--cyan-glow), var(--cyan-deep));
  color: var(--void-black);
  border: none;
  border-radius: 10px;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  box-shadow: var(--glow-button);
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}
```

#### 幽灵按钮 (Ghost Button)

```css
.btn-ghost {
  background: transparent;
  color: var(--cyan-glow);
  border: 1px solid var(--cyan-glow);
  border-radius: 10px;
  padding: 12px 24px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-ghost:hover {
  background: rgba(0, 229, 255, 0.1);
}
```

### 3.2 输入框 (Input)

```css
.input {
  background: var(--dark-surface);
  border: 1px solid var(--nebula-gray);
  border-radius: 12px;
  padding: 14px 18px;
  font-size: 15px;
  color: var(--star-white);
  transition: all 0.2s ease;
}

.input::placeholder {
  color: var(--moon-gray);
}

.input:focus {
  outline: none;
  border-color: var(--cyan-glow);
  box-shadow: var(--glow-input-focus);
}

.input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

### 3.3 消息气泡 (Message Bubbles)

#### 用户消息

```css
.message-user {
  background: var(--user-bubble);
  color: var(--star-white);
  border-radius: 18px 18px 4px 18px;
  padding: 14px 18px;
  margin-left: auto;
  max-width: 75%;
}
```

#### AI 消息

```css
.message-assistant {
  background: var(--deep-space);
  border: 1px solid rgba(100, 116, 139, 0.3);
  color: var(--star-white);
  border-radius: 18px 18px 18px 4px;
  padding: 14px 18px;
  margin-right: auto;
  max-width: 75%;
}
```

### 3.4 卡片 (Cards)

```css
.card {
  background: var(--deep-space);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 16px;
  padding: 20px;
}

.card-hover:hover {
  border-color: rgba(0, 229, 255, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
```

### 3.5 Header

```css
.header {
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(100, 116, 139, 0.2);
  padding: 16px 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

### 3.6 状态指示器 (Status Indicator)

```css
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success-green);
  box-shadow: 0 0 8px var(--success-green);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### 3.7 加载动画 (Loading Animation)

```css
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--cyan-glow);
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-8px); opacity: 1; }
}
```

---

## 4. 间距系统 (Spacing Scale)

基于 4px 网格系统：

| Token | 值 | 用途 |
|-------|------|------|
| space-1 | 4px | 紧凑间距 |
| space-2 | 8px | 元素内间距 |
| space-3 | 12px | 小间距 |
| space-4 | 16px | 标准间距 |
| space-5 | 20px | 组件内边距 |
| space-6 | 24px | 区域间距 |
| space-8 | 32px | 大间距 |
| space-10 | 40px | 区块间距 |
| space-12 | 48px | 页面边距 |

---

## 5. 圆角系统 (Border Radius)

| Token | 值 | 用途 |
|-------|------|------|
| radius-sm | 6px | 小元素、标签 |
| radius-md | 10px | 按钮、输入框 |
| radius-lg | 14px | 卡片 |
| radius-xl | 18px | 消息气泡 |
| radius-full | 9999px | 圆形、胶囊 |

---

## 6. 阴影系统 (Shadows)

```css
/* 层级 1：轻微浮起 */
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);

/* 层级 2：卡片 */
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);

/* 层级 3：弹出层 */
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.4);

/* 层级 4：模态框 */
--shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.5);
```

---

## 7. 动效系统 (Animations)

### 7.1 时长 (Durations)

| Token | 值 | 用途 |
|-------|------|------|
| duration-fast | 100ms | 微交互 |
| duration-normal | 200ms | 标准过渡 |
| duration-slow | 300ms | 复杂动画 |

### 7.2 缓动函数 (Easing)

```css
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### 7.3 预设动画

```css
/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 从下滑入 */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 消息出现 */
.message-enter {
  animation: slideUp 0.3s var(--ease-out);
}
```

---

## 8. 图标 (Icons)

使用 **Lucide React** 图标库，保持线条简洁、风格统一。

### 推荐图标

| 用途 | 图标名 |
|------|--------|
| 发送 | `Send` / `ArrowUp` |
| 设置 | `Settings` |
| 清空对话 | `Trash2` |
| 复制 | `Copy` |
| 刷新 | `RefreshCw` |
| 用户 | `User` |
| AI 助手 | `Bot` / `Sparkles` |
| 错误 | `AlertCircle` |
| 加载 | `Loader2` (旋转) |

### 图标样式

```css
.icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
  color: currentColor;
}

.icon-glow {
  filter: drop-shadow(0 0 4px currentColor);
}
```

---

## 9. 响应式断点 (Breakpoints)

```css
/* 移动端 */
--breakpoint-sm: 640px;

/* 平板 */
--breakpoint-md: 768px;

/* 小桌面 */
--breakpoint-lg: 1024px;

/* 大桌面 */
--breakpoint-xl: 1280px;
```

### 布局适配

| 设备 | 消息区最大宽度 | 内边距 |
|------|--------------|--------|
| 移动端 (<640px) | 100% | 16px |
| 平板 (640-1024px) | 640px | 24px |
| 桌面 (>1024px) | 768px | 32px |

---

## 10. 无障碍 (Accessibility)

### 对比度要求

- 正文文字：至少 4.5:1（WCAG AA）
- 大标题：至少 3:1
- 交互元素：至少 3:1

### 焦点样式

```css
:focus-visible {
  outline: 2px solid var(--cyan-glow);
  outline-offset: 2px;
}
```

### 键盘导航

- Tab 顺序：Logo → 对话区 → 输入框 → 发送按钮
- Enter：发送消息
- Shift+Enter：换行
- Escape：取消操作（如有弹窗）

---

## 11. CSS 变量汇总

```css
:root {
  /* 主色 */
  --cyan-glow: #00E5FF;
  --cyan-deep: #00B8D4;
  --cyan-dark: #00838F;

  /* 背景 */
  --void-black: #0A0E17;
  --deep-space: #111827;
  --dark-surface: #1A2332;
  --elevated: #243044;

  /* 文字 */
  --star-white: #F0F4F8;
  --moon-gray: #94A3B8;
  --nebula-gray: #64748B;

  /* 功能色 */
  --success-green: #10B981;
  --error-red: #EF4444;
  --warning-amber: #F59E0B;
  --info-blue: #3B82F6;

  /* 用户消息 */
  --user-bubble: #1E40AF;

  /* 发光 */
  --glow-primary: 0 0 20px rgba(0, 229, 255, 0.3);
  --glow-button: 0 0 15px rgba(0, 229, 255, 0.4);
  --glow-input-focus: 0 0 0 2px rgba(0, 229, 255, 0.2);

  /* 字体 */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* 圆角 */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;

  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.4);

  /* 动效 */
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```
