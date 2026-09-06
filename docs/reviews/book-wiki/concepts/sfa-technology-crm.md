---
type: concept
title: 销售技术与 CRM/SFA (Sales Technology, SFA & CRM)
aliases: [SFA, sales force automation, CRM, digital selling, sales tech]
sources: [johnston-sf-management-12e, jpssm2021-digital-selling, salesforce-annual-report, cdsd-brochure]
---
# 销售技术与 CRM/SFA (Sales Technology, SFA & CRM)

## 定义

**SFA（销售力量自动化）**是以移动/云系统承载销售流程（账户管理、拜访打卡、订单、管线）的信息技术层。Johnston & Marshall 指出自 1990 年代 SFA 以来"销售已重度依赖信息与技术" [johnston-sf-management-12e p.30, p.114]，并专章讨论"CRM 与数据分析时代的客户管理与销售角色"——CRM 把客户交互变成可分析的数据资产，改变销售战略与销售角色本身 [johnston-sf-management-12e p.94-96]。学术侧，JPSSM 2021 数字销售综述以"Practical Insights for Sales Force Digitalization Success"为纲，把 AI 辅助销售列为研究优先项 [jpssm2021-digital-selling p.1, p.23-25]。行业侧，Salesforce 年报自述其 CRM 市场地位与从 2000 年首版 CRM 起的云化扩张路径 [salesforce-annual-report p.20-21, p.37]。

## 核心框架

1. **SFA→CRM→数据分析三阶段**：自动化（记录）→ 关系管理（流程）→ 数据分析（洞察与 AI）[johnston-sf-management-12e p.26, p.94-96]。
2. **数字销售技术栈**：销售赋能平台、虚拟销售、AI 教练/推荐——学术共识是技术采纳的成功取决于"人-流程-技术"匹配而非工具本身 [jpssm2021-digital-selling p.1, p.23-25]。
3. **DSD（Direct Store Delivery）**：快消直达门店的配送+销售一体模式，是 SFA 打卡/车销数据的业务载体（CDSD 手册主题即 Direct Store Delivery 体系：司机/线路/门店执行）[cdsd-brochure p.1]。
4. **平台经济属性**：CRM 厂商以生态与数据闭环构筑份额 [salesforce-annual-report p.21, p.37]。

## 跨文献对照

- **一致**：SFA/CRM 的价值不在"记录"而在"把行为数据变成可分析资产"；打卡数据与真实拜访的偏差是数据质量的核心议题 [johnston-sf-management-12e p.114]。
- **互补**：Johnston 给管理与变革视角 [johnston-sf-management-12e p.94]；JPSSM 给学术框架与研究议程 [jpssm2021-digital-selling p.1]；Salesforce 年报给平台商业模型 [salesforce-annual-report p.37]；CDSD 手册给快消落地形态 [cdsd-brochure p.1]。
- **分歧**：厂商叙事（采纳=成功）与学术证据（采纳率长期偏低、需治理配套）之间存在张力 [jpssm2021-digital-selling p.1；salesforce-annual-report p.20]。

## 对 prism-ontology 的评审要点

1. **VisitRecord 与 ActualVisit 分离有强依据**：SFA 打卡是信息系统表示，物理拜访是事件——本体这一区分正是 SFA 文献与 DSD 实践的核心议题 [johnston-sf-management-12e p.114；cdsd-brochure p.1]。
2. **缺系统/来源实体**：本体 `hasSource` 是 ObjectProperty 却无 range，也没有 SFA 系统/数据平台类；文献视角下"数据来自哪个系统（SFA vs DSD 车销 vs 第三方平台）"决定可信度权重，应是受管概念（对应 `prism:source/*` 命名空间已注册却无 TTL 类定义）。
3. **执行禁令的盲区**：本体禁止 CRMStateMutation 概念（分析不回写），但 DSD/CRM 生态的现实是"洞察→行动→回写"闭环；PR 分析禁令应配 ElevationCandidate 的**受控行动流**建模（治理化的 Action Type），否则闭环在语义契约外发生，语义层失去监督能力 [johnston-sf-management-12e p.94-96]。
