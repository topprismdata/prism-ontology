# ml-sales-batch-002 — SRP 销售拜访规划净新增概念提案批次（批次二）

**提案方**：TopPrism ML Agent Program（达能潜店雷达 SRP 需求回流）
**提交日期**：2026-10-09
**状态**：`proposed`（七项逐项进入 GOVERNANCE.md §2 六态状态机评审，裁定权归治理委员会）
**编号空间**：MS-PROP-031 … MS-PROP-037（单调递增，紧接 ml-agent 批次一 MS-PROP-023…030）
**分支基线**：origin/main（`a081111`）；批次一（MS-PROP-023…030，PR #21）尚未合入，本批次编号按已分配至 030 续排

## 1. 批次动机

达能潜店雷达 SRP 需求书覆盖围栏、门店池、排班、路径、执行闭环五大段。为
给 SRP 各功能模块找到**跨供应商成立的公共语义**（而非平台专有对象），提案方
精读 14 篇 Salesforce 官方帮助文档全文（`/tmp/sf_pages/*.txt`，URL 与引文
逐条见各提案 `manual_evidence` 段），对照 sales-visit.ttl / core.ttl /
outlet.ttl / insight.ttl 查重后，确认 **7 项语义在 L1 与 sales-visit 均无
对应类**，且每项都有官方机制级出处。这 7 项若不上浮，SRP 的服务包配置、
排班审计、坐标治理、结构化回收、候选/承诺二分、批次治理只能停留在各引擎
局部命名空间，跨项目无法统一推理。故以**一个提案批次**整体提交：一次提案、
逐项审查、统一版本锁定。

## 2. 提案索引

| 编号 | 文件 | URI | 名称 | 父类主张 | SRP 需求 | 手册出处（/tmp/sf_pages/） | 与既有类关系（一句话） |
|---|---|---|---|---|---|---|---|
| MS-PROP-031 | `MS-PROP-031-service-package.yaml` | `prism:sales/ServicePackage` | 拜访服务包 | `prism-core:Policy` | FR-11 | visit_plans_create, maps_app_settings, optimization_methods | 服务标准规范载体（频次/时长/时段），被计划实例化；与售点侧 VisitModeConstraint 正交互补 |
| MS-PROP-032 | `MS-PROP-032-visit-optimization.yaml` | `prism:sales/VisitOptimization` | 拜访优化求解 | `prism-core:Activity` | FR-13/14 | visit_plans_create, optimization_methods, routes_vs_schedule | 求解过程（prov:Activity），产出 VisitPlan；与 Decision（审批）正交 |
| MS-PROP-033 | `MS-PROP-033-shift-constraint.yaml` | `prism:sales/ShiftConstraint` | 班次约束 | `prism-core:Constraint` | FR-11/12 | maps_app_settings, optimization_methods, create_route | 业代侧工作历时间边界；与售点侧 VisitModeConstraint 显式划界 |
| MS-PROP-034 | `MS-PROP-034-verified-location.yaml` | `prism:sales/VerifiedLocation` | 已核验坐标 | `prism-core:Observation` | FR-02~07 | geocoding_faq, activity_logging | 核验性位置观测（SOSA），取值优先于机器编码；与 DerivedEstimate（编码值）对偶 |
| MS-PROP-035 | `MS-PROP-035-visit-disposition.yaml` | `prism:sales/VisitDisposition` | 拜访处置表单 | `prism-core:InformationObject` | FR-16/17 | checkin_checkout, activity_logging | 结单结构化业务处置；与 VisitRecord（机制日志）三分、拒绝 Observation（业务申报非外部测量） |
| MS-PROP-036 | `MS-PROP-036-visit-pool.yaml` | `prism:sales/VisitPool` | 拜访门店池 | `prism-core:InformationObject` | FR-09/10/15 | visit_plans_create, routes_vs_schedule, mass_actions | 候选集合工件（版本化、不产生义务）；与 VisitPlan（承诺面）严格二分 |
| MS-PROP-037 | `MS-PROP-037-territory-model.yaml` | `prism:sales/TerritoryModel` | 辖区规划模型 | `prism-core:Plan` | FR-01/04/05 | sales_territories_intro, tm1_vs_etm, territory_planning | 设计工件（规划态→激活）；与 outlet:Territory（结果区域）设计/结果二分 |

## 3. 七概念关系图（文本）

```text
继承面（parent 主张，父类均为 core 既有类）
  prism-core:Policy        ── ServicePackage（服务标准规范）
  prism-core:Activity      ── VisitOptimization（求解过程，prov:Activity）
  prism-core:Constraint    ── ShiftConstraint（业代工作历边界）
  prism-core:Observation   ── VerifiedLocation（核验位置测量，sosa:Observation）
  prism-core:InformationObject ─┬─ VisitDisposition（结构化处置）
                                └─ VisitPool（候选集合工件）
  prism-core:Plan          ── TerritoryModel（辖区设计工件，规划态→激活）

SRP 流水（候选 → 排班 → 发布 → 执行 → 回收）
  TerritoryModel(激活) ──塑造──► Territory/Route 结构
  VisitPool(候选,版本v) ──(VisitOptimization 消费 ServicePackage+ShiftConstraint)
        ──产生──► VisitPlan(承诺,既有类) ──发布──► ActualVisit(既有类)
        ──结单──► VisitRecord(既有类,机制日志) + VisitDisposition(业务处置)
  VerifiedLocation ◄──被消费── 围栏归属/线路计算/打卡距离校验（坐标质量底座）
```

## 4. 与官方机制、SRP 功能点的对应

14 篇手册 → 7 概念的证据映射（逐条引文与 URL 见各提案 manual_evidence）：

| SRP 功能点（矩阵行号） | 官方机制 | 本批次概念 |
|---|---|---|
| #22-24 服务包/频次/工作时间（FR-11） | Maps Advanced visit criteria；Default Event Duration / Shift Times / Break Information / Optimize By | MS-PROP-031、MS-PROP-033 |
| #27-31 排班生成/路径求解（FR-13/14） | Plan Visits / Plan My Visits / StartAdvancedOptimization*；Shortest Distance / Fastest Shift Completion / Least Windshield Time；Routes(日)×Schedule(周) 双工具 | MS-PROP-032 |
| #25-26 工作量测算/超载告警（FR-12） | shift durations、traffic windows、fixed appointment times 为优化输入因子 | MS-PROP-033（消费方 MS-PROP-032） |
| #2-6、#13 围栏/片区/门店池坐标（FR-02~07） | Verified Latitude/Longitude 优先于标准经纬度；geocoder 季度更新与误差面；Verification Distance | MS-PROP-034 |
| #34-36、#41 发布/执行回收/异常工作台（FR-16/17） | Check In/Out + Auto Check Out；Custom Disposition 字段集表单（必填强制、依赖挑选列表限制） | MS-PROP-035 |
| #16-22、#25 池生成/准入/汰换/确认（FR-09/10/15） | visit criteria 圈定候选；Schedule queue；Mass Actions 圈选批量操作 | MS-PROP-036 |
| #1、#4-5、#11-12 规划批次/围栏调整/审批/版本发布（FR-01/04/05） | ETM Territory Models + planning state + activate；规则执行与部署分离；Audit Trail | MS-PROP-037 |

## 5. 五问法批次级结论

五问法逐问逐项见各提案文件 `five_questions` 段。批次级结论：7 项概念对象
客观稳定（配置、过程、边界、测量、记录、集合、设计工件均是可版本追溯的
管理对象）、跨供应商成立（Salesforce 与 SRP 引擎各自同构表达，无一依赖
平台专有 ID）、跨项目需要统一推理（服务包合规、排班审计、坐标治理、
结构化回收、候选/承诺二分、批次治理均为 SRP 多层共用的陈述）、定义明确
（各项给出可判定边界与越界判违）、不落入概念膨胀禁区（无临时字段、无
流水号、无平台专有 ID、全部不新增属性）。

## 6. 能力问题（CQ）汇总

每项净新增概念至少 1 条 CQ（表达力门槛）：

| CQ | 概念 | 场景 | 自然语言问题 | 表达力 | 数据可答 |
|---|---|---|---|---|---|
| CQ-009 | ServicePackage | 服务包合规（FR-11） | 某售点当前应获服务的频次/时长/时段标准是什么？其线路计划是否满足？ | pass | full |
| CQ-010 | VisitOptimization | 排班审计（FR-13/14） | 某线路计划由哪次求解、以何种方法、消费哪些约束产生？重放输入是否可取？ | pass | full |
| CQ-011 | ShiftConstraint | 工作量测算（FR-12） | 某业代某日班次窗口、休息与固定占用各是多少？计划工时是否超载？ | pass | full |
| CQ-012 | VerifiedLocation | 坐标治理（FR-02~07） | 某售点当前生效的核验坐标来自哪次核验（谁、何时、何方式）？与机器编码分歧多大？ | pass | full |
| CQ-013 | VisitDisposition | 执行回收（FR-17） | 某次拜访结单提交了哪些结构化处置字段？缺失/失败是否被记录而非静默丢弃？ | pass | full |
| CQ-014 | VisitPool | 池治理（FR-09/10） | 某服务周期的周访/双周访池是哪个版本？本版相对上版进出哪些门店、依据什么规则？ | pass | full |
| CQ-015 | TerritoryModel | 批次治理（FR-01） | 某辖区/围栏批次处于什么状态？由谁在何时审批激活？生效版本回滚到哪一版？ | pass | full |

CQ 编号续接批次一（CQ-001…008，见 `proposals/ml-agent/README.md` 批次一版本）。

## 7. 防概念膨胀自检（GOVERNANCE.md §2 裁定原则 2）

- [x] 不含任何平台专有字段（Salesforce Field Set 名、API 方法名等仅作事实源与引文）
- [x] 不含批次流水号（ml-sales-batch-002 仅作批次组织标识，不进入本体 URI）
- [x] 七项均不申请新增属性（proposed_properties 留空；参数面与生命周期状态留接受后 SHACL NodeShape）
- [x] 与既有 16 个 L1 类及 sales-visit 12 类、outlet 11 类逐一声明关系，无同义重复类

## 8. 已考虑并否决的候选（宁缺毋滥，防后续重复提案）

| 候选 | 否决理由 | 建议处置 |
|---|---|---|
| CheckInActivity（打卡活动） | 与 ActualVisit（物理事件）+ VisitRecord（系统记录）二分语义重复；再立活动类必触发 aligned_to_ 裁定 | aligned_to_ 既有二分；结构化业务结果缺口由 MS-PROP-035 补齐 |
| Geofence（围栏类） | 14 篇手册无围栏管理机制（仅圈选交互）；几何本质是 core:SpatialGeometry 实例，另立类属同义重复 | 围栏几何用 SpatialGeometry 承载；批次治理语义由 MS-PROP-037 承载 |
| Marker / MassAction（标记/批量动作） | 纯 UI 操作面概念，非客观稳定业务对象 | rejected（概念混淆/越界）：不提案 |
| POI（兴趣点搜索结果） | 搜索瞬时结果，非受管实体 | 不提案；搜入池后以成员 Outlet 身份存在 |

## 9. 边界备忘与提交方声明

- 批次通过前，7 项概念不存在于任何已发布 TTL，不发生任何行为变化；本批次
  为**纯新增提案**：不修改 `proposal-decisions.yaml`（委员会裁定记录，提交方
  不写）、不动 `ontology/**`、`profiles/**`、`dist/**`、`scripts/**`、
  `tests/**`；编号 MS-PROP-031…037 是否生效以委员会裁定为准。
- 与批次一（PR #21）关系：编号续接、目录相同（proposals/ml-agent/）、内容
  独立（批次一为 ML 共享核心，本批次为 SRP 销售拜访域）；两批次均基于
  origin/main，合入顺序由委员会决定，文件不相交。
- CQ-009…015 的评估口径（semantic_expressibility / data_answerability /
  blocking_reason / handling_policy）沿用批次一随批草案格式；如需完整
  competency_questions 扩展，待批次一裁定后统一登记，不在本批次展开。

## 10. 验证方式

```bash
# 1) YAML 语法自检（本目录 7 个提案文件 + 本 README）
python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob('proposals/ml-agent/MS-PROP-03*.yaml')];print('OK')"

# 2) 上游测试全绿（提案目录不在测试范围，回归不受影响）
.venv/bin/python -m pytest tests/ -q
```
