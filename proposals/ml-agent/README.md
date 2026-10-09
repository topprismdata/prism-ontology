# ml-core-batch-001 — ML 共享核心净新增概念提案批次

**提案方**：TopPrism ML Agent Program (cultivating-ml-agent)
**提交日期**：2026-10-09
**状态**：`proposed`（八项逐项进入 GOVERNANCE.md §2 六态状态机评审，裁定权归治理委员会）
**编号空间**：MS-PROP-023 … MS-PROP-030（单调递增，紧接 MS-PROP-022）

## 1. 批次动机

计划基线 v0.1 §3 定义了 14 项共享核心概念，作为 ML 实验链路（ExperimentIR /
DecisionTrace）与既有售点、洞察、跨域求解场景共享语义的基础。经与
prism-ontology core.ttl（HEAD `9d93a99`）逐项对照（ADR-001 §决策.3 映射表），
**6 项可直接映射到已发布类，8 项在 L1 无对应类**。

ML 实验链路需要跨域共享语义：跨域求解往返（PJP/仓储适配器，SPEC-006 JSON
信封）要陈述"同一冻结初始状态、几次确定性执行、什么事实结果"；决策链要陈述
"什么主张被什么独立证据证伪"；能力治理要陈述"某能力在声明 scope 内可否复用"。
这 8 项语义若不上浮至 L1，上述跨域陈述只能停留在 ML 局部命名空间
（`prism://ontology/ml/`，status: local / pending_proposal），跨项目无法统一推理。
故按 ADR-001 处置规则以**一个提案批次**整体提交：一次提案、逐项审查、统一版本
锁定。

## 2. 提案索引

| 编号 | 文件 | URI | 名称 | 父类主张 | 与既有类关系（一句话） |
|---|---|---|---|---|---|
| MS-PROP-023 | `MS-PROP-023-world-state-ref.yaml` | `prism:core/WorldStateRef` | 世界状态引用 | `prism:core/InformationObject` | 关于冻结视图的只读陈述（指纹+冻结点），拒绝实体化（写入即越界） |
| MS-PROP-024 | `MS-PROP-024-task.yaml` | `prism:core/Task` | 任务 | `prism:core/Activity` | 声明式指派活动（Activity 子类），与 Plan 并列（边界 vs 编排），不携带执行状态 |
| MS-PROP-025 | `MS-PROP-025-goal.yaml` | `prism:core/Goal` | 目标 | `prism:core/InformationObject` | 可判定达成条件声明，与 Constraint（硬性准入约束）正交可关联 |
| MS-PROP-026 | `MS-PROP-026-candidate.yaml` | `prism:core/Candidate` | 候选 | `prism:core/InformationObject` | 比较对象的声明性规格登记，拒绝实体化；与 insight/ElevationCandidate 并列 |
| MS-PROP-027 | `MS-PROP-027-execution.yaml` | `prism:core/Execution` | 执行 | `prism:core/Activity` | 纯函数式执行簿记（Activity 子类），与 Event（时点事实）正交，消耗 Plan/Task 指称 |
| MS-PROP-028 | `MS-PROP-028-claim.yaml` | `prism:core/Claim` | 主张 | `prism:core/InformationObject` | 可证伪主张节点，与 Decision（授权选择）正交；与 insight/InsightClaim 为**子类关系**主张（InsightClaim 细化为 Claim 特化） |
| MS-PROP-029 | `MS-PROP-029-outcome.yaml` | `prism:core/Outcome` | 结果 | `prism:core/Observation` | 执行后事实记录（Observation 子类），拒绝 Event；显式不替代"评估结果"（ADR-002 不设实体） |
| MS-PROP-030 | `MS-PROP-030-capability.yaml` | `prism:core/Capability` | 能力 | `prism:core/InformationObject` | 受管能力登记，与 Role（角色承担）正交；概念面对齐 ANF capability-record 记录面 |

## 3. 八概念关系图（文本）

```text
继承面（parent 主张）
  prism:core/InformationObject ─┬─ WorldStateRef（只读状态指称）
                                ├─ Goal（可判定达成条件）
                                ├─ Candidate（受控比较登记）
                                ├─ Claim（可证伪主张）
                                └─ Capability（受管能力登记）
  prism:core/Activity ─┬─ Task（声明式指派，不携带执行状态）
                       └─ Execution（纯函数式执行簿记）
  prism:core/Observation ── Outcome（执行后事实记录，含负例）

实验/决策链路
  WorldStateRef ──(公共起点)──► Execution ──(产出)──► Outcome（事实，含负例）
  Task ──(圈定边界)──► Goal ──(给定证据机械判定：通过/证伪，只能证伪)
  Candidate ──(入赛受控比较)──► Outcome ──(独立 Evidence 评判)──► Claim
  Claim ──(四眼链授权选择)──► Decision【既有类，不在本批次】
  Capability ◄──(验证结论仅作门禁证据输入；激活=授权方人为动作)

与既有 Profile 的泛化-特化主张（本批次均不修改既有 TTL）
  prism:core/Claim ◄── prism:insight/InsightClaim（建议父子化，待 insight Profile 版本化）
  prism:core/Claim ◄── prism:ml/Hypothesis（ML 局部 proposed_local，随父类翻转）
```

## 4. 与 ADR-001「六可映射 / 八净新增」结论的对应

ADR-001 §决策.3 对计划 v0.1 §3 的 14 项共享核心逐项对照 core.ttl：

| ADR-001 结论 | 概念 | 本批次处置 |
|---|---|---|
| 可映射（6 项） | Observation、Estimate→DerivedEstimate、Evidence、Constraint、Decision、Plan | **不在本批次**：直接引用 `prism-core:` 已发布类，不另造同义类 |
| 净新增（8 项） | WorldStateRef、Task、Goal、Candidate、Execution、Claim、Outcome、Capability | **即本批次 MS-PROP-023…030**，一次提案、逐项审查、统一版本锁定 |
| ML 局部扩展（11 项） | MLTask、DatasetSnapshot、FeatureSet、ValidationProtocol、MetricDefinition、Hypothesis、ExperimentRun、ExperimentPlan、EvaluationResult、ModelArtifact、TransferEvidence | 默认不申请进入 core.ttl；EvaluationResult 显式不设实体（ADR-002） |

## 5. 五问法批次级结论

五问法逐问逐项见各提案文件 `five_questions` 段。批次级结论：8 项概念对象客观
稳定（实验/决策/能力治理的公共语义）、跨供应商成立（不以任何平台专有 ID 为
前提）、跨项目需要统一推理（ExperimentIR 与跨域适配共用）、定义明确（各项
definition 给出可判定边界）、不落入概念膨胀禁区（无临时实验字段、无批次流水号、
无平台专有 ID）。缺任一项，则 ExperimentIR 与 DecisionTrace 的跨域陈述只能停留
在 ML 局部命名空间。

## 6. 能力问题（CQ）汇总

每项净新增概念至少 1 条 CQ（表达力门槛）。完整评估（semantic_expressibility /
data_answerability / blocking_reason / handling_policy）见随批草案
`competency_questions.yaml` 摘要如下：

| CQ | 概念 | 场景 | 自然语言问题 | 表达力 | 数据可答 |
|---|---|---|---|---|---|
| CQ-001 | WorldStateRef | 跨实验初始状态同一性判定 | 这次实验与上次实验面对的是不是同一个冻结的初始状态（同一数据快照与环境前置事实）？ | pass | full |
| CQ-002 | Task | 任务边界清单 | 组织内当前登记了哪些机器学习任务，各自圈定了什么数据、验证协议与度量选型边界（且不携带执行状态）？ | pass | full |
| CQ-003 | Goal | 达成条件判定 | 某实验声明的达成条件是什么？当前证据支持『通过』还是『证伪』？ | pass | full |
| CQ-004 | Candidate | 候选入赛合规性 | 某次受控比较中进入了哪些候选？每个候选与基线是否同协议、预算是否越界？ | pass | full |
| CQ-005 | Execution | 执行可复现性审计 | 某计划被确定性执行了几次？每次的输入指纹、产出工件与记录是什么？ | pass | full |
| CQ-006 | Claim | 被证伪主张清单 | 哪些『某改动会改善某度量』的主张被证据证伪了？各自引用了什么独立证据？ | pass | full |
| CQ-007 | Outcome | 跨域往返事实回查 | 上次跨域求解往返的事实结果是什么（哪些字段有值、哪些为空）——只报事实，不报评价？ | pass | full |
| CQ-008 | Capability | 能力复用资格查询 | 某能力候选在哪些任务家族上验证过、有无负例与争议、在声明的 scope 内可否复用？ | pass | partial |

CQ-008 blocking_reason：晋级门禁（预注册阈值：min_task_success>=3、
min_task_families>=2、require_negative_case、min_negative_transfer>=1、
max_evidence_age_days=180、require_no_dispute、activation_authority=A2）由 A 线
upgrade/p5-governance 落地；该分支合入前无机器可查的统一验证记录。
handling_policy：合入后由治理测试支持完整回答；此前人工查 ANF capability-record
逐条核对，激活永远是授权方人为动作，不做自动晋升。

## 7. 防概念膨胀自检（GOVERNANCE.md §2 裁定原则 2）

- [x] 不含任何临时实验字段（硬门字段留 ML 特化层：baseline_same_protocol、budget_bounds 等）
- [x] 不含批次流水号（ml-core-batch-001 仅作批次组织标识，不进入本体 URI）
- [x] 不含平台专有 ID（MLflow/ANF 等仅作事实源与记录面对照，不映射为类）
- [x] 八项均不申请新增属性（proposed_properties 留空；接受后由上游 SHACL NodeShape 补充约束）
- [x] 与既有 16 个 L1 类及 InsightClaim 逐一声明关系，无同义重复类（Claim 与 InsightClaim 已显式声明为泛化-特化主张而非正交重复）

## 8. 边界备忘与提交方声明

- 批次通过前，8 项概念仅存在于 ML 局部命名空间（`prism://ontology/ml/`，
  status: local / pending_proposal），禁止跨 Profile 复用，不发生任何行为变化。
- 本批次为**纯新增提案**：不修改 `proposal-decisions.yaml`（委员会裁定记录，
  提交方不写）、不动 `ontology/**`、`profiles/**`、`dist/**`、`scripts/**`、
  `tests/**`；编号 MS-PROP-023…030 是否生效以委员会裁定为准。
- 接受后回灌路径（提案方仓库侧，非本仓库动作）：compatibility BOM 以新版本
  锁定引用；mappings.yaml 以 supersedes 语义更新映射链（如 MLTask → Task →
  Activity）；pending_proposal 状态随裁定翻转。
- 八项概念定义与提案方仓库草案（docs/ontology/proposals/ml-core-batch-001/
  concept-proposals.yaml）逐字一致；本批次仅扩充论证，不改动定义语义。

## 9. 验证方式

```bash
# 1) YAML 语法自检（本目录 8 个提案文件）
python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob('proposals/ml-agent/*.yaml')];print('OK')"

# 2) 上游测试全绿（提案目录不在测试范围，回归不受影响）
python3 -m pytest tests/ -q
```
