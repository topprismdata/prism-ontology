---
type: concept
title: 销售力量规模与部署（Sales Force Sizing & Deployment）
aliases: [sales force size, sizing, workload method, deployment problem, FTE, 盈亏平衡法, 资源分配]
sources: [ejor2014-sf-deployment, darmon2002-ejor-territory-sizing, zoltners-sf-design, zoltners-accelerating-sfp, jpssm2008-sfe-framework]
---
# 销售力量规模与部署（Sales Force Sizing & Deployment）

## 定义（综合多来源）

- **部署问题（OR 权威定义）**："销售力量部署问题涉及同时求解四个相互关联的子问题：**销售力量规模（sizing）、销售员驻点（locations）、销售辖区对齐（alignment）、销售资源分配（resource allocation）**；目标是最大化总利润贡献。"市场划分为 SCU，"sizing 即决定进入市场区域所需销售员数量——选定规模也就同时决定了辖区数与驻点数"；部署是**聚合计划**，规划期通常一年，"某客户每周/每月拜访几次、哪天拜访、访问顺序"属于后续规划阶段。（ejor2014-sf-deployment, p.1）
- **规模决策的战略地位**：规模与结构是销售力量有效性驱动因素（definer drivers）之首。（jpssm2008-sfe-framework, p.6）
- **为什么规模是利润杠杆**："销售力量创造销售——它不只是费用，它驱动 top line"；许多 B2B 公司最大的销营预算项就是销售员薪酬、奖金与基础设施。（zoltners-accelerating-sfp, p.20）

## 核心框架（逐个带出处页码）

### 1. 销售响应函数：努力→销售的实证形态
辖区级数据："任何辖区年销售额的 20%-90% 源于当年销售员的努力"；曲线呈边际递减——"产品渗透殆尽时额外拜访产生的增量销售极少"（zoltners-sf-design, p.243）。关键复杂化是**遗留效应（carryover）**：撤销努力后销售不为零，来自前期建立的关系；急性用药 vs 慢性用药案例说明短期冲击与 carryover 因品类而异；因此"规模变化的总增量影响不是即时的，而是随时间增大"——裁掉 10 人次年损失 $5M，随后一年损失 $15M（zoltners-accelerating-sfp, p.91-94）。

### 2. 工作量法（workload build-up）
以"客户潜力分层 × 服务所需小时/周"为基础表（>$1M 账户 26.4 小时/周……<$25K 1.4 小时/周），逐层乘账户数得 FTE 需求（容量 = 每销售员每年 1,880 小时），示例合计 504 FTE；再按"覆盖深度"生成备选策略：策略 A 全覆盖 >$50K 客户需 161 人；策略 B 加深服务 >$100K 客户（39.6 小时/周）放弃 $100K 以下、同为 161 人——同样的规模可在"广度 vs 深度"间再分配。（zoltners-sf-design, p.241-242, Table 7.1-7.2）

### 3. 盈亏平衡法（break-even）
五步：估计全员平均销售额 → 计算毛贡献率（例 ($900-$300)/$900=66.7%）→ 盈亏平衡销售额 = 销售员成本/毛贡献率（$118,000/0.667=$176,911）→ 按平均销售/盈亏平衡比（例 5.65）与 carryover 查表判断"规模过小/合适/过大"。（zoltners-sf-design, p.257-258）注意反对直觉的判据："如果人均增量销售高于销售员全成本，那么增员同时降低人均销售额并提高利润——'人均销售高'本身不是好状态"。（zoltners-accelerating-sfp, p.82）

### 4. OR 求解进展（EJOR 2014）
将四子问题整合为含无穷多 0-1 变量的半无限规划；线性松弛用列生成求解、解析取约简成本最大列；给出整数解的紧致上下界（Branch-and-Price）；**显式连通性约束**用流变量表达；医药行业实例（50 个潜在驻点、500+ SCU）1,273 秒求解、gap<0.01%，比 Drexl-Haase (1999) 的约 3% gap 减半。（ejor2014-sf-deployment, p.1-2）文中术语口径：account=预期购买公司产品的客户；SCU=较小地理单元（县、邮编、公司交易区），可含多账户；territory=带责任销售员的 SCU 集合，"负责"=为辖区内全部（潜在）账户提供服务（p.2）。

### 5. 信息管理对最优规模的影响（Darmon 2002）
"收集与处理辖区和客户信息是销售员任务的主要方面；其效果取决于市场信息（客户需求与潜力、接触后成单概率等）的数量与质量"——信息活动与有效销售时间**竞争同一时间资源**。论文给出估计信息收集/处理成本的统计程序，用于估计"每个销售员可被指派的最盈利辖区规模，从而估计最优销售力量规模"。（darmon2002-ejor-territory-sizing, p.1-2）反直觉结论：信息过量同样有害——"若销售员在收集信息上超时，情报的量质提升可能不抵销售时间损失"（p.2）；信息水平随经验动态变化，故"辖区规模可能过大、过小，也可能恰到好处，且随销售员职业生涯移动"（p.7-10）；高绩效者更会找信息（p.2，MacIntosh et al. 1992）。

## 跨文献对照（一致/互补/分歧）

- **一致**：三个流派共享同一因果骨架：销售努力→销售响应（凹函数）→ 利润最大化决定规模与分配。Zoltners 用"增量分析 + carryover"（zoltners-accelerating-sfp, p.91-94），EJOR 用"凹响应函数 + 上下界"（ejor2014 p.1），Darmon 用"时间预算在信息 vs 销售间分配"（p.2）。
- **互补**：zoltners-sf-design 提供管理者可自算的两种方法（工作量法 p.241-242、盈亏平衡法 p.257-258）；ejor2014 提供整合四子问题的最优解法与连通性处理；darmon2002 揭示**信息成本是被前两者普遍忽略的时间项**——SCU 数量越大、账户越多，信息负担越重，最优辖区反而应更小，人员规模相应更大。
- **分歧**：对"连通性约束"的处理强度不同——Zoltners 1983 用层次邻接树硬保证连通（见辖区页），Skiera-Albers 的联合模型"若愿意可用启发式构造连通辖区但不显式约束"（ejor2014 p.2 转述），ejor2014 则把连通性写成模型内流约束。对规模调整的短期/长期效应，教科书法（盈亏平衡比）是静态快照，Zoltners 明确警告 carryover 使静态判断失真（p.94）。
- **规模与对齐互为条件**：EJOR 明确"sizing 即决定辖区数"（p.1）；zoltners-accelerating-sfp 的对齐章节（p.152-154）显示对齐问题反过来伪装成规模问题（"对齐问题常伪装成其他问题"）。

## 对 prism-ontology 的评审要点

1. **缺"规模/部署决策"事实类**：本体只有 Territory 无 `SalesCapacityPlan`（目标规模、FTE 容量假设、生效期）。工作量法的三个口径应成为 MetricDefinition：`serviceHoursPerAccountTier`（p.241 的 26.4-1.4 小时谱）、`annualCapacityHours=1880`（p.241 注）、`coverageDepthPolicy`（p.242 的广度/深度选项）。
2. **缺 SalesResponse/Carryover 语义**：20%-90% 的努力归因带（zoltners-accelerating-sfp p.91）与 carryover 意味着 InsightClaim 里"拜访→销售"的因果推断必须带滞后窗与品类情境； DerivedEstimate 应支持 `lag` 与 `carryoverFraction` 属性，否则把当年 SOVI/销量变化全归因于拜访频次会系统性高估。
3. **信息活动应占时间预算**：darmon2002 p.1-2 证明 VisitRecord/打卡所代表的"服务时间"与"信息收集时间"必须分开计量——本体若只有一个 visit duration，将无法表达"过量信息收集挤压销售时间"这一规模效应机制。建议 Observation 增加活动类型维度（selling vs information-gathering vs merchandising，后者也见于 brandidea p.3）。
4. **部署四子问题 = 本体分工图**：ejor2014 p.1 的 sizing/locations/alignment/resource allocation 四分法可直接作为 prism-ontology 销售管理世界模型在这一域的顶层分解检验——当前垂直切片只覆盖 alignment（Territory）与 resource allocation 的一角（VisitPlan），缺 locations（驻点）与 sizing 两个子域。
5. **SCU 定义应跨书对齐**：EJOR p.2 的 SCU 口径（县/邮编/交易区、可含多账户）与 Zoltners 1983 一致，可放心作为本体 PlanningUnit 类的权威出处。
