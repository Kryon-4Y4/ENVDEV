# Python 虚拟环境(.venv) 架构说明

> 笔记时间：2026-08-26
> 环境：Python 3.14.2 ｜ macOS


```
.venv/
├── bin/                        # 可执行文件 + 激活脚本
│   ├── activate                # bash/zsh 激活脚本
│   ├── activate.csh            # csh/tcsh 激活脚本
│   ├── activate.fish           # fish 激活脚本
│   ├── Activate.ps1            # PowerShell 激活脚本
│   ├── python  ->  python3.14  # Python 解释器软链接
│   ├── python3 ->  python3.14
│   ├── python3.14 -> /opt/homebrew/.../python3.14
│   ├── pip / pip3 / pip3.14    # 包管理工具
│   ├── pytest / py.test        # 测试工具
│   ├── ipython / ipython3      # 交互式 Python
│   └── dotenv / httpx ...      # 安装的命令行工具
├── lib/
│   └── python3.14/
│       └── site-packages/      # 第三方包安装位置（隔离区）
├── include/                    # C 扩展头文件
├── share/                      # 共享资源（man pages 等）
├── pyvenv.cfg                  # 虚拟环境配置文件
└── .gitignore                  # 内容为 *，忽略全部
```

## 各目录/文件详解

### `bin/` —— 可执行文件目录

包含激活脚本和所有可执行工具：

- **激活脚本**：`source .venv/bin/activate` 执行后，Shell 的 `PATH` 变量被修改，优先搜索 `.venv/bin/`，从而隔离 Python 环境
- **Python 解释器**：`python`、`python3` 是 `python3.14` 的软链接，而 `python3.14` 指向系统 `/opt/homebrew/` 中的 Python
- **包工具**：`pip` / `pip3` / `pip3.14` 都是独立的副本，安装的包只会进入当前虚拟环境
- **CLI 工具**：安装的第三方包自带的命令行工具（pytest、ipython、httpx、dotenv 等）也会出现在这里

### `lib/python3.14/site-packages/` —— 依赖隔离区

**核心隔离机制**。所有通过 `pip install` 安装的第三方包都安装在此目录下，与系统 Python 的全局包完全隔离。

目前安装的包包括：
- **基础**：httpx、pydantic、python-dotenv
- **开发**：pytest、pytest-asyncio、ipython
- **传递依赖**：certifi、anyio、jedi、pygments 等

### `include/` —— C 扩展头文件

当某些包需要编译 C 扩展时（如 `numpy`），编译所需的头文件会放在这里。

### `share/` —— 共享资源

存放 man pages 等文档资源。

### `pyvenv.cfg` —— 配置文件

```ini
home = /opt/homebrew/opt/python@3.14/bin
include-system-site-packages = false
version = 3.14.2
executable = /opt/homebrew/Cellar/python@3.14/3.14.2/Frameworks/Python.framework/Versions/3.14/bin/python3.14
command = python3.14 -m venv /path/to/.venv
```

关键字段说明：
- `home`：指向系统 Python 的 bin 目录
- `include-system-site-packages = false`：**不继承**系统全局包（设为 true 则会同时看到系统包）
- `version`：Python 版本号
- `executable`：Python 解释器的完整路径
- `command`：创建该虚拟环境的命令

### `.gitignore` —— Git 忽略

内容为 `*`，即忽略 `.venv/` 下的所有文件，确保虚拟环境不会被提交到 Git 仓库。

## 隔离原理

激活虚拟环境的本质是**修改 `PATH` 环境变量**：

```
# 激活前
PATH = /usr/local/bin:/usr/bin:/bin:...

# source .venv/bin/activate 后
PATH = /path/to/.venv/bin:/usr/local/bin:/usr/bin:/bin:...
```

这样 `python`、`pip` 等命令会优先找到虚拟环境中的版本，从而实现依赖隔离。

退出时执行 `deactivate`，即可恢复原来的 `PATH`。

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 创建虚拟环境 | `python3 -m venv .venv` |
| 激活（bash/zsh） | `source .venv/bin/activate` |
| 激活（fish） | `source .venv/bin/activate.fish` |
| 激活（PowerShell） | `.venv/bin/Activate.ps1` |
| 退出 | `deactivate` |
| 查看已安装包 | `pip list` |
| 导出依赖 | `pip freeze > requirements.txt` |

[def]: /image/venv-architecture.png