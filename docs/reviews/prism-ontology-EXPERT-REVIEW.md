# prism-ontology 专家级严格评审
**视角**：本体工程方法 + 企业语义层（Palantir Foundry Ontology）实践 + 销售管理领域权威文献
**依据**：21 份销售管理权威文献（LLM wiki，book-wiki/）+ 7 个在线验证的本体工程权威源 + 代码级证据（HEAD f133c7c）
**方法**：每个设计点 ≥3 个独立权威 → 结论 → 评分。引用格式：`[key p.N]` 指向 book-wiki（可按换页符回溯），[源] 指向在线规范。

## 总判决

**这个项目把"本体治理的仪式"建得很全，但把"销售管理领域的本体"建得很薄，且在形式层有系统性缺陷。**
一句话：**治理 A、仪式 A、领域覆盖 D+、形式语义 C-。** 它当前是一个"售点宽表的分析语义皮 + 完备的治理剧场"，以"销售管理世界模型"自我定位（README: Business World Model）严重名不副实。

| # | 评审维度 | 得分 | 一句话判决 |
|---|---|---|---|
| 1 | 定位与范围诚实度 | 3/10 | 自称世界模型，实测是单场景分析契约 |
| 2 | 上层本体与分类学 | 4/10 | 无形式根基，互斥只在 SHACL |
| 3 | 观测与证据模式 | 3.5/10 | 对齐 SOSA 是口号；shape 校验幽灵属性 |
| 4 | 度量口径工程 | 5/10 | 有边界意识，无 Farris 式口径纪律 |
| 5 | 客户/账户/角色 | 6/10 | 骨架对（GS1 同构），深度浅 |
| 6 | 辖区/线路/PJP | 5/10 | 类齐了，灵魂（workload/potential）没进去 |
| 7 | 执行与闭环 | 2/10 | 禁写回切断了 Palantir 意义上的"运营本体" |
| 8 | 治理/版本化/发布 | 4/10 | 仪式完备，兑现失败（rc2 事故） |
| 9 | 领域覆盖（对 13 章教科书） | 2/10 | 覆盖 Johnston 13 章中的 3.5 章 |
| 10 | 可验证性与测试 | 8/10 | 行为级 CQ+负向 SHACL，全行业少有 |

---

## 1. 定位与范围：自称世界模型，实测 3.5/13 章

**证据**：Johnston & Marshall《Sales Force Management》13 章是领域分类学 [johnston-sf-management-12e p.8-10 目录]：销售过程(2)、CRM 与客户策略(3)、组织(4)、信息与 SFA(5)、绩效行为(6)、激励(7)、个人特征(8)、招聘(9)、培训(10)、薪酬(11)、成本分析(12)、绩效评估(13)、预测(附录)。JPSSM 的 SFE 框架把这些组织成"环境→战略→设计→活动→绩效"因果链 [jpssm2008-sfe-framework p.1]。
**判决**：prism-ontology 的概念最多映射 Ch2-5 的一部分（买卖角色、组织、SFA 信息层）——**9.5 个章的领域空间完全没有概念承载**（配额、薪酬、激励、成本、评估、招聘、培训、预测、渠道成员）。Palantir 顾问视角：Foundry Ontology 的价值主张是"绑定企业实际运行的对象/链接/动作"[Palantir Action Types 文档]；一个不覆盖企业实际业务动作域的"世界模型"在客户现场撑不起语义层。README 的 Boundary 字段倒是诚实（"不代表完整世界模型"）——但 top 定位字段仍是 "Business World Model · Semantic Contract"，这属于**系统性过度承诺**。
**要求**：要么改名为 Outlet Insight Semantic Contract，要么补齐领域路线图（已有 2 个 draft 提案，远远不够——按 Johnston 目录至少还需要 quota/compensation/performance/forecast/channel-member 五个领域包）。

## 2. 上层本体与分类学：无形式根基 + 互斥不可见

**证据**：
- BFO/ISO 21838-2 要求角色（role）作为具体依赖连续体必须声明对承载者的依赖；UFO（Guizzardi）要求 Role 是 anti-rigid + externally dependent 的 sortal，关系用 relator 模式（连接两端参与者）[OBO/BFO 源]。
- OWL 2 Primer（已核验原文）："By omitting disjointness statements, many potentially useful consequences can get lost."——本项目 `grep disjointWith ontology/` = **0 条**。
- OOPS P10（Missing disjointness, Important）+ P11（Missing domain/range, Important）双命中：hasSource/hasIdentifier/hasServiceProvider/derivedFrom 缺 range，validDuring 缺 domain。
**判决**：
1. 反坍缩是全项目的灵魂卖点（README 五组区分），但它的全部实现是 5 个 SHACL 文件——**一个只用 OWL 的消费方（任何标准三元组库导入者）看到的本体允许"行政区=辖区"**。互斥应双轨：`owl:disjointWith`（语义层，可推理）+ SHACL（数据验证层），两层交叉引用。
2. `ServiceRelationship ⊑ Activity` 无 relator 两端公理（UFO 违例）：hasServiceProvider 无 range、无网点端属性——"关系"连参与者都表达不全。
3. `ChannelType/VisitPurpose/VisitMode ⊑ skos:Concept` 方向合法（SKOS Primer 4.7 允许特化），但**只做了 20%**：无 ConceptScheme、无 inScheme、无 altLabel——crosswalk 在手工重建 SKOS 已标准化的同义词/映射机制（应改用 skos:altLabel + skos:closeMatch/exactMatch）[SKOS Primer 已核验]。
4. OntoClean 视角：Territory 改挂 Entity 只是挪了父类；既非纯几何（丢了 covers 语义的量化）、也非组织单元（无负责人/目标/生命周期），身份准则（identity criterion）依然悬空。

## 3. 观测与证据模式：口号对齐，实现脱轨

**证据**：SOSA/SSN 的 Observation 三件套 hasFeatureOfInterest + observedProperty + hasResult(+unit) + resultTime 是 W3C/OGC 双标准 [vocab-ssn；ISO 19156]；多指标观测用 ssn-ext ObservationCollection。prism-core 现状：observedAt/hasSource/hasResultValue 已加（issue #2 修复），但——
1. **core.shacl.ttl 强制 `prism-core:observedValue`，该属性在全部 TTL 中不存在**（grep 实锤）；新定义的 hasResultValue 反而没有任何 shape 引用。负向测试通过仅仅因为测试数据自己用了这个幽灵属性——**约束层与词表层互相脱节，测试给了假信心**。
2. 没有 SHACL 强制 observedAt/hasSource 必填——类注释"必须携带来源与时间"依旧没有兑现机制。
3. 指标值仍是谓词直挂（test fixture `<prism://ontology/metric/WeekendTraffic> 1200`）：无单位（QUDT/OM 缺席）、无样本量、无时间，SHACL 无法封顶一个观测可携带哪些指标。
**判决 3.5/10**：对标 SOSA 的最小完整契约（featureOfInterest/observedProperty/result/resultTime/source）只完成了 value 一半。业务后果在 multi-source 场景（点评/携程/高德更新周期不同）无解。

## 4. 度量口径工程：有边界意识，无纪律

**证据**：Farris《Marketing Metrics》给每个指标四件套——定义、公式、**数据来源、陷阱/注意事项**（全书体例）[farris-marketing-metrics-2e p.18-25]；份额分解链（penetration share / share of requirements / heavy usage index）展示了"口径可组合"的正确姿势。
**对照**：
- 好的一面：HHI 用网点数份额并在 interpretation_boundary 里写死"非销售额份额、严禁反垄断推断"——符合 DOJ/USDA 对 footprint 集中度与收入集中度分列的最佳实践 [zoltners1983 之外的 HHI 文献链]；missing_value_policy 全局统一（null 不填补+报缺失率）。
- 差的一面：38 项指标的 formula 是不可执行的散文；numerator/denominator 大量占位（"N/A"、字面 "5"）；interpretation_boundary 多为"源自字段X"同义反复；**ActualSalesCrates 的 data_source 与 physical_column 曾为 null/「None」**（已修但暴露生成未复审）；SOCI/SOVI 引用 INE 执行标准作口径权威的能力为零（本体不知道 INE 存在）[ine-omnichannel-cn p.2]。
**判决 5/10**：按 Farris 体例逐指标补"数据源实体 + 已知陷阱 + 与其他指标的分解关系"，是 1.0.0 的硬门槛。

## 5. 客户/账户/角色：骨架对，深度浅（6/10）

**支持**：Outlet/CustomerAccount/CustomerRole 三分与 GS1 party–location–function 完全同构 [GS1 GLN Data Model]；"未服务网点未激活角色"注释有 UFO anti-rigid 意识。
**缺口**：
- Kotler 七角色采购中心（initiator/user/influencer/decider/approver/buyer/gatekeeper）[kotler p.109/122] 与 Johnston 的 Selling Center [johnston p.58] 表明**角色必须成族、按情境激活**——本体只有 CustomerRole 一个角色类，无角色类型受管词表，无"角色由 ServiceRelationship 激活"公理。
- Woodburn SAM 手册：大客户有 status 层级、账户团队、客户计划产物 [woodburn-sam-handbook p.317-337, p.398]——CustomerAccount 是平面的，无分级、无团队、无计划。
- Palantir 视角：Foundry 的 Customer 360 型对象本来就是"account + contacts + roles + hierarchy"打包；这里的账户模型离可用还差 hierarchy 一整层。

## 6. 辖区/线路/PJP：类齐了，灵魂没进去（5/10）

**权威定义**：Zoltners & Sinha 1983（Management Science）：辖区对齐=把账户分配到辖区，**平衡 workload 与 opportunity**，模型化目标与求解 30 年未变 [zoltners1983 p.3-7]；三十周年复盘强调公平性→士气→绩效链 [sales-territory-design-chapter p.4-6]；Darmon 2002 把**信息完备度**连进最优辖区/规模 [darmon2002 p.6-8]；EJOR 2014 把部署形式化为"市场×段×响应函数" [ejor2014 p.3]；农村 PJP 白皮书给出 Route=日服务网点序列+服务频次的业务粒度 [brandidea-pjp-rural p.3-7]；Salesforce 把账户级分配规则（AccountTerritoryAssignmentRule）作为辖区模型的核心对象 [Salesforce TM2 文档]。
**判决**：issue #5 修复后类是齐的（SalesRep/Route/assignedTo/onRoute/coversOutlet/cadence），但——
1. **Territory 没有任何 workload/potential/账户数属性**——Zoltners 意义上的辖区语义（平衡单元）在类定义里不存在，只在注释里提了"责任空间"；
2. `cadence` 是 xsd:string 自由文本（"每周一次 F1"）——不可计算、不可验证；业界标准是 ISO 8601-2 recurrence/iCalendar RRULE 或受控频次枚举；
3. coversOutlet 挂在 VisitPlan 上而不是 Route 上（Route 注释说"承载网点序列"却没有 coversOutlet 属性）——计划与线路的覆盖语义打架；
4. 账户级分配关系（account assignment）缺失，而那才是 1983 模型的原子操作。

## 7. 执行与闭环：语义层自我阉割（2/10）

**证据**：Palantir Foundry 的核心主张：Ontology = Object Types + Link Types + **Action Types**（"define a set of changes or edits…including side effects"）——写回是治理对象而非禁忌 [Palantir Action Types 文档]；Salesforce 同样把 Flow/审批作为平台一环。INE（可口可乐店内执行标准）的整个目的就是"统一执行标准、发现增长机会" [ine-omnichannel-cn p.2]——执行是可口可乐系统语义的一部分。Johnston：SFA 的意义在把行为数据变成可分析资产 [johnston p.114]。
**判决**：prism-ontology 禁止 Task/RoutePlan/ScheduleDecision/CRMStateMutation/WorldStateWriteCommand（SHACL 精确拦截），ElevationCandidate 强制 unreviewed 且无受控提升流。结果是：**"洞察→决策→行动→新观测"的运营闭环被逐出语义契约**，只能在契约外用代码和表格实现——Palantir 顾问的一句话判决：你们把 Ontology 里最值钱的第三件东西（Action）划给了别人，然后指望语义层管住别人。**正确姿势**：把 Action Types 建成受管概念（governed write intents：审批状态、前置校验、可回写字段白名单），而不是建"禁止概念"清单。五组反坍缩区分里"主张≠事实"是对的，但推论应是"主张→受控提升→事实"，不是"主张永不落地"。

## 8. 治理/版本化/发布：仪式完备，兑现失败（4/10）

**证据**：OBO Foundry FP3（唯一持久 URI）与 FP4（版本必须标记/存储/正式发布）是行业机器可检标准；W3C OWL 2 用 owl:versionIRI 做版本绑定；NeOn 方法论把版本迁移列为独立场景。实测：`prism://` 自造 scheme 不可解引用（无 HTTP、无 content negotiation、owl:imports 全部悬空）；全部模块 versionInfo 恒为 "0.1.0-rc1"；**rc2 发行包被原地重生成、tag 溯源断裂、manifest 记录的源提交与内容不符（clean_working_tree: true 为假）**（issue #10 实锤）；运行时新增 `prism:lifecycle:` 前缀未在 GOVERNANCE 注册。
**判决**：6 态状态机、五问法、checksums、确定性构建——文档和工具都是真的，但**治理者自己第一个违反了治理**。这比没有治理更糟：它给下游"已经治理过"的错觉。

## 9. 领域覆盖：对 13 章教科书的 D+（2/10）

以 Johnston 13 章为尺：Ch2 部分✓（买卖角色）、Ch3 部分✓（客户/CRM 语境）、Ch4 部分✓（组织骨架）、Ch5 部分✓（信息/SFA 语境）；Ch6-13（绩效行为、激励、特质、招聘、培训、薪酬、成本、评估）**0 概念**，预测 0 概念，渠道成员 0 概念，配额 0 概念。Palantir 顾问结论：这不是"早期阶段"，这是**定位错误**——按现有路径（每个场景一个 Profile）再走 5 个场景也补不齐领域骨架，需要一个跨场景的"销售领域核心包"（quota/compensation/performance/forecast/channel-member/account-hierarchy），且这正是 GOVERNANCE 五问法能通过的稳定概念。

## 10. 可验证性：全行业少有的亮点（8/10）

Grüninger & Fox 的 CQ 方法论要求"本体够用=CQ 通过"[TOVE；CQ survey 2023]；本项目是少数做到**行为级 CQ**（真实 RDF 事实图+SPARQL 断言）、SHACL 负向注入测试、SHA-256 校验和与确定性构建的工程本体。OBO Dashboard 式的机器可检原则（FP3/FP4/FP6/P11）有现成开源模式可抄，建议直接移植——把"治理"从委员会文档变成 CI 门禁，是本项目从 A- 仪式走向 A 治理的唯一路径。

---

## 最终评分：5.2/10

**最强资产**：反坍缩的问题意识（业务真痛点）、行为级测试文化、可口可乐系词汇接地（NARTD/PJP/INE/DSD）。
**最致命三伤**：① 领域覆盖与"世界模型"自我定位的鸿沟；② 运营闭环（Action）被禁令逐出契约；③ 形式语义层（互斥/依赖/domain-range/单位/时间）系统性欠账，且 SHACL 校验幽灵属性暴露"测试全绿≠质量合格"。

## 给作者的十条（按 ROI 排序）

1. **改名或扩域**：把 README 定位改为 "Outlet Insight Semantic Contract"，或立项"销售领域核心包"（quota/performance/forecast/channel-member/account-hierarchy 五提案）。
2. **互斥双轨**：全部反坍缩约束补 `owl:disjointWith` + SHACL，两层互引。
3. **补齐 P11**：5 个缺 domain/range 的属性一次修完；domain/range 按 OWL 2"推理规则"语义审查误用。
4. **观测契约对齐 SOSA 最小集**：observedProperty+hasResult(带 unit，走 QUDT)+resultTime+source 必填 SHACL；修 observedValue 幽灵属性；多指标观测用 ObservationCollection 模式。
5. **Territory 注入灵魂**：workload/potential/accountAssignment 进类定义（引用 Zoltners 1983 模型语义），cadence 改 ISO 8601-2/RRULE 或受控枚举，coversOutlet 移到 Route。
6. **受控 Action 概念**：把"禁写回"升级为"governed write intents"（审批流+字段白名单），参考 Palantir Action Types 的治理模型。
7. **度量口径照 Farris 体例**：每指标补数据源实体+陷阱+指标间分解关系；SOCI/SOVI 口径锚定 INE 标准。
8. **URI/版本合规**：`prism://` 换 `https://ontology.topprism.ai/` 形态（PURL 策略），每模块加 owl:versionIRI，GOVERNANCE 注册 lifecycle 前缀。
9. **治理 CI 化**：把 FP3/FP4/FP6/P11/P10 检查做成 pytest（OBO Dashboard 模式），发行链的 clean_working_tree 造假问题用"两段式提交"根除。
10. **SKOS 补课**：ChannelType 等建 ConceptScheme/inScheme，crosswalk 迁移到 skos:altLabel+exactMatch。

---
**评审材料**：book-wiki/（21 卡片 + 12 概念页 + 本体基础笔记）全部可回溯；前序报告：DEEPDIVE、BUSINESS-REVIEW、issue #1-#10。
