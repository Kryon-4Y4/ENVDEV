# ENVDEV

Agentic AI 学习项目 —— 参照 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 学习路线图，逐步实践 Agentic AI 开发。

## 项目结构

```
ENVDEV/
├── awesome-agentic-ai-zh/   # 参考学习资料
├── src/
│   └── envdev/             # 主代码包
│       ├── __init__.py
│       └── main.py
├── tests/                   # 测试
├── notebooks/               # Jupyter notebooks（探索用）
├── data/                    # 数据文件
├── pyproject.toml           # 项目配置
└── requirements.txt         # 依赖
```

## 快速开始

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装项目（可编辑模式）
pip install -e ".[dev]"

# 运行
python -m envdev
```

## 学习路线参考

参考仓库的 8 个阶段，按需学习和实践。