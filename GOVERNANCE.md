# prism-ontology 治理章程与规范 (GOVERNANCE)

**生效版本**：v0.2.0  
**维护机构**：棱镜极 TopPrism 统一本体治理委员会  

---

## 1. 命名空间与 URI 规范

本项目所有本体概念使用统一前缀体系，并通过各 Profile 根目录下的机器可读契约 [`prefix-map.json`](./profiles/outlet-insight/prefix-map.json) 与 [`context.jsonld`](./profiles/outlet-insight/context.jsonld) 提供标准前缀解析支持：

| 前缀 | 命名空间 URI | 适用领域 |
|---|---|---|
| `prism:core/` | `prism://ontology/core/` | L1 通用元模型概念 (Entity, Event, Observation 等) |
| `prism:outlet/` | `prism://ontology/outlet/` | L2 售点领域概念 (Outlet, Brand, CommercialSite 等) |
| `prism:insight/` | `prism://ontology/insight/` | L2+ 洞察产物概念 (AnalysisIntent, InsightClaim 等) |
| `prism:sales/` | `prism://ontology/sales-visit/` | L2 销售拜访边界概念 (CustomerAccount, CustomerRole, VisitPlan, SalesRep, Route) |
| `prism:metric/` | `prism://ontology/metric/` | 业务受管度量指标定义 |
| `prism:quality/` | `prism://ontology/quality/` | 数据质量与实体匹配评估指标 |
| `prism:lifecycle/` | `prism://ontology/lifecycle/` | 实体生命周期与时间轴属性 (EntityOnlineTime, RecordCreationTime) |
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
2. **防概念膨胀**：严禁将临时实验字段、批次流水号或特定平台专有 ID 直接提升为主概念。宽表临时物理列必须隔离至 `field-mapping.yaml`（`governance_status: mapping_only`）。
3. **提案编号管理**：提案采用 `MS-PROP-001` 起单调递增编号，并在 `proposal-decisions.yaml` 中永久追溯，严禁跨提案复用或覆盖编号（当前编号空间已分配至 `MS-PROP-022`）。
4. **外部标准对齐**：
   - 观测模型对齐 W3C SOSA/SSN (`sosa:Observation`)
   - 质量评估对齐 W3C DQV (`dqv:QualityMeasurement`)
   - 血缘溯源对齐 W3C PROV-O (`prov:Entity`, `prov:Activity`, `prov:Agent`)
   - 术语与分类学对齐 W3C SKOS (`skos:Concept`)

---

## 3. Profile 编译与版本发布规范

### 3.1 两段式发布流程 (Two-Stage Release Flow)
为确保发行制品（`dist/`）的机器可复现性与溯源真实性，发布必须执行严格的两段式流程：
1. **Stage 1 (Source Commit)**：提交所有本体 TTL 源码、Profile 注册表、提案与测试，在 Git 工作树完全干净（Clean Tree）的状态下生成源码提交。
2. **Stage 2 (Distribution Build & Stamp)**：基于 Stage 1 的 Commit 哈希运行 `build_profile_release.py`，生成确定性发行目录，使 `profile-manifest.json` 中真实签署 `git_commit` 与 `clean_working_tree: true`。
3. **Stage 3 (Tagged Release)**：提交发行包制品，签署与 Manifest 版本一致的 Annotated Git Tag（如 `outlet-insight-v0.1.0-rc3`）。

### 3.2 发行包不可变性铁律 (Artifact Immutability)
1. **历史发行包只读**：任何已签署 Git Tag 的发行目录（如 `0.1.0-rc1`、`0.1.0-rc2`）属于不可变历史资产，**绝对禁止原地覆写或篡改**。
2. **增量即升版**：任何修复、模型补充或重新编译必须递增版本号（如 `0.1.0-rc3`），并在全新的版本子目录中生成。
3. **禁止孤儿发行包**：`dist/` 下除合法白名单版本目录外，严禁保留无 Tag 签署、无溯源 Manifest 的孤儿目录。

### 3.3 版本号策略 (SemVer)
- `0.1.0-rcX`：发布候选版本（Release Candidate），用于跑通端到端消费验证。
- `1.0.0`：下游生产验证 100% 通过且生成真实 `profile.lock` 后的首个正式稳定版本。
- 主版本号升级 (Breaking Changes) 触发条件：修改 L1 元模型、删除已发布实体/度量、变更核心命名空间 URI 或破坏性变更 SHACL 约束。

