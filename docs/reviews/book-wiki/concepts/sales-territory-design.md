---
type: concept
title: 销售辖区设计（Sales Territory Design / Alignment）
aliases: [territory alignment, 辖区对齐, SCU, districting, realignment, workload balancing]
sources: [zoltners1983-territory-alignment, sales-territory-design-chapter, us7620564-territory-patent, brandidea-pjp-rural, zoltners-sf-design]
---
# 销售辖区设计（Sales Territory Design / Alignment）

## 定义（综合多来源）

- **奠基定义（Zoltners & Sinha 1983, Management Science）**："销售辖区对齐问题可视为把小的地理销售覆盖单元（sales coverage units, SCUs）归组为更大的地理簇——销售辖区——使结果在管理上相关的对齐准则下可接受（或最优）的问题。"SCU 通常取能获得数据的销售计划单元，如县、邮政编码。（zoltners1983-territory-alignment, p.2-3）
- **30 年实践综述的扩展定义**："把客户账户及其关联销售活动指派给销售员与团队，称为销售辖区对齐（alignment）"，同义词包括 assignment、realignment、deployment、districting、design；并强调对齐在**销售力量结构**的语境中定义——通才结构按地理（邮编/县/州）划分，市场型结构按"地理+账户规模/类型/行业"，产品型与活动型结构则一个账户由多个销售员覆盖不同产品或活动。（sales-territory-design-chapter, p.3）
- **为什么必须对齐**：产品引入与市场迁移需要持续调整；规模、组织变化与"改善覆盖、公平工作量、缩短差旅时间"的目标都会触发重对齐；多数公司一次重对齐要耗费数月人月。（zoltners1983-territory-alignment, p.2）

## 核心框架（逐个带出处页码）

### 1. SCU-指派模型（0-1 规划）
对 m 个辖区、n 个 SCU（n>>m），决策变量 x_ij=1 表示辖区 i 含 SCU j；约束"每 SCU 恰指派到一个辖区"；辖区属性值由 SCU 属性线性聚合，常见属性为 workload、sales potential、sales volume、距离；目标函数选优、约束淘汰劣质结构。早期模型（Hess-Samuels 的 GEOLINE）以"紧凑 + 单属性均等"为目标，缺陷有五：LP 松弛取整后可能非最优、取整破坏均衡、不保证连通（contiguous）、只支持单一准则、无视交通走廊与不可通行障碍（山脉水道）——"欧氏紧凑对政治选区重划重要，对销售辖区未必：经旅行线路的可达性重要得多"。（zoltners1983-territory-alignment, p.4-5）

### 2. 好对齐的属性与通用模型
Zoltners-Sinha (MSZ) 模型保证：**连通性**（用层次式 SCU 邻接树、以最短路定义可达，p.11）、**对一个或多个准则均衡**（上下界约束，实践中辖区均衡度多在完全均衡 5% 以内，p.15）、**地理相容**；目标可设为最小化差旅时间、最小化扰动或最大化盈利。（p.20 结论）启发式"试错-调整"法虽永不产生不连通辖区，但不支持多准则且无法做大重构。（p.3）

### 3. 工作量-机会平衡图（workload vs opportunity）
对齐的两大经典均衡轴：以"理想辖区工作量"曲线与横线（理想覆盖）对照实际散点——工作量过大的辖区无法有效覆盖全部客户与潜在客户；过小的辖区把时间浪费在低产拜访上；"由于地理约束，一些偏差不可避免，但估计约 60% 的辖区工作量偏离理想值 15% 以上"——这就是均衡辖区的论证。（sales-territory-design-chapter, p.5）

### 4. 对齐的绩效级联与三方诉求
对齐对绩效有级联影响：紧凑而公平的对齐 → 公平的绩效评估、均衡工作量、可控差旅 → 士气与激励 → 行为 → 客户满意 → 公司结果。好对齐与平均对齐的差异估计为**销售额的 2%-7%**。三方诉求表：销售员要（成功机会、足够收入、保留偏爱客户、公平工作量、低差旅、好经理指派）；客户要（最少扰动、保留熟悉销售员、适当关注）；公司要（有干劲与留存的队伍、高销售、低费用、高利润）。附案例：激励支付差异（底部 10% 人均 $28,500 vs 顶部 $116,000）根因不是薪酬方案而是辖区潜力悬殊——"为辖区机会而非销售员绩效付费"。（sales-territory-design-chapter, p.3-4）

### 5. 对齐作为系统与决策支持（专利视角）
US 7,620,564 B1 把辖区规划固化为方法流程：从可量化特征导出目标、战略与目标账户清单 → 对历史销售记录分群分类 → 按辖区逐一分析生成 **territory dashboard** → 辖区战略分析（基于账户分群、销售目标）→ 战术行动计划 → 执行与跟进（goal tracking、60 天战略工作表、辖区计划评审）。其引用文献首位即 Zoltners & Sinha 1983。（us7620564-territory-patent, p.1）

### 6. 辖区内的下一层：Beat/PJP
快消乡村市场实践中，辖区先按客户潜力排序、筛出可服务售点，再做"Beat Plan/永久线路（PJP）"——"为一线人员制定的按日销售线路计划，以预定义频率服务门店"，兼顾下单、理货与竞品分析；优化目标含"理想 beat 规模（beat 内最优售点数与单店耗时）、最优渠道组合、逐店访问顺序"。（brandidea-pjp-rural, p.3-4）

### 7. 对齐的高频变动
"销售员连续两年保持同一辖区极为罕见"；小边界调整常发生（新账户、搬迁、人口结构变化），大重构必然发生在规模/结构变化、并购、市场变化、新品上市、新建队伍之时。（sales-territory-design-chapter, p.3）

## 跨文献对照（一致/互补/分歧）

- **一致**：1983 论文与 2005 综述同源同构——SCU→辖区的聚合、多准则均衡、地理可达性贯穿 22 年；综述把 1983 模型放到 ZS 1,500+ 项目、约 50 万个辖区的实践证据链上（sales-territory-design-chapter, p.3）。
- **互补**：1983 论文是**规范模型**（数学规划 + 解法 + HSAT 数据库）；2005 综述补充**对齐对绩效的传导机制与三方政治学**（谁想从对齐中得到什么）；专利展示**决策支持系统形态**（dashboard→战略→战术→执行闭环）；brandidea 补充**辖区内的线路粒度**（beat=日级 SCU 序列），说明 SCU→territory→beat→visit 是四级嵌套。
- **分歧**：目标函数选择文献内部并不统一——Lodish 主张边际盈利均等、Easingwood 主张工作量均等、Heschel 主张潜力+面积双准则（zoltners1983 p.3）；1983 模型用多准则调和之，但"均衡什么属性"始终是公司策略变量。另一个操作张力：最优化结果"几乎从不被原样实施"——经理会因不可量化因素（销售员以辞职威胁、偏爱客户被移走、过夜出差增多）修改最优解（p.20 结论）。
- **演进**：Zoltners-sf-design 把对齐嵌入更大设计流程（结构→规模→对齐）并强调 synced alignment（多角色共享辖区）的 free-rider 问题（zoltners-sf-design, p.188），与 2005 综述"对齐在结构语境中定义"一致。

## 对 prism-ontology 的评审要点

1. **Territory 的正确语义是"指派关系"而非"地理面"**：2005 定义（"assignment of accounts and activities to salespeople"）与 1983 定义（SCU 分组）共同表明：Territory = 一组 SCU/账户 + 一个负责人 + 一组活动。本体应把 Territory 建为 `TerritoryAssignment`（带生效期、版本、对齐准则），AdministrativeRegion/Outlet 仅是其地理基底——这正是"实体≠角色/指派"的又一例证。
2. **缺 SCU 层**：1983 p.3 的 SCU 是辖区的基本构件（县、邮编、售点簇）。本体有 AdministrativeRegion 但没有"SCU 作为可聚合 planning unit"的类，也没有 `SCUAttribute`（workload、potential、volume、距离）记录——没有 SCU 属性，对齐模型无法复现。
3. **均衡准则应可配置**：对齐属性的权威枚举 = workload/sales potential/sales volume/distance（1983 p.4）+ 连通性与可达性约束（p.5, p.11）。建议 MetricDefinition 增加 `AlignmentCriteria` 口径族，并把 HHI/CR4 类集中度指标与之并列——集中度是辖区设计的诊断量，不是目标量。
4. **Territory 需要版本与扰动概念**：2005 p.3 的"小调整常发、大重构可预期"与 1983 p.20 的"最小化扰动"目标要求 Territory 带 `validFrom/validTo`、`parentAlignment`、`disruptionCost` 语义；现有 VisitPlan 直接挂在 Territory 上会因重对齐而断链。
5. **多角色覆盖打破互斥假设**：产品型/活动型结构下一个账户被多个销售员覆盖（2005 p.3 的办公室用品商一账户最多 5 人），故 Territory→SalesRep 不能是 1:1，须为 `CoverageAssignment` 多对多（与组织结构页结论互证）。
6. **Beat 属执行层**：brandidea 的 beat/PJP/访问序列是路线执行事实——按架构禁令，建议本体只保留 Territory（策略层）并在 VisitPlan 内引用"日级线路"作为 Visit 的聚合，不把 Route 升格为本体核心类。
