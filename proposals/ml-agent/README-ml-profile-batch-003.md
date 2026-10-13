# ml-profile-batch-003：ML Profile 局部概念提案（MS-PROP-038..047）

提交方：TopPrism ML Agent Program（cultivating-ml-agent）
日期：2026-10-13
状态：proposed / governance_review

## 批次定位

本批次提交 `prism-ml` 局部命名空间的 **10 个场景概念**（`prism:ml/*`），来源
`cultivating-ml-agent@main docs/ontology/ml-profile/0.1.0/`（concepts.yaml +
mappings.yaml，全部 pending_proposal）。**不含**共享核心净新增八项——那批
（WorldStateRef/Task/Goal/Candidate/Execution/Claim/Outcome/Capability）已由
`ml-core-batch-001`（PR #21）提交，本批次对其只有引用与联动，无重复提案。

## 编号避让说明（重要）

GOVERNANCE.md §2 台账（main）停留在 `MS-PROP-022`，但实际编号占用为：

| 编号 | 归属 | 状态 |
|---|---|---|
| 023 | proposals/datagovernance（DQ 裁决协议） | **已并入 main**（5dc427c）——main 台账未推进，建议委员会顺手修正 |
| 023-030 | ml-core-batch-001（PR #21） | open；**注意其 023 与已并入的 datagovernance 023 冲突**，需重编号或让 datagovernance 保号 |
| 031-037 | ml-sales-batch-002（PR #23，SRP 销售拜访概念） | open |
| **038-047** | **本批次** | 避让以上全部 |

## 概念关系图（本批次内部 + 对外依赖）

```text
prism:core/Activity ── MLTask(038)          ExperimentRun(044) ── 候选父类
                          │ 绑定                 │ 消耗           core/Execution(PR#21)
                          ▼                      ▼
prism:core/Plan ── ExperimentPlan(043) ── 含候选集 ── Hypothesis(047)
                                                  依赖父类 core/Claim(PR#21)
prism:core/InformationObject ── DatasetSnapshot(039) ─ 冻结 ─ FeatureSet(040)
                            ├── ValidationProtocol(041) ─ 求值口径 ─ MetricDefinition(042)
                            └── ModelArtifact(045) ─ 产出 ─ ExperimentRun(044)
prism:core/Evidence ── TransferEvidence(046) ─ 回指 ─ DecisionTrace(ANF 投影)
```

## 预期裁定与降级路径

- 10 项均自评为场景特化，**预期 profile_local**（保留在 ml-profile，不上推 core）。
- 两项主动给出合并/降级路径：MetricDefinition(042) 可 aligned_to
  `prism:insight/MetricDefinition`（定位同构）；Hypothesis(047) 随父类 Claim
  裁定联动（Claim 被拒则本项 mapping_only）。
- **EvaluationResult 显式不提案**：评估结果一律落 ANF evidence-envelope，
  DecisionTrace 为唯一完整保真载体（cultivating-ml-agent ADR-002 决议），
  ml.shacl.ttl 已设 ProhibitEvaluationResultShape。这是本批次的防膨胀自查核心。

## 与既有治理资产的一致性

- Capability 生命周期词表：本批次不涉 Capability（PR#21 资产），但提示委员会：
  ANF capability-record 已升 **0.2.0 规范词表**（ANF ADR-002，
  candidate/observed/validated-local/validated-transfer/stable/disputed/deprecated），
  PR#21 的 MS-PROP-030 文件中 lifecycle 六态描述已过时，建议随评审更新。
- 防泄漏门禁（G1-G6）、内容哈希身份、supersedes 修订链等实现事实见
  `cultivating-ml-agent` SPEC-001..007 与 220 测试基线（含跨仓投影互验 3/3）。

## 文件清单

MS-PROP-038-ml-task / 039-dataset-snapshot / 040-feature-set /
041-validation-protocol / 042-metric-definition / 043-experiment-plan /
044-experiment-run / 045-model-artifact / 046-transfer-evidence / 047-hypothesis
