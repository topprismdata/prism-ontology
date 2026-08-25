# prism-ontology 治理章程与规范 (GOVERNANCE)

**生效版本**：v0.1.0-RC1  
**维护机构**：棱镜极 TopPrism 统一本体治理委员会  

---

## 1. 命名空间与 URI 规范

本项目所有本体概念使用统一前缀体系：

| 前缀 | 命名空间 URI | 适用领域 |
|---|---|---|
| `prism:core/` | `prism://ontology/core/` | L1 通用元模型概念 (Entity, Event, Observation 等) |
| `prism:outlet/` | `prism://ontology/outlet/` | L2 售点领域概念 (Outlet, Brand, CommercialSite 等) |
| `prism:insight/` | `prism://ontology/insight/` | L2+ 洞察产物概念 (AnalysisIntent, InsightClaim 等) |
| `prism:sales/` | `prism://ontology/sales-visit/` | L2 销售拜访边界概念 (CustomerAccount, CustomerRole, VisitPlan) |
| `prism:metric/` | `prism://ontology/metric/` | 业务受管度量指标定义 |
| `prism:quality/` | `prism://ontology/quality/` | 数据质量与实体匹配评估指标 |
| `prism:source/` | `prism://ontology/source/` | 外部观测数据源标识 (Ctrip, Dianping, AMap) |
| `prism:profile/` | `prism://ontology/profiles/` | 场景运行 Profile 发布 URI |

---

## 2. 提案治理六态状态机 (Proposal Decision Lifecycle)

下游需求方（如谋圣）提出的任何 `proposed` 候选概念，必须在 `proposals/` 中经过以下 6 种状态之一的治理裁定：

```text
                 ┌──────────────────────────────────────────────────────────┐
                 │  Downstream Proposed Concept (待审候选)                  │
                 └────────────────────────────┬─────────────────────────────┘
                                              │ 治理委员会评审
            ┌────────────────┬────────────────┼────────────────┬────────────┐
            ▼                ▼                ▼                ▼            ▼
      【accepted】   【aligned_to_】    【profile_】     【mapping_】   【rejected】
      正式进入上层     已有概念吸收     仅保留在场景     仅作为字段清洗  概念混淆/越界
      Reference       直接复用         Profile局部      留在本地表映射   彻底废弃
            │
            └───────────────► 【deferred】(语义待业务进一步清晰，延期治理)
```

### 裁定原则：
1. **五问法裁定**：对象是否客观稳定？跨供应商/跨企业是否成立？跨项目是否需要统一推理？定义是否明确？
2. **防概念膨胀**：严禁将临时实验字段、批次流水号或特定平台专有 ID 直接提升为主概念。
3. **外部标准对齐**：
   - 观测模型对齐 W3C SOSA/SSN (`sosa:Observation`)
   - 质量评估对齐 W3C DQV (`dqv:QualityMeasurement`)
   - 血缘溯源对齐 W3C PROV-O (`prov:Entity`, `prov:Activity`, `prov:Agent`)

---

## 3. Profile 编译与版本发布规范

1. **版本号策略 (SemVer)**：
   - `0.1.0-rc1`：首个发布候选版本（Release Candidate），用于与下游跑通端到端消费验证。
   - `1.0.0`：下游验证 100% 通过且生成真实 `profile.lock` 后的首个正式稳定版本。
   - 主版本号升级 (Breaking Changes) 触发条件：修改 L1 元模型、删除已发布实体/度量、变更核心 SHACL 约束。
2. **发布包完整性契约**：
   - 每个 Profile 发布必须包含 `checksums.sha256` 完整性哈希清单。
   - 下游通过 `profile.lock` 锁定该哈希，任何未经治理委员会重新编译签署的 Profile 篡改均会被运行时阻断。
