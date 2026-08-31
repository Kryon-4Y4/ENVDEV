整理时间：2026-08-26（08-30 更新）

---
## 目录

- [一、项目结构](#sec-1) —— 微服务风格布局、包命名规则、文件职责、config vs pyproject
- [二、开发环境](#sec-2) —— .venv 原理、editable 安装机制、macOS 陷阱排查
- [三、Shell 基础](#sec-3) —— PATH、管道、常用命令
- [四、API 调用链路](#sec-4) —— base_url 时序关系
- [五、ChatBot 实现](#sec-5) —— 最小调用示例与要点
- [六、多端架构](#sec-6) —— Core/Server/UI、CORS、FastAPI、流式输出、React 前端、GUI 打包、移动端
- [七、Agent 人设与技能](#sec-7) —— AGENT.md vs Skill.md、二维码等宽渲染、ChatBot UI 渲染限制
- [八、CI/CD 部署](#sec-8) —— GitHub + Vercel + Railway 全链路

<a id="sec-1"></a>

## 一、项目结构

### 1.1 工程结构（内外两层 + 微服务风格域）

* 外层是**学习框架**（笔记、参考资料、实验场）
* 内层 `projects/project-agentic/` 是**项目框架**（可独立打包发布）。
* 包内按“领域”划分，保留微服务风格的长期规划骨架。

```
ENVDEV/                                # 学习框架（外层）
├── notes/ data/ jupyter-notebook/ tests/   # 学习笔记 / 数据 / 实验 / 测试
├── awesome-agentic-ai-zh/             # 参考仓库（克隆）
├── .env / .env.example / .venv/       # 环境变量 / 模板 / 虚拟环境（均在根目录）
└── projects/project-agentic/            # 项目框架（内层，可独立打包）
    ├── AGENT.md                       # Agent 人设（被 core 读入 system prompt）
    ├── pyproject.toml / uv.lock       # 打包配置 / 依赖锁定（where = ["."]）
    └── envdev/                        # 主代码包（包名必须小写合法）
        ├── __init__.py / __main__.py  # 包标识 / python -m envdev 入口
        ├── config.py                  # 运行时配置（settings 单例）
        ├── core/                      # 核心域：prompt 组装 + LLM 调用（被import）
        │   ├── core.py / skill/       # PROJECT_ROOT = projects/project-agentic
        ├── api_gateway/               # API 域：FastAPI 服务（:8001）
        ├── user_portal/               # 用户域：面向用户的各端
        │   ├── cli/main.py            #   终端 REPL（python -m envdev）
        │   ├── gui/main.py            #   桌面窗口（Tkinter，可打包成独立应用）
        │   ├── webui/                 #   React 前端工程（Vite，开发 :5173）
        │   └── mobile_app/            #   手机 APP（React Native，真机扫码运行）
        │   # 未来域（占位）：task_scheduler / crawler / ops-center / admin_console / data_layer / docu
```

**包命名规则**（血泪教训）：

| 规则 | 说明 |
|------|------|
| 连字符不能当包名 | `from envdev.api-gateway.server import ...` 会被解析为减号 → SyntaxError；微服务风格目录真要住代码时改下划线 `api_gateway` |
| 空占位目录 | Git 不跟踪空目录，需放 `.gitkeep`；连字符占位域将来进代码时再改名 |
| 目录搬家后 | 必须重新 `pip install -e 新路径/`（详见 2.2） |

### 1.2 各文件职责

| 文件 | 职责 |
|------|------|
| `__init__.py` | 包标识；`core/__init__.py` 额外做**再导出**，各端统一写 `from envdev.core import ...` |
| `__main__.py` | `python -m envdev` 的入口，转发到 `user_portal.cli.main.main()` |
| `config.py` | 从 `.env` 加载 API 密钥等配置，提供 `settings` 单例 |
| `core/core.py` | 业务核心：读 AGENT.md + skill 组装 system prompt，封装 LLM 调用，各端共用 |
| `api_gateway/server.py` | FastAPI 纯 API 端（不托管页面），见第六章 |
| `user_portal/cli/main.py` | 终端多轮对话 REPL |
| `user_portal/gui/main.py` | 桌面窗口聊天（Tkinter 标准库，直调 core，见 6.7） |
| `user_portal/mobile_app/` | 手机 APP（Expo + React Native）：`npx expo start` 出二维码，手机装 Expo Go 扫码运行，见 6.8 |
| `user_portal/webui/` | React 前端工程（Vite）：`npm run dev` 开发，`npm run build` 产出 `dist/` |
| `pyproject.toml` | 替代传统 `setup.py`，定义包名、版本、依赖、构建系统；`packages.find where` 必须与实际源码位置一致 |
| `.env` | 存放 LLM API 密钥等敏感信息（**不提交 Git**） |
| `.env.example` | 只含变量名不含值，供他人参考格式（**提交 Git**） |
| `uv.lock` | 精确记录每个依赖的版本和哈希 |

### 1.3 config.py vs pyproject.toml

一句话：**`pyproject.toml` 管“项目怎么装”，`config.py` 管“程序怎么跑”。**

| 维度 | `pyproject.toml` | `config.py` |
|------|------------------|-------------|
| 本质 | 项目元数据 / 打包配置 | 应用运行时配置模块 |
| 格式 | TOML（声明式，不可执行） | Python（可执行代码） |
| 给谁读 | `pip`/`setuptools` 等工具 | Python 代码（`settings`） |
| 生效时机 | 安装 / 构建时 | 程序运行时 |
| 内容 | 依赖、版本、构建系统 | API key、模型名等变量值 |
| 敏感信息 | 无（提交 Git） | 间接读 `.env` 密钥 |

协作关系：`pyproject.toml` 声明依赖 → `pip install` 装好 → `config.py` 用 `load_dotenv()` 读 `.env` → 生成 `settings` 供代码使用。

---

<a id="sec-2"></a>

## 二、开发环境

### 2.1 Python 虚拟环境（.venv）

#### 目录结构

```
.venv/
├── bin/                        # 可执行文件 + 激活脚本
│   ├── activate                #   bash/zsh 激活脚本
│   ├── activate.csh / .fish    #   其他 Shell 激活脚本
│   ├── Activate.ps1            #   PowerShell 激活脚本
│   ├── python -> python3.14    #   解释器软链接 → 系统 Python
│   ├── pip / pip3              #   包管理工具
│   └── pytest / ipython ...    #   安装的 CLI 工具
├── lib/python3.14/
│   └── site-packages/          # 第三方包安装位置（隔离区）
├── include/                    # C 扩展头文件
├── share/                      # 共享资源（man pages 等）
├── pyvenv.cfg                  # 虚拟环境配置
└── .gitignore                  # 内容为 *，忽略全部
```

#### 隔离原理

激活虚拟环境的本质是**修改 `PATH` 环境变量**：

```
# 激活前
PATH = /usr/local/bin:/usr/bin:/bin:...

# source .venv/bin/activate 后
PATH = /path/to/.venv/bin:/usr/local/bin:/usr/bin:/bin:...
```

`python`、`pip` 等命令优先找到虚拟环境中的版本，实现依赖隔离。退出时 `deactivate` 恢复原 `PATH`。

---

<a id="sec-3"></a>

## 三、Shell 基础

### 3.1 Shell 是什么

**Shell** 是命令行解释器：用户输入命令 → Shell 解析 → 内核执行。

| Shell | 特点 |
|-------|------|
| `sh` | 1977 元老 |
| `bash` | Linux 默认 |
| `zsh` | macOS 默认，bash 超集，智能补全更强 |

### 3.2 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **PATH** | 命令搜索路径，`:` 分隔 | `export PATH="/opt/homebrew/bin:$PATH"` |
| **配置文件** | `.zshrc`（zsh）/ `.bashrc`（bash） | `source ~/.zshrc` 修改后立即生效 |
| **管道** | `\|`：左边输出作为右边输入 | `grep error log \| head -5` |
| **重定向** | `>` 覆盖 / `>>` 追加 | `python run.py > output.txt` |
| **退出码** | `$?`：0=成功，非0=失败 | `cmd && echo ok \|\| echo fail` |
| **引号** | `'` 原样 / `"` 解析变量 / `` ` `` 执行命令 | `echo "$HOME"` → `/Users/...` |

### 3.3 常用命令

| 操作 | 命令 |
|------|------|
| 文件列表 | `ls -la` |
| 递归建目录 | `mkdir -p a/b/c` |
| 实时看日志 | `tail -f log` |
| 查进程 | `ps aux \| grep python` |
| 激活虚拟环境 | `source .venv/bin/activate` |
| 退出虚拟环境 | `deactivate` |
| 命令位置 | `which python` |
| 历史搜索 | `Ctrl + R` |
| 行首/行尾 | `Ctrl + A` / `Ctrl + E` |

### 3.4 同类工具一览

| 类别 | 工具 |
|------|------|
| 其他 Shell | **fish**（开箱即用）、**PowerShell**（微软）、**Nushell**（结构化数据）、**xonsh**（Python 语法） |
| 终端模拟器 | **iTerm2**（macOS 增强）、**Warp**（AI 现代终端）、**Ghostty**（GPU 加速）、**VS Code 内置终端** |
| 增强神器 | **oh-my-zsh**（框架）、**fzf**（模糊搜索）、**zoxide**（智能跳转）、**tmux**（多会话）、**eza/bat/fd**（ls/cat/find 替代） |

---

<a id="sec-4"></a>

## 四、API 调用链路

### 4.1 base_url 时序关系

以 DeepSeek 的 Anthropic 兼容接口为例，请求从程序到模型的完整链路：

```
App --> SDK --> BASE(DeepSeek) --> MODEL
```

**要点**：SDK 是"打包工具"，`base_url` 是"发货地址"——SDK 把请求按 Anthropic 格式打包，发到 `base_url` 指定的地址，该地址的服务器能看懂 Anthropic 格式并调用底层模型。

---

<a id="sec-5"></a>

## 五、ChatBot 实现

### 5.1 最小调用示例（业务核心 `core/core.py`）

通过 **OpenAI 兼容客户端**调用 DeepSeek，读入 `AGENT.md` 人设 + skill 组装 system 消息，三端（终端 / API / 前端）共用：

```python
def build_system_prompt() -> str:
"""组装 system 提示：AGENT.md 人设 + skill 技能。"""
rules=(PROJECT_ROOT/"AGENT.md").read_text(encoding="utf-8")
skill=(SKILL_DIR/"hello_skill"/"skill.md").read_text(encoding="utf-8")
return(
f"【项目指引 AGENT.md】\n{rules}\n\n"
f"【技能 skill.md】\n{skill}\n\n"
"当用户意图匹配技能触发条件时，严格按技能指令执行。"
)

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

def chat(messages: list) -> str:
"""调用 LLM 并返回模型回复。
 messages 为完整对话历史（含 system 人设），由调用方负责维护。
 """
msg=client.chat.completions.create(
model=settings.LLM_MODEL,
messages=messages,
)
returnmsg.choices[0].message.content
```

```python
#定义的是一个**类**——但它是种特殊的类：**数据模型**（用来描述"请求长什么样"），里面没有方法，只有字段声明：
classChatRequest(BaseModel):
"""请求体：本轮消息 + 历史对话。"""
message: str
history: list=[]# [{"role": "user"/"assistant", "content": "..."}, ...]
# @app.post("/api/chat") 是路由注册 这行叫装饰器（@ 开头），作用是给下面的函数"挂牌"： 
# 当有人向 POST http://127.0.0.1:8000/api/chat 发请求时，就调用下面的 api_chat() 函数。

@app.post("/api/chat")
def api_chat(req: ChatRequest) -> dict:
"""聊天接口：组装消息 → 调核心逻辑 → 返回模型回复。"""
"""系统提示词+用户历史消息+用户最新消息"""

messages=[{"role": "system","content": build_system_prompt()}]
messages+=req.history

messages.append({"role": "user","content": req.message})
return {"reply": chat(messages)}

```

```python
front.py

def main() -> None:
"""启动静态文件服务：访问 / 自动返回 static/index.html。"""
handler=functools.partial(
http.server.SimpleHTTPRequestHandler,directory=str(STATIC_DIR)
)
withhttp.server.ThreadingHTTPServer((HOST,PORT),handler)ashttpd:
print(f"前端页面：http://{HOST}:{PORT}（需同时启动后端 API：:8000）")
httpd.serve_forever()
```

```html
index.html
  
<script>
// 历史累积：本轮问答都存进去
history.push({ role:"user", content:message });
history.push({ role:"assistant", content:reply });
</script> 
```

### 5.2 关键步骤

| 步骤 | 作用 |
|------|------|
| `PROJECT_ROOT` | 基于 `__file__` 定位项目根，任意目录运行都可用 |
| 读 `AGENT.md` | 取出人设文本 |
| 注入 system | 人设塞进 system 消息，随请求发给模型 |
| `chat.completions.create` | 调用 DeepSeek 聊天接口，取回回复 |

### 5.3 要点

- 用 **OpenAI 兼容客户端**调 DeepSeek：`base_url="https://api.deepseek.com"`
- API key 从 `.env` 的 `DEEPSEEK_API_KEY` 读取（经 `settings` 单例）
- 模型名用 `settings.LLM_MODEL`，不写死
- 入口守卫 `if __name__ == "__main__"`：模块被 import 时 `__name__` 是模块名，守卫不触发；多个入口文件都有守卫也不冲突，只有被直接运行的那个才执行 `main()`
- 区分两个交互界面：**Shell**（`$` 提示符，敲命令）与 **Python REPL**（`>>>` 提示符，只能写 Python 代码）——在 `>>>` 里敲 `python -m xxx` 会报 SyntaxError；退出 REPL 用 `exit()`

---

<a id="sec-6"></a>

## 六、多端架构（前后端分离 + 本地直调）

### 6.1 快速开始

前提：项目根目录（ENVDEV/）下，每个终端先激活虚拟环境：`source .venv/bin/activate`

| 终端    | 命令                                                           | 效果                               |
| ----- | ------------------------------------------------------------ | -------------------------------- |
| API   | `python -m envdev.api_gateway.server`                        | API 服务 :8001（文档 :8001/docs）      |
| WebUI | `cd projects/project-agentic/envdev/user_portal/webui && npm run dev` | React 聊天页 :5173（代理 /api → :8001） |
| CLI   | `python -m envdev`                                           | 终端对话，`exit` 退出                   |
| GUI   | `python -m envdev.user_portal.gui.main`                      | 桌面窗口，直调 core，不依赖上面任何服务           |
| App   | `cd envdev/user_portal/mobile_app && npx expo start --lan`   | 二维码，手机装 Expo Go 扫码运行（需同一 WiFi）   |

### 6.2 一句话本质

**Core 是库（被 import，不是独立进程），其余各端是独立进程**。分两类：Server/UI 隔着浏览器沙箱必须走 HTTP；CLI/GUI 与 core 同机同语言，直接 import（本地直调，无端口）：

| 层      | 代码                              | 形态                     | 端口    |
| ------ | ------------------------------- | ---------------------- | ----- |
| Core   | `core/core.py`                  | 业务库（被 import）          | 无     |
| Server | `api_gateway/server.py`         | FastAPI 纯 API，不托管页面    | :8001 |
| WebUI  | `user_portal/webui/`（React 工程）  | 开发：Vite 服务器（走 HTTP，被迫） | :5173 |
| CLI    | `user_portal/cli/main.py`       | 终端 REPL（直接调 core）      | 无     |
| GUI    | `user_portal/gui/main.py`       | 桌面窗口（直接调 core）         | 无     |
| Mobile | `user_portal/mobile_app/App.js` | 手机原生渲染（走 HTTP，跨设备）     | 无     |

### 6.3 启动命令

```bash
python -m envdev                          # 终端版（CLI）
python -m envdev.api_gateway.server       # API 端 :8001（API 文档：:8001/docs）
cd envdev/user_portal/webui && npm run dev   # 前端 React 版 :5173（代理 /api → :8001）
python -m envdev.user_portal.gui.main     # GUI 桌面窗口（直调 core，无需起其它服务）
cd envdev/user_portal/mobile_app && npx expo start --lan   # 手机端（手机装 Expo Go 扫码）
```

### 6.4 FastAPI 三个核心概念（server.py）

| 概念 | 说明 |
|------|------|
| `class ChatRequest(BaseModel)` | **数据模型类**（不是方法）：只有字段声明没有方法，描述“请求体长什么样”，FastAPI 自动校验 + 生成文档 |
| `@app.post("/api/chat")` | **装饰器“挂牌”**：把函数注册到 POST /api/chat 路由，请求到达时自动调用 |
| `if __name__ == "__main__": uvicorn.run(...)` | 入口守卫：`python -m envdev.api_gateway.server` 直接运行时才启动服务 |

### 6.5 流式输出（Streaming）

**一句话本质**：`stream=True` 把“等模型写完一次性返回”变成“模型每吐一小块就立刻送达”。SDK 返回值从完整消息变为**生成器**，增量文本在 `chunk.choices[0].delta.content`。

**四层联动**（本项目已实现，`/api/chat` 非流式与 `/api/chat/stream` 共存）：

| 层 | 做法 |
|----|------|
| Core | `chat_stream()` 生成器：`create(stream=True)`，逐块 `yield delta.content` |
| CLI | 边收边打：`print(piece, end="", flush=True)`，同时拼接完整文本存历史 |
| API | FastAPI `StreamingResponse` + SSE 格式（`data: {...}\n\n`，`[DONE]` 为结束信号） |
| 前端 | `fetch` + `res.body.getReader()` 逐块读，按 `\n\n` 切分，增量渲染气泡 |

**CLI 端示例**：

```python
print("🤖: ", end="", flush=True)   # flush：不等换行立即刷出（否则缓冲区看不到打字机效果）
reply = ""
for piece in chat_stream(messages):
    print(piece, end="", flush=True)
    reply += piece                    # 流式只是传输形态，历史必须存完整文本
```

**API 端 SSE**：

```python
def generate():
    for piece in chat_stream(messages):
        yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
    yield "data: [DONE]\n\n"          # 结束信号（沿用 OpenAI 惯例）

return StreamingResponse(generate(), media_type="text/event-stream")
```

**前端读取要点**：先挂空气泡 → `reader.read()` 循环 → 缓冲按 `\n\n` 切（一次 read 的字节与消息边界不对齐，最后不完整的半段留到下轮）→ `bubble.textContent = full` 增量刷新。

### 6.6 前端工程化（Vite + React）

**一句话本质**：**React 是“写界面的库”（声明式），Vite 是“跑和打包的工具链”**——不是同一层的东西；React 代码（JSX）浏览器看不懂，靠 Vite 开发时实时编译、上线时打包成纯静态文件。**后端完全不动**（只认 HTTP + SSE）。

**工程结构**（`projects/project-agentic/envdev/user_portal/webui/`，前端工程住在用户域包里；打包无虞：`find_packages` 只认 `__init__.py`，node_modules 不会混入）：

| 文件 | 职责 |
|------|------|
| `package.json` | 项目清单：依赖 + 脚本命令（类比 `pyproject.toml`） |
| `node_modules/` | 依赖存放处，体积巨大必须 gitignore（类比 `.venv` 的 site-packages） |
| `vite.config.js` | React 插件 + 开发代理（`/api` → :8001） |
| `index.html` | 只含 `#root` 挂载点 + 入口脚本引用 |
| `src/main.jsx` | 入口：把 App 组件挂到 #root |
| `src/App.jsx` | 主组件：聊天界面 + `streamChat` 流式逻辑 |
| `src/App.css` | 样式 |

**npm 命令对照 pip**：

| 前端 | Python 对应 | 作用 |
|------|-------------|------|
| `npm install` | `pip install` | 装依赖（国内加 `--registry=https://registry.npmmirror.com`） |
| `npm run dev` | `uvicorn --reload` | 开发服务器 :5173，改代码浏览器自动刷新（热更新） |
| `npm run build` | 打包产出 | 产出 `dist/` 纯静态文件，`npm run preview` 可本地预览 |

**React 四个核心概念**（对照旧版原生 JS 写法）：

| 概念 | 说明 | 旧写法对照 |
|------|------|-----------|
| 组件 | 返回界面的函数（`MessageBubble`） | `append()` 手动建 DOM |
| JSX | JS 里写 HTML（`class` → `className`） | 模板字符串拼 HTML |
| `useState` | 数据一变界面自动重渲染（声明式） | `appendChild` / `textContent` 命令式操作 |
| props | 组件参数（`<MessageBubble role=... />`） | 函数传参 |

**启动**（需先起后端 `api_gateway.server`）：

```bash
cd projects/project-agentic/envdev/user_portal/webui
npm install                          # 首次（装依赖）
npm run dev                          # 开发：:5173（代理 /api → :8001）
npm run build && npm run preview     # 生产：构建后本地预览 dist/
```

### 6.7 GUI 端与打包发布（PyInstaller）

**GUI 端**（`user_portal/gui/main.py`，Tkinter 标准库零依赖）与 CLI 同属本地直调端：直接 `from envdev.core import chat_stream`，不走 HTTP、无需起 API 端。判断口诀：**能 import 就不 HTTP，不能见面才分离**（webui 走 HTTP 是因为浏览器沙箱里没法跑 Python，被迫）。流式实现：后台线程把流式增量塞进 `queue`，主线程用 `window.after(50ms)` 轮询取出渲染——Tkinter 只允许主线程操作控件，与 Web 端“事件循环不阻塞”是同一思想。

**打包**（PyInstaller：把 Python 解释器 + 依赖 + 你的代码装进一个应用，目标机器无需装 Python）：

```bash
source .venv/bin/activate            # 必须：PyInstaller 靠 PYTHONPATH 找 editable 安装的 envdev
cd projects/project-agentic
pyinstaller --name ENVDEV --windowed --collect-all envdev envdev/user_portal/gui/main.py
```

交付 = `dist/ENVDEV-GUI/`：`ENVDEV.app`（123M）+ 外置配置三件套 `.env / AGENT.md / skill/`。配置外置的好处：改人设/密钥无需重新打包，双击启动不依赖 cwd。

**路径双模式兼容**（打包改造的关键）：代码用 `sys.frozen` 分流——打包态去 `.app` 所在目录找配置（macOS 的 app 是三层深的文件夹套装 `ENVDEV.app/Contents/MacOS/`，`sys.executable` 同目录 ≠ 交付目录），开发态保持 `__file__` 定位。判断 .app 层用 `p.endswith(".app")`（`".app" in parts` 匹配不上 `"ENVDEV.app"`）。

### 6.8 移动端（Expo / React Native）

**一句话本质**：React Native = 用 React 的写法渲染**手机原生控件**；
Expo = 跑和预览 RN 的工具链（对照 Vite 之于 React）。
mobile_app 是首个**跨设备端**——手机与后端无法互相 import，必须走 HTTP；
但 RN 发的是原生网络请求，不经浏览器沙箱，
**因此无需 CORS**（CORS 管的是“浏览器里的代码”，不是“跨域”本身）。

**与 webui 的四点差异**：

| | webui（浏览器） | mobile_app（手机） |
|--|----------------|-------------------|
| 控件 | `div` / `span` / `input` | `View` / `Text` / `TextInput` |
| 样式 | CSS | `StyleSheet.create`（JS 对象） |
| HTTP | 受 CORS 约束 | 原生请求，无 CORS |
| API 地址 | 相对路径 `/api`（Vite 代理） | 必须写 Mac 的**局域网 IP**（`127.0.0.1` 在手机上指手机自己） |

**启动链路**（手机与 Mac 同一 WiFi）：

```bash
ipconfig getifaddr en0                       # 查 Mac 局域网 IP，填进 App.js 的 API_BASE
python -m envdev.api_gateway.server          # API 端（0.0.0.0:8001，允许局域网访问）
cd envdev/user_portal/mobile_app && npx expo start --lan   # 出二维码（Metro :8081）
# 手机端：装 Expo Go → 扫二维码（iPhone 可直接用系统相机）
```

代码留在 Mac 上（Metro 打包器实时推送 JS），手机只做原生渲染——改 `App.js` 保存，手机自动热重载。当前用非流式 `/api/chat`（RN 的 `fetch` 读流支持不稳，流式进阶用 `react-native-sse`）。

**三个坑**：

| 坑 | 教训 |
|------|------|
| 后端绑定冲突 | `127.0.0.1` 只接待本机，手机访问需 `0.0.0.0`（监听所有网卡）；但本机 Docker 已通配监听 :8000，两个通配打架（表现为局域网访问 :8000 得到 Docker 的 404）→ API 整体迁 **:8001**，`server.py` / `App.js` / `vite.config.js` 代理三处同步改 |
| `127.0.0.1` 永远是"自己" | 跨设备必须用对方的局域网地址；换网络环境要重新 `ipconfig getifaddr en0`。后端已部署到 Railway（`api.4y4.com`），生产环境直接用公网域名，本地开发仍用局域网 IP |
| 排查工具 | `lsof -nP -iTCP:端口 -sTCP:LISTEN` 看谁在监听；`curl 局域网IP:端口/api/chat` 模拟手机访问路径验证后端 |

---

<a id="sec-7"></a>

## 七、Agent 人设与技能

### 7.1 一句话本质

`AGENT.md`（人设）和 `Skill.md`（技能）都是**可复用的 Prompt 文本**，最终都注入 LLM 上下文。区别在于**角色**和**注入策略**。

### 7.2 运行机制

```
人 → AGENT.md(人设文本) → Agent 加载 → 投喂给 LLM → 按人设回答 → 执行工具循环
```

```
System Prompt = 人设(AGENT.md) + 命中的技能(Skill) + 工具定义 + 记忆 + 当前任务
```

### 7.3 AGENT.md vs Skill.md

| | AGENT.md（人设） | Skill.md（技能） |
|---|---|---|
| 角色 | 全局人设 / 行为准则 | 具体能力 / 执行流程 |
| 数量 | 通常 1 个 | 可多个 |
| 注入时机 | 每次对话常驻 | 按需触发才加载 |

### 7.4 为什么 Skill 要“按需”加载

- **省 token**：skill 全塞进 system，每次对话都要付费
- **防干扰**：指令太多会稀释模型注意力，降低遵循质量

skill.md 的 frontmatter 要写 `description`（触发条件）——平时只常驻 `name + description`，用户意图命中时才加载完整正文。

### 7.5 代码示例

**人设（常驻）**

```python
system_prompt = load_file("AGENT.md")   # Agent 读取人设文件

while True:
    user_input = wait_user_message()
    llm_response = call_llm(
        system=system_prompt,
        user=user_input
    )
```

**技能（按需）**

```python
# 简化版：skill 全文拼进 system，靠模型自己判断触发
skill = load_file("skill/hello_skill/skill.md")
system_prompt = f"{persona}\n\n【技能】\n{skill}\n命中触发条件时严格按技能指令执行。"

# 进阶版：只在命中触发条件时才加载正文（省 token）
meta = load_frontmatter("skill/hello_skill/skill.md")   # 只读 name + description
if matched(user_input, meta["description"]):
    system_prompt += load_file("skill/hello_skill/skill.md")   # 才注入完整正文
```

### 7.6 AGENT.md 中的二维码：编辑模式 vs 预览模式

**问题**：ASCII 字符画二维码在 Markdown **编辑模式**下可扫描，但切到**预览模式**后字体/行高变了，二维码几何结构被破坏，手机扫不了。

**原因**：预览模式默认用非等宽字体，字符宽度不一致。

**解决**：用 HTML `<pre>` 标签强制等宽渲染：

```html
<pre style="font-family:monospace;line-height:1;font-size:16px;letter-spacing:0;display:inline-block;">
█▀▀▀▀▀▀▀█▀████▀▀▀▀█▀▀▀▀▀▀█
█ █▀▀▀█ ██▄▄▄▄█▀███ █▀▀▀█ █
...（二维码内容）
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
</pre>
```

**关键样式**：

| 样式 | 作用 |
|------|------|
| `font-family:monospace` | 强制等宽字体，保证每个字符宽度一致 |
| `line-height:1` | 统一行高，避免行间距破坏二维码比例 |
| `letter-spacing:0` | 消除字间距，防止列偏移 |
| `display:inline-block` | 让 `<pre>` 按内容大小显示，不撑满整行 |

**最佳实践**：二维码内容用 Python `qrcode` 库程序生成，不要手动输入（手动输入容易改坏二维码数据）：

```python
import qrcode, io
qr = qrcode.QRCode(border=1)
qr.add_data("https://t.me/KuangyueHuang")
qr.make(fit=True)
output = io.StringIO()
qr.print_ascii(out=output, invert=True)
ascii_qr = output.getvalue()  # 精确的二维码字符画
```

**备选方案**：如果 ChatBot 的网页 UI 不支持 HTML 渲染（见 7.7），直接给纯文本链接更可靠：

```
链接：https://t.me/KuangyueHuang
用户名：@KuangyueHuang
```

### 7.7 ChatBot 网页 UI 的渲染限制

**发现**：ChatBot 的网页 UI（React 前端）**不渲染 HTML 标签和 Markdown 语法**，所有内容当纯文本显示。

具体表现：

| 写法 | 预期效果 | 实际效果 |
|------|---------|----------|
| `<pre style="...">` | 等宽渲染二维码 | 显示为普通文字 `<pre style="...">` |
| `[文字](url)` | 可点击链接 | 显示为普通文字 `[文字](url)` |
| `**粗体**` | 粗体文字 | 显示为普通文字 `**粗体**` |

**结论**：在 AGENT.md 中给 ChatBot 的指令里，不要使用 HTML 标签或 Markdown 语法，全部用纯文本格式。

**最终结论**：ChatBot 网页 UI 字体很大，ASCII 二维码中的 Unicode 方块字符（█▀▄）会被渲染成巨大的色块，宽高比完全不对，二维码几何结构被彻底破坏，**永远无法扫描**。代码块标记 ```` ``` ```` 也会被当普通文字显示。因此只给纯文本链接和用户名：

```
链接：https://t.me/KuangyueHuang
用户名：@KuangyueHuang
```

---

<a id="sec-8"></a>

## 八、CI/CD 部署（GitHub + Vercel + Railway）

### 8.1 全景架构

**一句话本质**：代码全在一个 GitHub repo，Vercel 只构建前端子目录，Railway 跑整个 Python 后端（含 Core）。

```
本地（一个工程 ENVDEV）
│
└── GitHub Repo: ENVDEV（整个推上去）
    │
    ├── Vercel 构建 webui/（前端）
    │   └── vercel.json 指定 Root Directory
    │
    └── Railway 跑 api_gateway（后端 = api_gateway + core）
        └── Start Command: python -m envdev.api_gateway.server
```

**Core 不需要单独部署**——Core 是库（被 import），api_gateway 启动时自动加载 core，一个进程搞定。

### 8.2 各平台职责与当前状态

| 平台 | 部署内容 | 域名 | 状态 |
|------|---------|------|------|
| GitHub | 整个 ENVDEV 仓库 | [github.com/Kryon-4Y4/ENVDEV](https://github.com/Kryon-4Y4/ENVDEV) | ✅ 已推送，Git 连接已建立 |
| Vercel | `projects/project-agentic/envdev/user_portal/webui/` | [www.4y4.com](https://www.4y4.com) | ✅ 已上线，push 自动部署 |
| Railway | 整个 Python 项目 | [api.4y4.com](https://api.4y4.com) | ✅ 已上线，push 自动部署 |

### 8.3 前端 API 地址：Vercel Rewrites

前端代码用相对路径 `/api/...`，开发时靠 Vite 代理转发到 `:8001`。生产环境没有 Vite，靠 **`vercel.json` 的 `rewrites`** 把 `/api/*` 转发到 Railway 后端：

```json
// vercel.json（放在项目根目录）
{
  "buildCommand": "cd projects/project-agentic/envdev/user_portal/webui && npm install && npm run build",
  "outputDirectory": "projects/project-agentic/envdev/user_portal/webui/dist",
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://api.4y4.com/api/:path*" }
  ]
}
```

**好处**：前端代码不用改，相对路径在开发和生产都生效（Vite 代理 → Vercel rewrites，无缝切换）。

> **域名演进**：初期用 `envdev-production.up.railway.app`（Railway 默认域名），后替换为自定义域名 `api.4y4.com`。

### 8.4 后端部署（Railway）—— ✅ 已完成

**步骤**：

1. ~~GitHub 创建 repo → 本地 push~~ ✅ 已完成
2. ~~Railway 新建项目 → "Deploy from GitHub repo" → 选 `Kryon-4Y4/ENVDEV`~~ ✅ 已完成
3. ~~配置 Railway：~~ ✅ 已完成
   - **Root Directory**：`projects/project-agentic`（`pyproject.toml` 所在位置）
   - **Start Command**：`python -m envdev.api_gateway.server`
   - **Variables**：`DEEPSEEK_API_KEY`、`LLM_MODEL`（在 Railway 面板设置）
4. ~~Railway 自动分配域名~~ ✅ 已完成（`envdev-production.up.railway.app` → 后改为自定义域名 `api.4y4.com`）
5. ~~把 Railway 域名填回 `vercel.json` 的 `rewrites`~~ ✅ 已完成

### 8.5 CORS 更新

后端部署后需要放行 Vercel 前端域名，修改 `server.py`：

```python
# 开发 + 生产都放行
allow_origins=[
    "http://127.0.0.1:5173",           # 本地 Vite 开发
    "http://127.0.0.1:3000",           # 本地旧端口
    "https://www.4y4.com",             # 生产前端域名
],
```

### 8.6 实际部署流程（已全部完成）

```bash
# ① GitHub 创建 repo + 推送 ✅ 已完成
gh repo create ENVDEV --public --source=. --push

# ② Vercel 首次部署 ✅ 已完成
#    安装 CLI → 登录授权 → vercel --yes --prod
#    然后在 Vercel 面板连接 GitHub（实现 push 自动部署）

# ③ 连接 Git 自动部署 ✅ 已完成
#    Vercel 面板 → Settings → Git → 连接 Kryon-4Y4/ENVDEV
#    此后每次 git push 自动触发 Vercel 重新构建

# ④ Railway 部署 ✅ 已完成
#    在 Railway 网页面板操作：New Project → Deploy from GitHub → 选 ENVDEV
#    设置 Root Directory = projects/project-agentic
#    设置 Start Command = python -m envdev.api_gateway.server
#    在 Variables 面板添加 DEEPSEEK_API_KEY 等环境变量

# ⑤ 自定义域名 ✅ 已完成
#    阿里云 DNS：CNAME www → cname.vercel-dns.com, CNAME api → envdev-production.up.railway.app
#    Vercel 面板添加 www.4y4.com
#    Railway 面板添加 api.4y4.com（需 TXT 验证）
#    更新 vercel.json rewrites → api.4y4.com
#    更新 server.py CORS → www.4y4.com
```

### 8.7 日常开发 vs 生产对照

| 场景 | 前端 API 转发 | 后端位置 | 配置文件 |
|------|-------------|---------|----------|
| 本地开发 | Vite proxy（`/api` → `:8001`） | 本地 `python -m envdev.api_gateway.server` | `vite.config.js` |
| 生产环境 | Vercel rewrites（`/api` → Railway） | Railway 自动运行 | `vercel.json` |

### 8.8 辅助文件

**`.vercelignore`**（放在项目根目录）：告诉 Vercel 上传时跳过哪些目录，减少文件数量、避免无效符号链接。

```
awesome-agentic-ai-zh/    # 参考仓库（体积大，不需要部署）
data/ jupyter-notebook/   # 数据 / 实验
tests/ notes/             # 笔记 / 测试
projects/project-agentic/build/    # PyInstaller 打包产物（含无效 symlink）
projects/project-agentic/dist/     # 同上
.venv/                    # 虚拟环境
.env                      # 密钥（不能上传）
# ...其余未来域占位目录也排除
```

### 8.9 踩坑记录

| 坑 | 现象 | 解决 |
|------|------|------|
| 项目名大写 | `Project names can be up to 100 characters long and must be lowercase` | 目录名 ENVDEV 是大写，Vercel 要求小写；去掉 `vercel.json` 的 `name` 字段即可 |
| 文件数超限 | `files should NOT have more than 15000 items, received 19229` | 创建 `.vercelignore` 排除 `awesome-agentic-ai-zh/`、`dist/`、`.venv/` 等大目录 |
| 无效符号链接 | `is not a valid symlink`（`dist/ENVDEV.app/` 内） | PyInstaller 打包的 `.app` 含 macOS 特殊 symlink，通过 `.vercelignore` 排除 `dist/` |
| uv.lock 过期 | `The lockfile at uv.lock needs to be updated, but --locked was provided` | 本地运行 `uv lock` 更新后提交推送 |
| 部署排队超时 | Railway 免费套餐构建队列等待时间长（5-15 分钟） | 耐心等，或取消旧部署后 push 新 commit 触发 |
| 0 Variables | 部署时环境变量未注入 | 确保变量在部署前设置好，旧部署不会自动获取新变量 |
| PORT 写死 | Railway 动态分配端口，写死 8001 导致无法访问 | 改为 `port=int(os.environ.get("PORT", 8001))` |
| Start Command 缺失 | Railway 不知道如何启动 Python 模块 | 在面板 Settings 中显式设置 Start Command |
| ChatBot UI 不渲染 HTML/MD | `<pre>`、`[text](url)`、`**粗体**` 全部显示为纯文字 | AGENT.md 中给 ChatBot 的指令只用纯文本，不用 HTML 或 Markdown |
| ASCII 二维码变形 | ChatBot UI 字体太大，█▀▄ 渲染成巨大色块，二维码无法扫描 | 放弃二维码，只给纯文本链接 + 用户名 |
| Railway 自定义域名需 TXT 验证 | 添加自定义域名时要求 DNS TXT 记录验证所有权 | 按 Railway 面板提示，在 DNS 添加 `_railway-verify.api` TXT 记录 |

### 8.10 自定义域名配置

**DNS 解析**（阿里云 DNS 控制台 `https://dns.console.aliyun.com`）：

| 类型 | 主机记录 | 记录值 |
|------|---------|--------|
| CNAME | `www` | `cname.vercel-dns.com` |
| CNAME | `api` | `envdev-production.up.railway.app` |
| TXT | `_railway-verify.api` | `railway-verify=...`（Railway 面板提供的验证值） |

**平台配置**：

| 平台 | 操作 |
|------|------|
| Vercel | Settings → Domains → 添加 `www.4y4.com` |
| Railway | Settings → Networking → Add Custom Domain → `api.4y4.com`（需 TXT 验证） |

**代码同步更新**：

| 文件 | 改动 |
|------|------|
| `vercel.json` | `rewrites` 的 destination 改为 `https://api.4y4.com/api/:path*` |
| `server.py` | CORS `allow_origins` 改为 `https://www.4y4.com` |

**最终状态**：

| 服务 | 域名 | 状态 |
|------|------|------|
| 前端 | [www.4y4.com](https://www.4y4.com) | ✅ |
| 后端 API | [api.4y4.com](https://api.4y4.com) | ✅ |
| API 文档 | [api.4y4.com/docs](https://api.4y4.com/docs) | ✅ |

### 8.11 注意事项

- **`.env` 不提交 Git**：本地用 `.env`，Railway 用平台 Variables 面板，Vercel 用 Settings → Environment Variables
- **`node_modules/` 不提交**：根目录 `.gitignore` 已覆盖；Railway/Vercel 构建时各自 `npm install`
- **push 自动部署**：GitHub push → Vercel 自动重新构建前端；Railway 自动重新部署后端（Git 连接已建立）
- **Python 版本**：Railway 需指定 Python 3.14（在 `pyproject.toml` 的 `requires-python` 已声明）
九、从 ChatBot 到 Agentic 架构演进
9.1 当前 ChatBot 架构（三层分离）
┌─────────────────────────────────────────────────────────────────────┐
│                    core.py 业务逻辑层                                │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐ │
│  │ Build_System_Message │  │ client=OpenAI(key,Url)               │ │
│  │ (AGENT.md + skill)   │  │ client.chat(model, message)          │ │
│  └──────────────────────  │ return msg.choices[0].message.content│ │
│                             └──────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│                    server_api.py 服务层                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ @app.post("/api/chat")                                       │   │
│  │ def api_chat(req: ChatRequest) -> dict:                      │   │
│  │     messages = [system(build_system_prompt())] + history     │   │
│  │     messages.append(user(req.message))                       │   │
│  │     return {"reply": chat(messages)}                         │   │
│  └──────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────┤
│                    front_end.py 展现层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ chatInput    │→ │ req.history  │→ │ history += assistantReply│  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
数据流：
用户输入 → front_end(chatInput)
         → POST /api/chat {message, history}
         → server_api 组装 messages = [system] + history + [user]
         → core.py chat(messages)
         → OpenAI client → LLM 返回
         → server_api 返回 {"reply": "..."}
         → front_end 渲染 + history.push(reply)
核心循环（伪代码）：
# ChatBot 本质：一个 while 循环
while chatinput:
    assistant_reply = request + history + systemPrompt
    history += assistant_reply
System Prompt 组成：
system_prompt = AGENT.md(人设) + skill.md(技能)
文件	角色	注入时机
AGENT.md	全局人设 / 行为准则	每次对话常驻
skill.md	具体能力 / 执行流程	按需触发才加载
流式输出：stream=True → 生成器 → SSE → 前端逐块渲染（打字机效果）
9.2 ChatBot 的局限
当前架构是被动问答模式：
用户问 → 模型答 → 结束
局限	说明
无工具调用	模型只能"说"，不能"做"（查数据库、调 API、执行代码）
无规划能力	复杂任务无法拆解为多步骤执行
无记忆持久化	对话结束即丢失，跨会话无上下文
单轮响应	每次只回复一次，不会主动追问或迭代
无环境感知	不知道当前时间、用户身份、外部状态
9.3 Agentic 架构：从"问答"到"行动"
一句话本质：ChatBot 是"你说我答"，Agent 是"你给我目标，我自己规划、执行、验证、迭代"。
ChatBot:  用户问 → 模型答 → 结束
Agent:    用户给目标 → 模型规划 → 调用工具 → 观察结果 → 调整计划 → 再执行 → ... → 完成
Agent 核心循环（ReAct 模式）：
while not task_complete:
    # 1. 思考（Thought）
    thought = llm.think(current_context)
    
    # 2. 行动（Action）
    action = llm.decide_action(thought)  # 选择工具
    
    # 3. 执行（Execute）
    result = tools[action.name](**action.args)
    
    # 4. 观察（Observation）
    observation = result
    
    # 5. 更新上下文，继续循环
    context.append(thought, action, observation)
9.4 Agentic 架构的三层扩展
在现有 ChatBot 三层基础上，Agent 需要新增：
┌─────────────────────────────────────────────────────────────────────┐
│                    core.py 业务逻辑层（扩展）                         │
│                                                                      │
│  原有：                                                               │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐ │
│  │ Build_System_Message │  │ client.chat(model, message)          │ │
│  └──────────────────────  └──────────────────────────────────────┘ │
│                                                                      │
│  新增：                                                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Agent Loop（ReAct 循环）                                      │   │
│  │ 1. 思考：分析当前状态，决定下一步                               │   │
│  │ 2. 选工具：从工具列表中选择合适的工具                           │   │
│  │ 3. 执行：调用工具，获取结果                                     │   │
│  │ 4. 观察：将结果加入上下文                                       │   │
│  │ 5. 判断：任务完成？→ 输出最终回复；未完成 → 回到步骤1           │   │
│  ──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 工具注册表（Tool Registry）                                    │   │
│  │ - 搜索工具：web_search(query)                                 │   │
│  │ - 代码工具：run_code(code)                                    │   │
│  │ - 文件工具：read_file(path), write_file(path, content)        │   │
│  │ - API 工具：call_api(endpoint, params)                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────┤
│                    server_api.py 服务层（扩展）                       │
│                                                                      │
│  原有：/api/chat（单次问答）                                          │
│  新增：/api/agent（Agent 任务执行）                                    │
│  ┌──────────────────────────────────────────────────────────────   │
│  │ @app.post("/api/agent")                                      │   │
│  │ def api_agent(req: AgentRequest) -> dict:                    │   │
│  │     # AgentRequest 包含：目标描述 + 可用工具列表 + 最大迭代次数  │   │
│  │     result = agent_loop(req.goal, req.tools, req.max_steps)  │   │
│  │     return {"reply": result, "steps": agent.trace}           │   │
│  └──────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────┤
│                    front_end.py 展现层（扩展）                        │
│                                                                      │
│  原有：chatInput + history（对话气泡）                                │
│  新增：Agent 执行过程可视化                                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 思考过程展示：                                                  │   │
│  │  Thought: 我需要先搜索最新数据...                             │   │
│  │ 🔧 Action: 调用 web_search("2026 F1  standings")             │   │
│  │ 📋 Observation: 返回 10 条结果...                               │   │
│  │ 💭 Thought: 数据已获取，现在分析...                              │   │
│  │ ✅ Final: 输出分析报告                                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
─────────────────────────────────────────────────────────────────────
9.5 ChatBot vs Agent 对比
维度	ChatBot	Agent
交互模式	问答（Q&A）	任务执行（Task Execution）
响应次数	单次回复	多轮迭代（思考→行动→观察）
工具使用	无	有（搜索、代码、API、文件等）
规划能力	无	有（任务拆解、步骤规划）
记忆	仅对话历史	对话历史 + 工具执行结果 + 长期记忆
自主性	被动（等用户问）	主动（可自主决定下一步）
错误处理	无法自我纠正	可观察结果、调整策略、重试
适用场景	客服、咨询、闲聊	数据分析、代码生成、研究、自动化
9.6 演进路径：从当前 ChatBot 到 Agent
阶段 1：工具调用（Tool Use） ← 当前最接近的下一步
# 在 core.py 中增加工具调用能力
def chat_with_tools(messages: list, tools: list) -> str:
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        tools=tools,  # OpenAI 兼容的工具定义
        tool_choice="auto",
    )
    
    # 如果模型选择了工具
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            result = execute_tool(tool_call)
            messages.append({"role": "tool", "content": result})
        # 再次调用 LLM，基于工具结果生成最终回复
        return chat(messages)
    
    return response.choices[0].message.content
阶段 2：ReAct 循环（思考-行动-观察）
def agent_loop(goal: str, tools: dict, max_steps: int = 10) -> str:
    context = [{"role": "system", "content": AGENT_PROMPT}]
    context.append({"role": "user", "content": goal})
    
    for step in range(max_steps):
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=context,
            tools=tools,
        )
        
        # 模型输出最终回复（无工具调用）
        if not response.choices[0].message.tool_calls:
            return response.choices[0].message.content
        
        # 执行工具
        for tool_call in response.choices[0].message.tool_calls:
            result = tools[tool_call.function.name](**json.loads(tool_call.function.arguments))
            context.append({"role": "tool", "content": result})
    
    return "达到最大步骤数，任务未完成。"
阶段 3：多 Agent 协作
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                      │
│  接收用户目标 → 拆解子任务 → 分配给专业 Agent → 汇总结果      │
└──────────┬──────────────────┬──────────────────┬────────────┘
           │                  │                  │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │ Research    │   │ Code        │   │ Analysis    │
    │ Agent       │   │ Agent       │   │ Agent       │
    │ (搜索/爬虫)  │   │ (写代码/调试) │   │ (数据分析)   │
    └─────────────┘   └─────────────┘   └─────────────┘
9.7 本项目演进建议
基于当前 ENVDEV 架构，Agent 化的最小改动路径：
步骤	改动	文件
1	定义工具 Schema（OpenAI function calling 格式）	core/tools.py（新建）
2	实现工具执行函数（搜索、代码执行等）	core/tools.py
3	修改 chat() 支持工具调用循环	core/core.py
4	新增 /api/agent 端点	api_gateway/server.py
5	前端展示 Agent 思考过程	webui/src/App.jsx
工具 Schema 示例：
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "搜索互联网获取最新信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "执行 Python 代码并返回结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python 代码"}
                },
                "required": ["code"]
            }
        }
    }
]
9.8 关键概念总结
概念	说明
System Prompt	模型的"人格"和"规则"，每次对话常驻
Tool Calling	模型决定调用哪个工具 → 执行 → 结果返回模型 → 模型生成最终回复
ReAct	Reasoning + Acting：思考→行动→观察→再思考的循环
Agent Loop	Agent 的核心循环：直到任务完成或达到最大步骤数
Orchestrator	多 Agent 场景中的协调者，负责拆解任务和分配
Memory	短期（对话历史）+ 长期（向量数据库/文件）
一句话总结：
ChatBot = LLM + System Prompt + 对话历史Agent = LLM + System Prompt + 工具 + 循环 + 记忆
