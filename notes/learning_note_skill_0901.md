Skill和渐进式披露机制

1.模式
简单提取文本 先用工具提取 PDF 中的文本/图片内容
再用 HTML + CSS 手动/自动生成排版好的页面
高保真还原 PDF 排版 
按照现有 4Y4 limited.html 的风格重新排版 
不要额外的资产目录，保持单一文件。
样式上我想加 。左侧导航文章，正文Page及Page的章节导航
深色模式/浅色模式

2.配置成 Skill。这样后续只需 /pdf-to-html <文件路径> 即可一键执行整套流程。



Skill的分级
- **内置级 Skill（Built-in Skill）**：IDE Agent Extension 自带的全局原生技能，无需安装，在所有项目中均可使用。如 `/find-skills`、`/vercel-deploy`。
- **项目级 Skill（Project Skill）**：安装在项目中的技能，Agent 进入该项目上下文后才可使用。如 `/pdf-to-html`、`/archify`。
- **Agent 级 Skill（Agent Skill）**：项目中定义的 Agent 自身所具备的技能模板，用于赋予 Agent 特定的领域能力。如 `/hello_skill`。
