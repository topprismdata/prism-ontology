# prism-ontology 深度评审报告

日期：2026-09-06 ｜ 本地：/Users/guohongbin/github/prism-ontology ｜ HEAD: d408175（与 origin/main 同步）

## 一句话结论

这是 33 个仓库中工程质量最高的项目之一：一个治理规范完整、机器可验证、发布可复现的 OWL/SHACL 本体仓库，测试真实通过，发行链路自洽。适合作为 TopPrism 语义底座的骨架继续演进。

## 项目定位

"棱镜世界模型"的共享语义契约：定义可复用概念（Outlet、Territory、Observation、InsightClaim 等）、关系、反概念坍缩约束（SHACL）和场景化 Operational Profile，本身不存业务事实、不执行算法。首个垂直切片是面向"谋圣·售点洞察"场景的 Outlet Insight Profile（v0.1.0-rc2，Release Candidate）。

## 实测验证结果（全部真实执行）

| 验证项 | 结果 |
|---|---|
| pytest 测试套件 | ✅ 3/3 passed（0.35s） |
| Turtle 语法 + OWL-RL 推理一致性 | ✅ 通过（4 个本体模块合并推理无不可满足类） |
| SHACL 反坍缩负向测试 | ✅ 7 种概念坍缩/越界注入全部被精确拦截 |
| 10 条 Golden CQ 行为级 SPARQL 验证 | ✅ 全部通过（正例事实图 + 查询断言） |
| dist/v0.1.0-rc2 SHA-256 校验 | ✅ 11/11 文件 OK |
| 发行链路（Source → Dist → Tag） | ✅ 源提交 f8fa1d2 是发行 tag 417cb65 的可追溯祖先，annotated tag 存在 |
| 构建可复现性 | ✅ 重跑 build_profile_release.py 后，全部语义内容文件逐字节一致；仅 manifest 提交戳/时间戳/报告时间戳变化（符合设计） |
| 治理记录 | ✅ proposals/mousheng 有 20 条裁定，状态机真实运转（accepted / profile_local / mapping_only 混合），对齐 SOSA/DQV/PROV-O/schema.org |

## 架构亮点

1. **反概念坍缩设计是灵魂**：把"行政区≠销售辖区、网点≠客户角色、实际拜访≠打卡记录、观测≠估计、主张≠事实"五组区分做成机器可验证的 SHACL 互斥约束，并有负向测试证明真的拦得住。这比大多数"文档式本体"扎实得多。
2. **测试是行为级的**：CQ 测试不是摆设——构造真实 RDF 事实图（美宜佳/瑞幸/星巴克 fixture），逐条跑 SPARQL，覆盖聚合、排序、跨区对比、背离检测、数据稀疏拒答（CQ-008 的"竞品销量拒答"设计尤其务实）。
3. **确定性发行**：dist/ 带 SHA-256 清单 + manifest 溯源提交 + annotated tag，本次实测重建后内容哈希完全一致（唯一差异是时间戳字段），"可复现发布"名不虚传。
4. **治理真实运转**：6 态提案状态机（accepted/aligned_to_/profile_local/mapping_only/rejected/deferred）有 20 条带 rationale 的裁定记录，五问法原则 + 防概念膨胀红线写进了 GOVERNANCE.md。

## 发现的问题（按重要性）

1. **【中】L1 core.ttl 部分基类缺乏下游使用证据**：Entity/Policy/Constraint/Eligibility/Decision/TimeInterval 等 16 个 L1 概念中，Sales-visit 和 insight 模块只用了少数几个；Policy、Eligibility、Decision 目前没有任何关系指向它们，属于"预留但未验证"的概念，有概念膨胀风险（尽管治理红线明确写了要防）。
2. **【中】tests/ 里有多个 Python 版本的 __pycache__ 被提交进仓库**（cpython-313 × pytest 9.0.2 / 9.1.1），应清理并加入 .gitignore（`__pycache__/` 已在 .gitignore，说明是 ignore 生效前提交的）。
3. **【低】CQ-007 的谓词拼写**：fixture 中星级谓词写为 `prism://ontology/observed/Ctrip_星级`（中文+下划线的 URI），与 metric 命名空间的规整风格不一致，虽然只出现在负向 NOT EXISTS 场景。
4. **【低】release_date 字段语义漂移**：重新构建时 release_date 会被刷新为构建日期（实测 2026-08-25 → 2026-08-28），发行"日期"与"构建时间"混用；建议分离 `build_timestamp` 与 `release_date`。
5. **【低】owlrl 版本未钉死**：pyproject 依赖 rdflib/pyshacl/owlrl 未锁版本，不同版本推理闭包细节可能有差异（本次 7.1.4/0.30.1/7.4.0 通过）。
6. **【备忘】验证过程副作用已恢复**：上一轮验证时重跑构建脚本弄脏了 dist/ 三个文件的提交戳字段，本次已 `git checkout -- dist/` 恢复干净（并清掉了一个残留的 .git/index.lock）。

## 建议的下一步

- 走 1.0.0 前的两件事：给 L1 未使用概念补充 CQ/正例或降级为 profile_local；清理 __pycache__。
- 若要接入下游（autogluon-assistant / mousheng-outlet-insight），按 README 消费路径实现 profile.lock 校验，可先用 scripts/stamp_release_commit.py + checksums 做运行时阻断验证。
