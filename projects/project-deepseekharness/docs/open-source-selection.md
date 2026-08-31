# 开源项目选型调研：多租户 SaaS + 调度 + 爬虫 + 数据脚本 + 运维 + Agentic 化

> 对应架构：`architecture.md`（传统微服务）与 `architecture-agentic.md`（Harness 化）
> 结论先行：**有成熟项目，但没有一个项目能全覆盖** —— 按架构分层组合开源项目是行业常态；
> Agentic 层（2024–2025 爆发）已有多个可生产化选项。

---

## 1. 按架构层选型表

### ① 后台管理系统 / Admin Console（含多租户底座）

| 项目 | 定位 | 与需求的契合点 | 备注 |
|---|---|---|---|
| [芋道 yudao-cloud](https://github.com/sugarkissme/yudao-cloud) | Spring Cloud Alibaba 微服务后台 | **多租户 + RBAC + 数据权限 + 工作流 + 支付/短信/商城**，开箱即用，与"多租户 + Admin Console"需求重合度最高 | RuoYi 系衍生，生态大、文档全；租户隔离默认行级 |
| [若依 RuoYi / ruoyi-vue-pro](https://blog.csdn.net/chenchuang0128/article/details/156392726) | 单体/微服务后台脚手架 | 国内最流行的后台基础，多租户需自行扩展或使用衍生版 | 与芋道、JeeSite、JeecgBoot 的对比见[该文](https://leheavengame.com/article/697f64037a00789668548f36) |
| [JeecgBoot](https://blog.csdn.net/chenchuang0128/article/details/156392726) | 低代码后台平台 | 在线表单/报表/代码生成，天然适合"数据脚本"类快速交付 | 微服务版基于 Spring Cloud |
| [NocoBase](https://www.nocobase.com/en/blog/4-open-source-data-management-tools-for-business-systems) | 开源无代码数据管理平台 | 插件化架构 + 多租户，适合把"后台管理系统"做薄 | 与 Directus 等对比见其博客 |
| [EcoNets Admin Vue3](https://github.com/EcoNetsTech/econets-ui-admin-vue3) | Vue3 管理端 UI | SaaS 多租户 + RBAC + 工作流的前端模板 | 适合作为 User Portal / Admin Console 前端起点 |

### ② API 网关 / 接入层

| 项目 | 定位 | 备注 |
|---|---|---|
| [Apache APISIX](https://raw.githubusercontent.com/stoa-platform/stoa-docs/refs/heads/main/blog/2026-01-28-open-source-api-gateway-2026.md) | 云原生高性能网关 | 插件体系完善，**支持租户维度路由/限流/配额**，中文生态活跃 |
| Apache ShenYu / Kong / Traefik / Envoy / Spring Cloud Gateway | 通用网关 | 选型对比见[网关选型对比](https://blog.csdn.net/wokoone/article/details/131720584)；Java 栈团队常用 Spring Cloud Gateway |
| Keycloak / Casdoor | 多租户 IAM | 提供 realm/租户级认证与 SSO，可作为 RBAC 底层 |

### ③ 任务调度器 / Task Scheduler

| 项目 | 定位 | 与需求的契合点 |
|---|---|---|
| [XXL-Job](https://www.dtstack.com/zh-cn/blogs/workflow-scheduler-selection-guide) | 轻量分布式调度 | cron、分片广播、失败重试、可视化控制台，**中文生态最普及**，适合"定时触发爬虫/脚本" |
| [Apache DolphinScheduler](https://www.dtstack.com/zh-cn/blogs/workflow-scheduler-selection-guide) | DAG 工作流调度 | 可视化依赖编排、补数、告警，适合"爬虫→清洗→入库"的多步依赖链 |
| Apache Airflow / Prefect / Dagster | 数据工作流编排 | 生态大、Python 原生，适合重数据工程场景 |
| 三选一参考 | — | 官方对比见 [dtstack 调度选型指南](https://www.dtstack.com/zh-cn/blogs/workflow-scheduler-selection-guide) 与 [OSC 对比文](https://my.oschina.net/emacs_7995523/blog/19486942) |

### ④ 数据脚本 / 数据集成层

| 项目 | 定位 | 备注 |
|---|---|---|
| [Apache SeaTunnel](https://my.oschina.net/SeaTunnel/blog/19207023) | 新一代数据集成引擎 | 多源接入、分布式、中文生态；与 DataX/Airbyte/Canal/Debezium 对比见[此文](https://segmentfault.com/a/1190000047603823) |
| DataX | 阿里离线批量同步 | 成熟稳定，适合定时批量导入导出 |
| dbt | SQL 转换层（数据仓库建模） | 适合"数据脚本"标准化为可测试的 SQL 工程 |
| Airbyte / Flink CDC / Canal / Debezium | EL / 实时增量同步 | 实时链路需要时引入 |

### ⑤ 爬虫工具 / Crawler Tool

| 项目 | 定位 | 备注 |
|---|---|---|
| Scrapy | 经典 Python 爬虫框架 | 稳定、可扩展（代理池/去重/限速均可自建中间件） |
| [Crawl4AI](https://codeguilds.dev/packages/awesome-ai-web-scraping) | LLM 友好爬虫 | 输出结构化 Markdown/JSON，**直接喂给 Agent 使用**，与 Agentic 化契合 |
| Skyvern / Browser-use / Playwright MCP | Agentic 浏览器自动化 | 视觉驱动、自动操作网页（填表/点击/对抗反爬），是 Agent 化爬虫的主流方向 |
| Agentic 浏览器生态全景 | — | 见 [The Agentic Browser Wars 2026 Landscape Map](https://www.unbrowse.ai/blog/agentic-browser-wars-2026-landscape) |

### ⑥ 运维中心 / Ops Center 与可观测

| 项目 | 定位 | 备注 |
|---|---|---|
| [Spug](https://github.com/lianghuiyuan/spug) | 轻量无 Agent 运维平台 | **主机管理、批量执行、在线终端、应用发布、任务计划、配置中心、监控报警** 一站式，与 Ops Center 需求高度吻合 |
| Grafana + Prometheus + Alertmanager | 监控告警 | 事实标准 |
| Apache SkyWalking / ELK / Loki | APM 与日志链路 | 对应"全链路 Trace" |
| [HolmesGPT](https://blog.gitcode.com/fbf9ab728694c50850a173855955a10d.html) | AI 运维助手 | 告警接入 → 自动根因分析，对应 Ralph 自愈循环雏形 |
| [AI Incident Response Agent](https://github.com/sd031/ai_powered_incident_response_agent) | 告警自动处置参考实现 | PagerDuty/OpsGenie → 自动调查 → 结构化根因报告 |

### ⑦ Agentic 编排层（Harness 化核心，2024–2025 成熟度快速上升）

| 项目 | 定位 | 与架构的对应关系 |
|---|---|---|
| [Dify](https://markaicode.com/best/best-dify-production-practices/) | 开源 LLM 应用平台 | 可视化 **Agent/工作流编排 + 工具接入 + RAG 知识库 + 多租户应用发布**，几乎直接对应"Agent Gateway + Workflow + 记忆层"；与 Flowise/Langflow 对比见[该文](https://markaicode.com/best/best-dify-production-practices/) |
| n8n | 工作流自动化（fair-code） | 400+ 集成 + Agent 节点，适合做**事件总线和跨服务编排总线** |
| Flowise / Langflow | 低代码 Agent 构建 | 快速原型友好 |
| CrewAI / AutoGen | 多 Agent 框架（代码层） | 需要深度定制时作为开发框架 |
| [awesome-mcp-servers](https://github.com/mctrinh/awesome-mcp-servers) | MCP 工具服务清单 | 现成工具（浏览器/数据库/GitHub/爬虫等）直接接入，对应"工具适配层"；另一清单见 [Sagargupta16/awesome-mcp-servers](https://github.com/Sagargupta16/awesome-mcp-servers) |

---

## 2. 推荐组合方案

### 方案 A：全栈底座最快路径（Java 栈）
> 目标：最快搭出"多租户后台 + 调度 + 数据"可用系统

```
yudao-cloud（多租户 + RBAC + Admin Console + 工作流）
  + XXL-Job（任务调度器：cron/重试/分片）
  + DolphinScheduler（复杂 DAG：爬虫→清洗→入库）
  + SeaTunnel / DataX（数据脚本：批量同步/导入导出）
  + Scrapy / Crawl4AI（爬虫工具）
  + Spring Cloud Gateway / APISIX（API 网关）
  + Spug + Grafana + SkyWalking（运维中心 + 可观测）
```

### 方案 B：组件化自研（多语言/更强控制）
```
APISIX（网关）→ Keycloak（多租户 IAM）
  → 自研核心服务（多租户上下文 + 隔离策略）
  → XXL-Job + DolphinScheduler
  → SeaTunnel + dbt
  → Crawl4AI / Skyvern
  → Grafana + SkyWalking + ELK
  → 自研 Admin Console / Ops Center
```

### 方案 C：Agentic 化叠加（在 A/B 之上，对应 architecture-agentic.md）
```
Dify（Agent 编排层：意图路由 + Workflow + RAG 记忆）
  → 现有服务经 MCP 暴露为工具（awesome-mcp-servers 直接复用现成工具）
  → Crawl4AI / Skyvern 作为"爬虫 Agent"的工具
  → HolmesGPT / 自研 Ralph 循环（告警 → Goal → 自愈）
  → 保留确定性链路为降级通道
```

---

## 3. 需要注意的坑

1. **没有"一个项目全覆盖"**：多租户 SaaS + 调度 + 爬虫 + 数据脚本 + 运维的组合必须拼装，
   拼装成本主要在**租户上下文透传**与**统一鉴权/审计**，建议用网关 + Keycloak 收口。
2. **租户隔离深度**：开源后台（若依/芋道系）默认多为 `tenant_id` 行级隔离；
   需要 Schema-per-Tenant 或独立实例时，需在数据访问层自行扩展（对应隔离策略的可配置化）。
3. **许可证务必核实**：各项目 License 差异大（如 XXL-Job 为 GPL、n8n 为 fair-code 可持续使用许可，
   商用/SaaS 多租户售卖前必须逐项确认；Apache 系项目一般最省心）。以上仅为例示，以各仓库 LICENSE 为准。
4. **Agentic 层定位**：Dify/n8n 类平台擅长"编排与工具接入"，但**不替代业务微服务**；
   生产环境建议将其作为编排旁路（方案 C），核心交易仍走确定性链路。
5. **爬虫合规**：Skyvern/浏览器自动化的反爬对抗能力是把双刃剑，需内置域白名单、
   限速与数据最小化护栏（对应治理层策略中心）。
