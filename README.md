# prism-ontology

棱镜世界模型的共享语义契约与场景 Profile 工程。

prism-ontology 定义棱镜世界模型中可复用的概念、关系、约束和语义边界，并将它们编排为面向具体业务场景的 Operational Profile。

它负责回答“一个对象是什么、可以与什么发生关系、哪些概念不能混淆、一个场景允许读取和产生什么语义对象”，但不负责存储具体业务事实、执行洞察算法、生成业务动作或修改外部系统状态。

---

## 当前状态

项目目前处于早期 Release Candidate 阶段。

首个 Operational Profile：

- **Outlet Insight Profile** `0.1.0-rc2`
- **状态**：可用于受控集成（Release Candidate）
- **范围**：售点结构、空间关系、观测事实、指标口径、派生估计、洞察主张、质量限制及非执行边界

> **说明**：RC 状态不表示整个世界模型已经完成。本体将通过更多业务场景和跨 Profile 复用持续演化。

---

## 为什么需要它

当不同数据集、指标引擎、Agent 和业务系统使用相同词汇时，它们未必表达相同含义。

例如：

- **客户实体不等于客户在某次销售关系中的角色**（售点客观存在，未服务潜客尚未激活客户角色）；
- **行政区域不等于销售辖区**（国家法定行政区划与企业销售管理责任路线分立）；
- **实际拜访不等于拜访计划或打卡记录**（物理事件、前瞻性计划与 IT 打卡数据三权分立）；
- **数据观测不等于模型推算**（带来源/时间的经验观测与算法预测估计严格区分）；
- **洞察主张不等于已经写入世界状态的事实**（分析观点受证据约束，不自动回写世界模型）。

prism-ontology 通过统一标识、关系定义和机器可验证约束（SHACL），防止这些概念在跨系统协作中发生语义坍缩。

---

## 整体架构与定位

```text
Reference Ontology (L1/L2)
共享概念、关系和反坍缩原则
          │
          ▼
Operational Profiles (场景契约)
面向场景选择概念、指标和约束
          │
          ▼
数据映射 / 知识图谱 / 洞察组件 / Agent
引用并遵守 Profile 契约
```

- **Reference Ontology**：长期、跨场景的共享语义基石。
- **Operational Profile**：为具体业务场景裁剪出的可执行语义契约与度量集合。
- **Knowledge Graph**：符合本体约束的具体事实、实体和关系实例。
- **Application / Agent**：消费事实与语义契约，完成确定性查询、分析洞察或业务流程。

---

## 核心设计原则

### 1. 实体、角色与关系分离
一个现实对象可以承担业务角色，但角色不等于对象本身（如 `Outlet playsRole CustomerRole`，`CustomerAccount represents Outlet`）。

### 2. 计划、事件与记录分离
计划（`VisitPlan`）描述预期，事件（`ActualVisit`）描述客观发生，记录（`VisitRecord`）描述信息系统留下的打卡表示。

### 3. 观测与估计分离
`Observation` 表示来源可追溯的客观测量事实；`DerivedEstimate` 表示经过算法模型、规则或计算得到的估计值。

### 4. 主张与事实分离
`InsightClaim` 是基于数据证据形成的分析主张，不自动成为世界状态事实。

### 5. 行政空间与业务辖区分离
`AdministrativeRegion` 表示法定行政地理；`Territory` 表示企业组织管理或销售责任覆盖范围。

### 6. 本体不直接执行世界状态变更
本体可以描述动作与约束边界，但 Operational Profile 显式禁止组件生成 `Task`、`RoutePlan`、`ScheduleDecision`、`CRMStateMutation` 或 `WorldStateWriteCommand`。

---

## 分层架构与目录组织

```text
prism-ontology/
├── ontology/              # Reference Ontology (权威本体源文件)
│   ├── core/              # L1 通用元模型 (Entity, Role, Event, Observation 等)
│   ├── outlet/            # L2 售点领域本体 (Outlet, Brand, Region, Territory 等)
│   ├── insight/           # L2+ 洞察产物扩展 (AnalysisIntent, InsightClaim 等)
│   └── sales-visit/       # L2 销售拜访边界骨架 (CustomerAccount, ServiceRelationship 等)
├── profiles/              # Operational Profiles (场景运行契约编排)
│   └── outlet-insight/    # 售点洞察场景 Profile (concepts, relations, metrics, SHACL)
├── proposals/             # 需求提案及 6 态治理裁定记录
├── scripts/               # 构建、验证与确定性发行工具
├── tests/                 # 本体完整性、OWL-RL 推理与 Profile CQ 测试
├── dist/                  # 已构建的版本化发行物 (不可直接编辑)
├── GOVERNANCE.md          # 命名空间、提案状态机与治理规则
└── pyproject.toml         # 项目依赖与测试配置
```

> **注意**：`dist/` 是确定性构建产物，不是概念编辑入口；所有语义变更必须发生在 `ontology/`、`profiles/` 或 `proposals/` 源文件中。

---

## 当前 Operational Profiles

| Profile | 版本 | 状态 | 用途 |
|---|---:|---|---|
| **Outlet Insight** | `0.1.0-rc2` | Release Candidate | 售点结构、差异、异常、质量限制与分析洞察表达 |

Outlet Insight Profile 是本项目的第一个完整垂直切片。它用于验证 Reference Ontology、Profile 编排、SHACL 约束、确定性发行和下游语义契约消费的全链路。

---

## 快速开始

### 作为 Profile 消费端（如数据分析 Agent / 数据集成）

1. 选择目标 Operational Profile（如 `profiles/outlet-insight`）。
2. 读取上游发行包中的 `profile-manifest.json` 与 `checksums.sha256`。
3. 校验 Release Tag 与 Source Commit 的可追溯祖先关系。
4. 递归校验本地映射引用的所有 URI 是否属于 Profile 受管集合。
5. 将版本和各发行文件摘要写入本地锁文件（`profile.lock`）。

> **消费红线**：使用者不得直接依赖未发布的工作区文件，也不得仅通过 URI 前缀猜测概念存在。

### 作为本体贡献者

1. 在 `proposals/` 下提交概念提案，说明定义、适用范围、反例和复用场景。
2. 经治理委员会完成 6 态审查裁定（`accepted` / `profile_local` / `rejected` 等）。
3. 修改对应 Reference Ontology 或 Profile 源文件。
4. 编写正例图、反例约束及 Competency Question。
5. 运行 `pytest` 测试套件。
6. 从干净源码提交构建版本化发行包并打 Tag。

---

## 验证与测试

当前自动化测试覆盖：

- **RDF / Turtle 语法解析**：验证所有本体文件符合 W3C 标准语法。
- **OWL-RL 规则推理烟雾检查**：验证本体在演绎推理闭包下无逻辑矛盾与不可满足类。
- **SHACL 正向与负向约束**：精确断言 7 处核心概念坍缩与执行类违规被机器拦截。
- **Profile URI 注册闭包**：验证映射引用的概念、属性与度量 100% 存在于受管注册表。
- **Competency Question 行为级验证**：通过正例 RDF 事实图与 SPARQL 查询验证 10 条 Golden CQ 的语义可表达性。
- **发行文件完整性与版本溯源**：校验 SHA-256 校验和与 Git 提交祖先链条。

> **边界认知**：
> - OWL-RL 测试不等于完整的描述逻辑（DL）一致性证明；
> - CQ 可表达性不等于下游应用已经实现对应算法或界面；
> - Profile 发布不等于所有概念都已成为永久不可变更标准。

---

## 发布模型

每个 Profile 采用独立版本化发布。

一个有效发行包（`dist/<profile>/<version>/`）必须包含：

- `profile-manifest.json`（元数据清单与 Git 提交信息）
- `outlet-insight.owl.ttl`（合并后的 OWL 本体图）
- `outlet-insight.shacl.ttl`（合并后的 SHACL 形状图）
- `concepts.yaml` 与 `relations.yaml`（受管概念与关系清单）
- `metric-definitions.yaml`（受管度量定义与语义前提）
- `sources.yaml` 与 `organizations.yaml`（数据源与组织实例）
- `competency-questions.yaml` 与 `competency-question-report.md`（能力验证报告）
- `checksums.sha256`（发行文件哈希清单）

**发布链路规范**：
$$\text{Source Commit} \longrightarrow \text{Distribution Commit} \longrightarrow \text{Annotated Release Tag}$$

---

## 非目标 (Non-Goals)

prism-ontology 明确不负责：

- 存储具体网点、客户或拜访事实实例；
- 替代物理数据库 Schema 或企业数据目录；
- 替代实时查询与图数据库知识图谱；
- 执行指标数值计算和洞察合成算法；
- 生成销售路线、拜访排程或派单指令；
- 接收或执行 CRM 状态变更命令；
- 因某个外部数据表存在某列就无条件创建全局本体概念；
- 专门为大模型提供提示词词典（LLM 可以消费本体，但不是本体存在的前提）。

---

## TopPrism status

| Field | Value |
|---|---|
| Purpose | Business World Model · Semantic Contract |
| Maturity | Early Release Candidate |
| Evidence | RDF/OWL-RL/SHACL、Competency Questions、Profile URI 闭包与发行完整性测试 |
| Boundary | 不代表完整世界模型；不存储业务事实、不执行洞察算法、不生成或执行业务动作 |
| Related | Operational Profiles and downstream semantic consumers |

---

## 治理与贡献入口

新增或修改概念前，请先阅读：

- [`GOVERNANCE.md`](GOVERNANCE.md)：治理原则、命名空间、6 态提案状态机与发布规则。
- `proposals/`：下游需求证据与历史裁定记录。
- `profiles/outlet-insight/`：售点洞察场景边界与约束。

涉及以下重大变更时必须进行治理评审：
1. 修改既有 URI 的核心定义；
2. 变更类之间的继承结构或互斥关系；
3. 变更受管度量的统计计算口径；
4. 将 Profile-local 局部概念提升为全局 Reference Ontology；
5. 引入可能产生世界状态写入效果的概念。
