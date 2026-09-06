---
type: concept
title: 采购中心与销售角色分离 (Buying Center & Selling Roles)
aliases: [buying center, buying centre, selling center]
sources: [kotler-marketing-mgmt-15e, johnston-sf-management-12e, woodburn-sam-handbook]
---
# 采购中心与销售角色分离 (Buying Center & Selling Roles)

## 定义

**采购中心（Buying Center）**是 B2B 采购决策中所有参与者的集合，Kotler & Keller 按决策角色分为七类：发起者(initiator)、使用者(user)、影响者(influencer)、决定者(decider)、批准者(approver)、购买者(buyer)、把关者(gatekeeper)——"把关者是有权阻止卖家或信息接触采购中心成员的人" [kotler-marketing-mgmt-15e p.109, p.122]。Johnston & Marshall 在销售组织章节对称提出 **Selling Center（销售中心）**概念：卖方一侧同样是一个多角色团队（销售、技术支持、服务、管理层），"Selling Centers and Buying Center" 是组织销售力量时的基本分析单元 [johnston-sf-management-12e p.50/p.58]。SAM 文献进一步指出采购中心方法（Johnston & Bonoma 1981）是理解大客户价值链的关键透镜 [woodburn-sam-handbook p.398, p.471]。

## 核心框架

1. **七角色采购中心**（Webster & Wind 传统，Kotler 采用）：同一自然人可承担多角色，角色随采购阶段变化 [kotler-marketing-mgmt-15e p.109, p.122]。
2. **Selling Center 对称结构**：销售侧团队角色化，是团队销售（team selling）的组织基础 [johnston-sf-management-12e p.50]。
3. **SAM 账户团队**：战略客户管理中，跨职能账户团队与客户采购中心逐层对接 [woodburn-sam-handbook p.398]。

## 跨文献对照

- **一致**：三方均主张"角色是情境激活的关系，不是人的固有属性"——同一采购员对不同品类可能是 user 也可能是 decider；这正是"实体≠角色"建模的业务根据。
- **互补**：Kotler 给出买侧角色清单 [kotler-marketing-mgmt-15e p.122]；Johnston 给出卖侧对称结构并讨论跨组织界面管理 [johnston-sf-management-12e p.50]；Woodburn 把两者接入大客户价值创造流程 [woodburn-sam-handbook p.471]。
- **分歧**：角色清单的粒度（Kotler 7 角色 vs SAM 的更粗三层）——分层粒度依场景而变，本体应支持角色类型受管可扩展。

## 对 prism-ontology 的评审要点

1. 本体的 `Outlet playsRole CustomerRole` + `CustomerAccount represents Outlet` 结构与"角色情境激活"完全同构，**业务根据坚实** [johnston-sf-management-12e p.50]。
2. **缺卖侧角色**：本体有 CustomerRole 但没有 SellingCenter 侧的概念——SalesRep 已补（issue #5），但"团队销售"中技术/服务/管理角色无承载类；SAM 页指出的账户团队结构无对应建模。
3. **角色定义不对称**：CustomerRole 注释说"未服务网点尚未激活此角色"（anti-rigid 意识正确），但无任何公理表达"角色由 ServiceRelationship 激活"——按 UFO relator 模式，应加 `CustomerRole activatedBy ServiceRelationship` 类似约束。
4. 关系缺失：无"角色作用于特定关系/时段"的限定（validDuring 已定义但从未被角色类使用）。
