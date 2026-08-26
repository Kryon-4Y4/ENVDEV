# 项目根目录结构与说明

> 更新时间：2026-08-26

## `src/` 源码目录

项目采用 **src layout** 布局，所有源码放在 `src/` 下，与配置文件、文档等根级文件分离。

```
src/
├── envdev/                          # 主代码包（envdev）
│   ├── __init__.py                  # 包初始化，定义 __version__
│   ├── __main__.py                  # python -m envdev 入口
│   ├── main.py                      # 主程序逻辑
│   └── config.py                    # 配置模块（加载 .env 环境变量）
├── envdev.egg-info/                 # pip install -e 自动生成的元信息（无需手动管理）
│   ├── PKG-INFO                     #   项目元数据
│   ├── SOURCES.txt                  #   源文件清单
│   ├── requires.txt                 #   依赖列表
│   ├── top_level.txt                #   顶层包名
│   └── dependency_links.txt         #   依赖链接（通常为空）
└── envdev/__pycache__/              # Python 字节码缓存（自动生成，可忽略）
```

### 各文件职责

| 文件 | 职责 |
|------|------|
| `__init__.py` | 包标识，定义 `__version__ = "0.1.0"` |
| `__main__.py` | `python -m envdev` 的入口，调用 `main()` |
| `main.py` | 主程序逻辑，`ProjectInfo` 示例类 |
| `config.py` | 从 `.env` 加载 API 密钥等配置，提供 `settings` 单例 |

---

## 根目录文件

| 文件 | 说明 |
|------|------|
| `pyproject.toml` | 项目配置核心。定义包名、版本、依赖、构建系统等，替代传统的 `setup.py` |
| `.env` | 环境变量文件。存放 LLM API 密钥等敏感信息（**已 .gitignore，不提交**） |
| `.env.example` | 环境变量模板。只含变量名不含值，供他人参考格式（**提交 Git**） |
| `.gitignore` | Git 忽略规则。排除 `.venv/`、`__pycache__/`、`.env` 等 |
| `README.md` | 项目说明文档 |
| `uv.lock` | uv 包管理器的依赖锁定文件（精确记录每个依赖的版本和哈希） |

---

## 根目录文件夹

| 文件夹 | 说明 |
|--------|------|
| `awesome-agentic-ai-zh/` | 克隆的参考学习仓库 |
| `.venv/` | Python 虚拟环境（隔离项目依赖） |
| `notes/` | 学习笔记（markdown + 图片） |
| `tests/` | 测试用例 |
| `jupyter-notebook/` | Jupyter notebook 探索笔记 |
| `data/` | 数据文件 |
| `src/` | 源码目录（如上所述） |