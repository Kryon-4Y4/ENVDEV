---
name:hello-skill
description:第一个 hello skill。 当用户说“请打招呼”或“say hi”时触发
---

当用户请你打招呼时，回三件事：
1.用简体中文和英文各说一次hello
2.提现在的日期（用system时间）
3.给一个今日小提醒（随机选健康/学习/心情建议）
4.发送一串可爱的表情符号。


根据记忆中的配置说明：
打包后配置外置（.env / AGENT.md / skill/ 目录）
这意味着 skill/ 和 .env、AGENT.md 一样，属于配置/资源类文件，应该与 core/（核心代码）平级，而不是放在 core/ 内部。