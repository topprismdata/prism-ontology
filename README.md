# prism-ontology (棱镜极世界模型统一本体工程)

> **定位**：棱镜极 (TopPrism) 世界模型的上位语义权威源头与统一本体工程底座。  
> **核心原则**：统一治理、稳定演进、严禁概念坍缩、通过受管 Operational Profile 单向赋能下游业务洞察与决策组件。

---

## 1. 架构分层体系

本项目遵循世界模型标准分层架构（L0 ~ L2+）：

```text
prism-ontology
├── L0/L1 通用元模型 (ontology/core/)
│   └── Entity, Role, Event, Activity, Observation, Policy, Constraint, Eligibility, Decision, Plan, DerivedEstimate, Evidence, Organization, TimeInterval
├── L2 领域本体模块
│   ├── 售点领域 (ontology/outlet/): Outlet, Brand, CommercialSite, CustomerAccount, CustomerRole, AdministrativeRegion, Territory, ChannelType, ServiceRelationship, OutletObservation
│   ├── 洞察领域 (ontology/insight/): AnalysisIntent, MetricDefinition, MetricObservation, ComputationActivity, InsightClaim, QualityAssessment, InsightPackage, ElevationCandidate
│   └── 销售拜访领域 (ontology/sales-visit/): VisitPurpose, VisitMode, VisitModeConstraint, VisitModeEligibility, VisitPlan, ActualVisit, VisitRecord
├── 场景运行契约 Profile (profiles/)
│   └── outlet-insight: 售点洞察场景编译 Profile (v0.1.0-RC)
├── 需求与提案治理 (proposals/)
│   └── mousheng: 接收下游需求证据并进行 6 态治理裁定
└── 编译与发布归档 (dist/)
    └── 确定性发布的 Profile 包与 SHA-256 Checksums
```

---

## 2. 核心防坍缩底线（SHACL 机器断言防线）

1. **`Outlet ≠ CustomerAccount ≠ CustomerRole`**：客观网点实体、IT系统账户与业务情境角色三权分立。
2. **`AdministrativeRegion ≠ Territory`**：法定国家行政区划与企业销售辖区责任路线物理隔离。
3. **`Observation ≠ DerivedEstimate ≠ WorldStateFact`**：多源外部动态观测、算法派生估计与既成事实严格区分。
4. **`Eligibility ≠ Decision ≠ Plan ≠ ActualVisit`**：准入资格、决策、计划与实际发生拜访事件不可混淆。
5. **`ActualVisit ≠ VisitRecord`**：物理拜访发生事件与销售打卡记录信息对象解耦。
6. **`InsightClaim ≠ WorldStateFact`**：洞察主张为分析观点，默认不修改世界状态。
7. **Profile 契约禁止执行对象**：Profile 严禁输出 `Task`, `RoutePlan`, `ScheduleDecision`, `CRMStateMutation`, `WorldStateWriteCommand`。

---

## 3. 下游消费依赖关系

依赖方向严格单向：
```text
prism-ontology  ──(编译发布 Profile)──>  mousheng-outlet-insight (消费 Profile)
```
- 下游谋圣组件提出需求证据与 `proposed` 候选 URI；
- 本项目通过 `proposals/` 提案治理流程进行裁定后发布 Profile；
- 下游读取 Profile 并校验 SHA-256 生成 `profile.lock`。
