# prism-ontology 业务质量评审（基于论文与行业标准比对）

日期：2026-09-06 ｜ 评审方式：通读全部本体源文件/Profile 注册表/提案记录 + 外部文献基准比对

## 总评

**概念骨架是业务上正确的，治理机制是行业少见的，但"语义纯度"和"观测模式"两处有硬伤。**
一句话：骨架 A、组织 A、语义纯度 C、模式对齐 C。当前状态适合做内部世界模型的骨架，但按它自己的发行标准（rc → 1.0.0），还不具备作为"语义契约"对外交付给消费端的质量。

业务综合评分：**6 / 10**

| 维度 | 得分 | 依据 |
|---|---|---|
| 概念骨架正确性 | 8/10 | 五组反坍缩区分直击 FMCG 数据真痛点；行业术语接地真实 |
| 业务覆盖完整性 | 5/10 | 无 Product/时间/人员维度；洞察半边腿 |
| 语义层-数据层分离 | 4/10 | 裸物理列直通进注册表，违背自身治理红线 |
| W3C/行业标准模式对齐 | 4/10 | 声称对齐 SOSA/PROV-O 但缺核心部件 |
| 度量口径严谨性 | 6.5/10 | HHI 边界声明符合最佳实践；部分口径流于表格化 |
| 治理与验证机制 | 8.5/10 | 行为级 CQ、反例回归测试、确定性发行、6 态状态机 |

---

## 一、做对了什么（业务视角）

### 1. 五组反坍缩区分 = FMCG 路线到市场（Route-to-Market）数据的真实痛点
本体拒绝合并的五对概念，每一对都对应快消行业真实的数据事故模式：

- **网点(Outlet) ≠ 客户账户(CustomerAccount) ≠ 客户角色(CustomerRole)**：这正是 GS1 GLN Data Model 的 party–location–function(role) 三分离原则（GS1 标准页：GLN 可标识法律实体、物理位置、数字位置与功能角色）。CRM 里一个客户主数据对应多个物理网点、或一个网点挂多个账户，是售点主数据去重领域最经典的问题。建模方向与 GS1 一致，是对的。
- **行政区划 ≠ 销售辖区**：行政编码与销售责任区双轨、只建 covers 关联不建等同——这防止了"按区县汇总销售"与"按辖区考核"互相污染，是快消行业熟知的大区/办事处/线路体系与民政区划不重合问题。
- **计划(PJP) ≠ 实际拜访 ≠ 打卡记录**：PJP（Permanent Journey Plan，永久性拜访线路计划，快消/可口可乐系统标准术语）、ActualVisit（物理进店事件）、VisitRecord（SFA 打卡 GPS+照片）三分。SFA 打卡数据与真实拜访的偏差（代打卡、店外打卡）是零售执行稽核的核心议题，三者分离才能表达"打卡率 100% 但真实拜访存疑"这类业务判断。
- **观测 ≠ 估计**：DianpingRating 是观测，RevenuePotential* 是 DerivedEstimate，禁止互混——这是防止"模型预测值回写为事实"的关键闸门。
- **主张 ≠ 事实**：InsightClaim 不自动回写世界状态 + ElevationCandidate 强制 unreviewed——对应分析结果治理的 human-in-the-loop 原则。

### 2. 行业术语接地是真实的，不是编的
指标与字段词汇（NARTD 排面数、冰柜门数、SOVI/SOCI 排面占比、PJP、RED、太古乡镇、红镇、赶集日、NIQ-NARTD 指数、LINX MT 黄金门店）指向明确的行业口径：
- **NARTD**（Non-Alcoholic Ready-To-Drink）是可口可乐系统定义总市场的标准术语，用于其财报份额基准（可口可乐财报原话："公司在非即饮非酒精饮料（NARTD）总量中的价值份额…"）；NIQ（NielsenIQ）零售普查/NARTD 指数是装瓶商体系的标准市场计量。
- 太古乡镇/红镇/赶集日 → 太古可口可乐中国区乡镇市场路线批发口径。
- 结论：数据源是一个可口可乐系装瓶商的售点宇宙（outlet universe）宽表 + 点评/携程/高德/人口网格增补。本体作者懂这个行业，词汇表不是拍脑袋。

### 3. HHI 边界声明符合测量方法论最佳实践
用**网点数份额**而非销售额份额计算 HHI/CR4/CR8。学术/官方口径上 HHI 标准定义在收入份额上（DOJ/FTC），网点数 HHI 是常见的 footprint 代理，已知偏差是低估大店、高估小店连锁；USDA/Census 研究还表明零售集中度对**地理边界选择**极其敏感。本体的 `interpretation_boundary` 明确写了"网点物理覆盖集中度，非实际销售金额市场份额；严禁推断反垄断法意义上的垄断"——这正是"footprint 集中度与收入集中度分列、明示代理性质"的最佳实践。扣分点：`spatial_scope` 是自由文本"指定区域"，而市场边界恰是零售集中度测量最大的误差源，应该用受管区域实例。

### 4. 拒答设计诚实
CQ-008（可口可乐 vs 百事真实销量份额）显式声明 missing_concept 并拒答，而不是让模型编数。CQ-007 的 partial + 降级置信度同理。这比大多数"什么都答"的 BI 语义层更符合负责任 AI 的口径管理。

---

## 二、硬伤（业务后果导向）

### 1.【最严重】语义层被数据字典污染，违背自身治理红线
`relations.yaml` 54 个注册项里约 40% 是裸物理列直通：`prism:observed/是否红镇，默认否`、`prism:observed/太古乡镇`、`prism:observed/大众点评-必吃和黑珍珠` 等。URI 里带"默认否"（默认值说明）、"200米/400米"（参数化变体）这类**数据清洗痕迹**；这些项没有 domain/range、没有定义、没有外部对齐——它们不是本体概念，是列别名。

而 README"非目标"第 7 条白纸黑字：*"因某个外部数据表存在某列就无条件创建全局本体概念"* 是本项目明确不做的事。GOVERNANCE 五问法第 1 问"对象是否客观稳定"也过不了"是否红镇，默认否"。**治理机制和实际产出打架了。** 业务后果：下游 agent 拿到的是一个伪装成本体的宽表字段清单，"防止语义坍缩"只防住了 TTL 里的 7 个反例，没防住注册表里 35 个直通列。

### 2. 观测模型声称对齐 SOSA/SSN，但缺关键部件
core.ttl 注释说 Observation"必须携带来源与时间"，但：
- 本体中**没有任何属性**表达观测时间（sosa:resultTime / phenomenonTime）和来源（wasAttributedTo / usedProcedure / madeBySensor）；prov:Activity 只被 import 没被用上。
- 指标值以"谓词直挂"方式表达（CQ fixture：`<urn:obs:...> <prism://ontology/metric/WeekendTraffic> 1200`）——predicate-per-metric 反模式。单位、时间戳、置信度、样本量无处安放；SHACL 也无法约束"一个 OutletObservation 可以携带哪些指标"（谓词是开放集合）。
- W3C SSN/SOSA 标准模式是：Observation 通过 hasFeatureOfInterest 指向对象、observedProperty 指向被观测属性、hasResult 携带带单位的值、resultTime 记录时间，溯源走 PROV-O 映射（Compton et al. 的 SSN+PROV-O 组合是公认实践）。

业务后果：这是"售点洞察"场景的**核心质量缺口**——点评评分、携程评分、高德客流来自三个更新周期不同的源，多源冲突时（点评说营业、高德说停业）没有时间与来源就无法裁决新鲜度与可信度，"洞察主张基于证据"（groundedInEvidence）也无从落地，因为 Evidence 类同样没有任何属性。

### 3. 注册表之间互相漂移，闭包测试没兜住
- crosswalk 引用**不存在的属性**：`prism:outlet/locatedInRegion`、`prism:outlet/belongsToTerritory`（本体里是 locatedInAdministrativeRegion / coveredBySalesTerritory）；引用**不存在的度量**：`prism:metric/RoomCount`、`prism:metric/RevenuePotential`。
- concepts.yaml 注册了 **TTL 里从未定义的类**：TownshipContext、DemographicObservation、AssetAndDisplayObservation、CompetitorSalesVolume、EntityResolutionAssessment、MatchPairAssessment、DataEngineeringContext 等 7 个。
- CQ-007 的 formal_expression 引用 `prism:metric/Ctrip_星级`，但该 URI 只存在于 observed 直通列，不是受管度量。
- 测试只校验"URI 是否在 YAML 注册表成员里"，不校验"URI 是否真的在 TTL 中有定义"——所以 100% closure 全绿是假阴性。
- ActualSalesCrates 度量的 physical_column/data_source 为 null，interpretation_boundary 里出现字面量「None」——自动生成未复审的痕迹。

业务后果：下游按 README 的消费路径（读 manifest → 校验 URI 受管集合 → 写 profile.lock）接入，会踩到悬空引用；rc 阶段靠人肉弥补，1.0.0 必炸。

### 4. 业务覆盖偏窄（部分有自知之明，部分没有）
- **无 Product/SKU/品类维度**：只有 Brand。SOVI/SOCI（份额排面）其实隐含了品类/包装，但本体无法表达"什么产品的排面"。作为售点结构洞察可以接受，作为"洞察"底座偏窄。
- **无时间语义**：38 个指标 temporal_scope 全是"当前快照周期"，无历史、无趋势表达；无 bitemporal（业务时间 vs 系统时间）——而拜访/打卡场景天然需要双时间轴（他们自己把 Plan/Event/Record 分开了，却没有时间属性去承载）。
- **拜访骨架撑不起"拜访洞察"**：有 VisitPlan/ActualVisit/VisitRecord 类，但没有 SalesRep/Person、没有线路(Route/Line)、没有 VisitPlan 的 assignedTo/scheduledDate、没有拜访频次标准与覆盖率度量（PJP 达成率是快消一线最核心的 KPI）。骨架比空缺少，但离可用差一层。
- ServiceRelationship 注释说"特定销售组织与售点之间"，却**没有指向组织端的属性**（只有 accountRealizesRole/outletPlaysCustomerRole），关系的参与者建模不完整。

### 5. OntoClean 视角的分类学问题（轻）
- ChannelType ⊑ InformationObject、VisitPurpose/VisitMode ⊑ InformationObject：业态/目的/模式是**类别**（行业惯例用 skos:Concept，GOVERNANCE 自己在提案对齐里也写了 skos:Concept），不是"信息对象"。身份准则上它们靠名称字符串成立，放进 InformationObject 是范畴错置（OntoClean 的 identity/rigidity 检查会标红）。
- Territory ⊑ SpatialGeometry：辖区有组织身份（会设立/合并/撤销），纯几何建模弱；应拆为"组织单元 + 覆盖几何"（territoryCoversRegion 已经是正确方向，类层级放错了重心）。
- 正面：互斥/反例是 OntoClean 最有价值的产出，他们把 7 个坍缩反例做成了 SHACL 回归测试——方法上领先绝大多数工程本体。

---

## 三、结论与建议（按优先级）

**业务判定：骨架正确、机制完备、词汇真实，但当前版本是"半个本体 + 半个数据字典"，rc 阶段可内测，1.0.0 前必须完成语义纯化。**

P0（1.0.0 前必须）：
1. 把 relations.yaml 的 ~35 个裸列从"受管关系注册表"里降级为独立的 `data-dictionary` 层（或 mapping_only 裁定），URI 去掉清洗痕迹；
2. 给 Observation 补 observedAt/hasSource/hasResult（或直接采用 sosa:resultTime/observedProperty/hasResult），补 Evidence 的最小属性；SHACL 强制"观测必须带时间与来源"，兑现注释承诺；
3. 加"YAML 注册表 URI ⊆ TTL 定义"的一致性测试，修掉 crosswalk/concepts.yaml 的悬空引用和 ActualSalesCrates null 字段。

P1：
4. ChannelType/VisitPurpose/VisitMode 迁到 skos:Concept 方案；Territory 挂组织单元；
5. 补 SalesRep、Route、VisitPlan 分配与频次、PJP 达成率度量——打通拜访洞察闭环；
6. spatial_scope 改受管区域实例；指标值改 hasResult/QuantityValue 结构（带单位），为后续接入 QUDT 留路。

P2：
7. Product/品类维度按 6 态流程立项（这会是下一个大提案，也正好检验治理状态机的成色）。

---

## 外部基准来源

- W3C [Semantic Sensor Network Ontology (SSN/SOSA)](https://www.w3.org/TR/vocab-ssn/)、[SSN Extensions](https://www.w3.org/TR/vocab-ssn-ext/)、[The SOSA/SSN Ontology: A Joint W3C and OGC Standard (Semantic Web Journal)](https://www.semantic-web-journal.net/content/sosassn-ontology-joint-w3c-and-ogc-standard-specifying-semantics-sensors-observations)、[SOSA: A Lightweight Ontology (Janowicz et al.)](https://arxiv.org/html/1805.09979v2)
- Guarino & Welty [An Overview of OntoClean](https://www.loa.istc.cnr.it/old/Papers/GuarinoWeltyOntoCleanv3.pdf)、[Evaluating ontological decisions with OntoClean (CACM 2002)](https://dl.acm.org/doi/10.1145/503124.503150)；Poveda-Villalón [A Pitfall-Based Approach to Ontology Diagnosis](https://oa.upm.es/39448/1/MARIA_POVEDA_VILLALON.pdf)
- Grüninger & Fox TOVE 能力问题法与综述：[Use of Competency Questions in Ontology Engineering: a Survey (2023)](https://www.inf.ufes.br/~monalessa/wp-content/papercite-data/pdf/use_of_competency_questions_in_ontology_engineering__a_survey_2023.pdf)、[Characterising Competency Questions for Ontologies (CEUR-WS)](https://ceur-ws.org/Vol-4176/caos-9.pdf)、[NIST: The Evaluation of Ontologies](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=822618)
- GS1 [Global Location Number (GLN)](https://www.gs1.org/standards/id-keys/gln)、[GLN Data Model Solution Standard](https://www.gs1.org/standards/gln-data-model-solution-standard/current-standard)
- 可口可乐系统 NARTD 口径：[Coca-Cola Q4/FY2025 Results](https://investors.coca-colacompany.com/news-events/press-releases/detail/1151/coca-cola-reports-fourth-quarter-and-full-year-2025-results)、[CCEP 2025 Annual Report](https://www.cocacolaep.com/assets/Global/Investors/2025-Annual-Report/CCEP-Annual-Report-and-Form-20-F-2025.pdf)
- 零售集中度测量：[USDA ERS food retailing HHI](http://www.ers.usda.gov/data-products/charts-of-note/105671)、[US Census: Evolution of U.S. Retail Concentration](https://www.census.gov/data/academy/webinars/2021/evolution-of-retail-concentration.html)、[DOJ HHI](https://www.justice.gov/atr/herfindahl-hirschman-index)、[OECD methodologies](https://one.oecd.org/document/DAF/COMP/WD(2021)3/en/pdf)
