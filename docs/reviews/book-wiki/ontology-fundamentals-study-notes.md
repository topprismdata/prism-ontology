# 本体构建基础知识学习笔记（评审前补课）

日期：2026-09-06 ｜ 用途：升级 prism-ontology 评审的方法论依据
状态：在线验证 7 个权威源；Methontology/NeOn 引自标准文献（Gómez-Pérez et al. 2004；Suárez-Figueroa et al. 2012），标注为文献引用而非即时抓取。

## 1. 方法论版图

| 方法 | 核心 | 对本项目的适用点 |
|---|---|---|
| TOVE (Grüninger & Fox 1995) | 能力问题（CQ）驱动：先写 CQ，再形式化为公理，本体"够用"由 CQ 通过定义 | prism-ontology 的行为级 CQ 测试是**教科书级正确**；但 CQ 未随类扩展而更新（新增 SalesRep/Route 后没有对应新 CQ） |
| Methontology (Gómez-Pérez et al.) | 生命周期五阶段：specification → conceptualization → formalization → implementation → maintenance；三类文档（支持/技术/用户） | 项目有 specification（GOVERNANCE/README）与 implementation，**conceptualization 文档缺失**（没有概念化记录：为什么 Territory ⊑ Entity，决策依据在哪）；maintenance 意识好（6态状态机） |
| NeOn (Suárez-Figueroa et al. 2012) | 场景化协作：9 个场景（重用/重构/模块化/CQ 驱动/版本迁移/NLP 抽取…）；治理网络 | 版本迁移场景正是 rc2 原地重生成事故踩掉的坑（issue #10） |
| OntoClean (Guarino & Welty 2002) | 用元性质（刚性 rigidity、身份 identity、统一性 unity、依赖 dependence）清洗分类学 | Role 无依赖公理、ChannelType 的身份准则、Territory 的类别错置——之前已指出，现在有了方法论名分 |

## 2. 形式本体论（上层本体）要点

- **BFO (ISO/IEC 21838-2)**：continuant（持续体：对象/角色/性质/处置）vs occurrent（发生体：过程/事件/边界）二分；角色（role）是**具体依赖连续体**（specifically dependent continuant），必须依赖承载者存在。BFO 是 ISO 认可的顶级本体，OBO 生态的地基。
  - 对应评审：prism-core 的 Entity/Role/Event/Activity 大致映到 continuant/occurrent，但**未声明依赖公理**——Role 可以孤立存在（无 bearer 强制），OOPS P10/P11 的组合体现。
- **UFO (Guizzardi)**：Role 是 **anti-rigid + externally dependent** 的 sortal（必须由外部关系激活）；**relator 模式**：两个 endurant 之间的关系应建为连接二者的个体（如 ServiceRelationship 应是 relator，同时连接 Organization 与 Outlet）。UFO 会要求 ServiceRelationship 有**两端参与者公理**——本体只有 hasServiceProvider（domain 唯一、无 range），缺网点端与组织端 range。
- **DOLCE (Masolo et al. 2003)**：endurant/perdurant/quality/abstract 四分；"服务关系"在 DOLCE 视角下更接近 stative（状态性）而非 activity——`ServiceRelationship ⊑ Activity` 是把状态建成过程的范畴错置。

## 3. W3C 规范细节（本次验证的关键收获）

### SKOS Primer（已细读）
- `subClassOf skos:Concept` **合法**（Primer 4.7 明确允许特化扩展）——作者对 #4 的修法方向没错；
- 但**规范用法要求配套**：`skos:inScheme` 挂入 ConceptScheme、`hasTopConcept` 声明顶层、`prefLabel` 每语言唯一、`altLabel` 管同义词、`skos:note`/`definition` 管文档——prism-ontology 只做了 subClassOf，**ConceptScheme/inScheme/altLabel 全缺**，导致 crosswalk 手工重复造 SKOS 已标准化的同义词机制；
- Primer 警告：`owl:imports` 一个 KOS 会把 ConceptScheme 实例推成 owl:Ontology（落 OWL Full）——引用 SKOS 方案时要小心。

### OWL 2 Primer（已细读相关节）
- **DisjointClasses**：开放世界下不相交性不会自动成立，必须显式声明；"By omitting disjointness statements, many potentially useful consequences can get lost"——本项目 0 条 `owl:disjointWith`，全部互斥只在 SHACL 层，OWL 导入方完全感知不到；
- **domain/range 是推理规则不是约束**（"not a constraint on the knowledge, but allows a reasoner to infer further knowledge"）——`hasAge 9` 反推出 Felix∈Person 的经典陷阱；本项目大量 domain-only 属性（hasSource、hasIdentifier、hasServiceProvider、derivedFrom、validDuring）会让 reasoner 做无意义推断；
- **Punning**：OWL 2 DL 允许同一 IRI 既作类又作个体，但两种视图语义独立——本项目未用到，无风险。

### SHACL / SOSA / PROV-O（此前已验证）
- 观测模式对齐缺口（observedProperty/hasResult/resultTime 缺失）此前已报告，本次补充：core.shacl.ttl 强制的 `prism-core:observedValue` 在 TTL 中**根本未定义**（幽灵属性），真正的 hasResultValue 未被任何 shape 引用。

## 4. OOPS! 陷阱命中清单（对 prism-ontology）

| 陷阱 | 严重度 | 命中证据 |
|---|---|---|
| **P11 缺 domain/range** | Important | hasSource（无 range）、hasIdentifier（无 range）、hasServiceProvider（无 range）、derivedFrom（无 range）、validDuring（无 domain） |
| **P10 缺 disjointness** | Important | 全库 0 条 owl:disjointWith |
| **P08 缺标注** | Minor | field-mapping.yaml 44 项映射关系全部无定义/标注（在 YAML 层，不在 TTL） |
| P20 标注误用 | Minor | 全部定义塞在 rdfs:comment，未区分 skos:definition/IAO:definition 与一般注释 |
| P22 命名不一致 | Minor | `Ctrip_星级`（下划线+中文）vs `CtripStarRating`（CamelCase）混用；中文列名直接作 URI 段 |
| 未命中 | — | 无循环层级（P06）、无自造 is（P03）、无错误等价（P31）；SHACL 负向测试覆盖了坍缩反例（好于平均） |

## 5. OBO Foundry 原则对照（机器可检部分）

| FP | 要求 | prism-ontology 现状 |
|---|---|---|
| FP3 命名空间 | 唯一持久 URI（PURL/HTTP 形态） | ❌ `prism://` 自造 scheme 不可解引用；且运行时新增 `prism:lifecycle:` 前缀未在 GOVERNANCE 注册 |
| FP4 版本化 | 版本必须标记、存储、正式发布（version IRI） | ❌ 全模块 owl:versionInfo 恒为 "0.1.0-rc1"，无 owl:versionIRI；dist rc2 被原地重生成（issue #10） |
| FP6 文本定义 | 多数类必须有定义 | ⚠️ TTL 层定义覆盖率高（好）；注册表层（field-mapping）零定义 |
| FP7 关系复用 | 复用既有关系（RO） | ⚠️ 声称对齐 SOSA/PROV-O 但实际自造 hasSource/observedAt/hasResultValue 平行词表 |
| FP1/FP2 开放+通用格式 | ✅ MIT + Turtle | 通过 |
| FP5 范围 | ⚠️ README 写了非目标（好），但概念膨胀仍现（16 个 L1 类多数无下游使用） | 部分 |

## 6. 对评审报告的增量修正

1. 之前说"Territory 改挂 Entity 是对的"——UFO 视角下更准确的说法：Territory 应建为 **relator 连接组织与空间**，或 Organization 的子类+覆盖几何分离，现在只是把类挪了个父类，依赖与参与者公理仍缺。
2. 之前把"SHACL 只此一层"当作轻微问题——OntoClean/OWL 2 Primer 依据下升级：**缺 disjointness 是 Important 级陷阱**（P10），且让反坍缩约束对纯 OWL 消费方不可见。
3. SKOS 修法（#4）方向正确但只完成 20%——按 Primer 规范应补 ConceptScheme/inScheme/altLabel，用 SKOS 映射属性（closeMatch/exactMatch）替代手工 crosswalk。
4. 新增可自动化建议：直接采用 OBO Dashboard 式自动检查（FP3 前缀唯一、FP4 versionIRI、FP6 定义覆盖率、P11 domain/range 完整性）——这些都有现成开源实现可抄。
