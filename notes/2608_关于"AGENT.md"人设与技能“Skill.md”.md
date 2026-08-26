# AGENT.md（人设）与 Skill.md（技能）

## 一句话本质

两者都是**可复用的 Prompt 文本**，最终都注入 LLM 上下文。区别在于**角色**和**注入策略**。

## 运行机制

```
人 → AGENT.md(人设文本) → Agent 加载 → 投喂给 LLM → 按人设回答 → 执行工具循环
```

```
System Prompt = 人设(AGENT.md) + 命中的技能(Skill) + 工具定义 + 记忆 + 当前任务
```

## AGENT.md vs Skill.md

| | AGENT.md（人设） | Skill.md（技能） |
|---|---|---|
| 角色 | 全局人设 / 行为准则 | 具体能力 / 执行流程 |
| 数量 | 通常 1 个 | 可多个 |
| 注入时机 | 每次对话常驻 | 按需触发才加载 |

## 为什么 Skill 要"按需"加载

- **省 token**：skill 全塞进 system，每次对话都要付费
- **防干扰**：指令太多会稀释模型注意力，降低遵循质量

所以 skill.md 的 frontmatter 要写 `description`（触发条件）——平时只常驻 `name + description`，用户意图命中时才加载完整正文。

## 最小代码示例

**人设（常驻）**

```python
system_prompt = load_file("AGENT.md")   # Agent 读取人设文件

while True:
    user_input = wait_user_message()
    # 把人设 + 用户指令，一起发给大模型 LLM
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
