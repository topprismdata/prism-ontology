---
type: concept
title: 销售预测 (Sales Forecasting)
aliases: [demand forecasting, sales projection]
sources: [johnston-sf-management-12e, kotler-marketing-mgmt-15e, zoltners-accelerating-sfp]
---
# 销售预测 (Sales Forecasting)

## 定义

销售预测是对未来一段时间、特定市场范围内销售量的预估，是配额设定、预算、生产与人力规划的共同输入。Johnston & Marshall 将其归入销售计划的核心活动，区分**主观法**与**统计法**两大族，并强调"销售经理必须理解每种方法的偏差来源" [johnston-sf-management-12e p.169]。Kotler & Keller 从需求测量角度定义：市场预测是在既定营销环境下、既定营销支出水平上的预期市场销量，并区分市场潜量/市场预测/公司销售预测三层 [kotler-marketing-mgmt-15e ch.3]。

## 核心框架

1. **主观（判断）方法**：销售代表汇总法、经理汇总法、Delphi 技术（多轮匿名专家意见收敛，"minimizes effects of group"）——Johnston 给出各方法优缺点对照 [johnston-sf-management-12e p.169-172]。
2. **统计（时间序列）方法**：移动平均、指数平滑、回归——同章列出 [johnston-sf-management-12e p.170]。
3. **预测-配额-潜力链**：Zoltners & Sinha 强调预测困难源于环境持续变化（"forecasting is difficult—the environment changes constantly"），并将预测作为潜力估计与目标设定的上游 [zoltners-accelerating-sfp p.46, p.51]。
4. **需求测量分层**：Kotler 的市场潜量 → 市场预测 → 公司销售潜量级联 [kotler-marketing-mgmt-15e ch.3]。

## 跨文献对照

- **一致**：预测是估计而非事实；判断法易受激励扭曲（代表低报以保配额），统计法对环境突变迟钝——两书均提示混合使用 [johnston-sf-management-12e p.169-172；zoltners-accelerating-sfp p.51]。
- **互补**：Johnston 站在销售管理运营视角（方法选择与偏差治理）[johnston-sf-management-12e p.169]；Kotler 站在营销战略视角（潜量层级与营销支出弹性）[kotler-marketing-mgmt-15e ch.3]。
- **分歧**：无实质分歧，但 Zoltners 更强调预测应服务于"部署决策"（allocating selling effort），而非终点本身 [zoltners-accelerating-sfp p.46]。

## 对 prism-ontology 的评审要点

1. 本体把 `DerivedEstimate` 定义为"算法推导的估计，严禁等同事实"，与文献"预测≠事实"完全一致——方向正确 [johnston-sf-management-12e p.169]。
2. **缺预测结构**：`RevenuePotential*` 三个估计变体存在，但无 Forecast 类、无 forecastHorizon（预测期）、无预测方法引用（methodUsed）、无置信区间——文献明确方法与偏差来源是预测语义的一部分 [johnston-sf-management-12e p.169-172]。
3. **缺"潜力 vs 预测 vs 目标"三层的区分**：Kotler/Zoltners 的潜量级联表明三者是不同概念（潜力=上限估计，预测=期望，配额=目标）；本体的 metric-definitions 只有估计类指标，目标/配额概念整体缺失，与 motivation-compensation-quota 页的发现一致。
