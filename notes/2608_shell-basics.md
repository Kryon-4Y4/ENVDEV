# Shell 基础知识整理

> 更新时间：2026-08-26 | macOS / zsh

## 一、Shell 是什么？

**Shell** 是命令行解释器，用户输入命令 → Shell 解析 → 内核执行。常见的有 `sh`（1977 元老）、`bash`（Linux 默认）、`zsh`（macOS 默认，bash 超集，智能补全更强）。

## 二、核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **PATH** | 命令搜索路径，`:` 分隔 | `export PATH="/opt/homebrew/bin:$PATH"` |
| **配置文件** | `.zshrc`（zsh）/ `.bashrc`（bash） | `source ~/.zshrc` 修改后立即生效 |
| **管道** | `\|`：左边输出作为右边输入 | `grep error log \| head -5` |
| **重定向** | `>` 覆盖 / `>>` 追加 | `python run.py > output.txt` |
| **退出码** | `$?`：0=成功，非0=失败 | `cmd && echo ok \|\| echo fail` |
| **引号** | `'` 原样 / `"` 解析变量 / `` ` `` 执行命令 | `echo "$HOME"` → `/Users/...` |

## 三、常用命令

| 操作 | 命令 |
|------|------|
| 文件列表 | `ls -la` |
| 递归建目录 | `mkdir -p a/b/c` |
| 实时看日志 | `tail -f log` |
| 查进程 | `ps aux \| grep python` |
| 激活虚拟环境 | `source .venv/bin/activate` |
| 退出虚拟环境 | `deactivate` |
| 命令位置 | `which python` |
| 历史搜索 | `ctrl + r` |
| 行首/行尾 | `ctrl + a` / `ctrl + e` |

## 四、同类工具一览

| 类别 | 工具 |
|------|------|
| 其他 Shell | **fish**（开箱即用）、**PowerShell**（微软）、**Nushell**（结构化数据）、**xonsh**（Python 语法） |
| 终端模拟器 | **iTerm2**（macOS 增强）、**Warp**（AI 现代终端）、**Ghostty**（GPU 加速）、**VS Code 内置终端** |
| 增强神器 | **oh-my-zsh**（框架）、**fzf**（模糊搜索）、**zoxide**（智能跳转）、**tmux**（多会话）、**eza/bat/fd**（ls/cat/find 替代品） |

