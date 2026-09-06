# prism-ontology GitHub Issues #1-#7 综合修复实施计划

> **执行者指南**：所有任务包含完备的测试断言、代码逻辑与验证指令。

**目标**：彻底解决 GitHub 7 个审查 Issue，消除工程卫生隐患、修复注册表漂移与假阴性、落地 SOSA/PROV-O 观测模型、剥离物理列以守住治理红线、重构分类学及拜访骨架。

**架构理念**：
- 严格分离语义层与数据工程映射层（`relations.yaml` vs `field-mapping.yaml`）；
- 严格对齐国际开放标准（W3C SOSA/SSN、PROV-O、SKOS、QUDT）；
- 建立端到端强自洽的 CI 自动化双向闭包测试（YAML ↔ RDF Graph）。

**技术栈**：Python 3.10+, rdflib 7.x, pyshacl 0.40+, owlrl 7.x, pytest 9.x, PyYAML

---

## 全局约束与红线
1. 严禁使用裸物理宽表字段作为全局受管 URI；
2. YAML 注册表中的每一个受管 URI 必须且只能对应合并 TTL 知识图中的一个合法 Subject；
3. 不得破坏既有 Golden CQ 的 SPARQL 行为级验证；
4. 任何概念变更必须同步更新 SHACL 约束并验证无 OWL-RL 逻辑矛盾。

---

### Task 1: 工程卫生与构建确定性修复 (对应 Issue #7)

**涉及文件**：
- 修改：`.gitignore`
- 修改：`pyproject.toml`
- 修改：`scripts/build_profile_release.py`
- 修改：`profiles/outlet-insight/competency-questions.yaml`
- 修改：`tests/test_cq_expressibility.py`
- 命令清理：`git rm -r --cached tests/__pycache__`

**任务目标**：
1. 从 git 索引中清除 pycache 字节码；
2. 在 `pyproject.toml` 中补齐 `owlrl>=7.1.4` 并明确依赖版本；
3. 拆分 `release_date`（固化为发布签署日期 2026-08-25）与 `build_timestamp`；
4. 修复 CQ-007 的中文谓词命名，并适配本地新增的 CQ-011（消除硬编码 `assert len == 10`）。

- [ ] **Step 1: 清理 pycache 跟踪并核验 .gitignore**
  执行 `git rm -r --cached tests/__pycache__`，确保 `.gitignore` 包含 `__pycache__/`。
- [ ] **Step 2: 完善 pyproject.toml 依赖声明**
  在 `dependencies` 中补充 `"owlrl>=7.1.4"`。
- [ ] **Step 3: 优化 build_profile_release.py 的日期与构建戳逻辑**
  解耦 `release_date`（固化为 `"2026-08-25"`）与 `build_timestamp`。
- [ ] **Step 4: 规范 CQ-007 谓词与 CQ 数量断言**
  - 规范 CQ-007 fixture 谓词；
  - 适配本地 CQ-011（`assert len(cqs) >= 10` 并包含 CQ-011 SPARQL 测试逻辑）。
- [ ] **Step 5: 验证测试**
  运行 `.venv/bin/pytest -v tests/`。

---

### Task 2: 注册表一致性修复与强闭包检验 (对应 Issue #3)

**涉及文件**：
- 修改：`proposals/mousheng/ontology_crosswalk.yaml`
- 修改：`profiles/outlet-insight/metric-definitions.yaml`
- 修改：`profiles/outlet-insight/concepts.yaml`
- 新增测试：`tests/test_profile_registry_integrity.py`

**任务目标**：
1. 修正 crosswalk 中的 4 处悬空属性和度量；
2. 修复 `ActualSalesCrates` 中的 null 与 `「None」` 字符；
3. 治理 `concepts.yaml` 中未在 TTL 定义的 7 个概念；
4. 编写强闭包测试：校验 YAML 注册表与合并后的 RDF 知识图 Subject 双向一致性。

- [ ] **Step 1: 修复 ontology_crosswalk.yaml 悬空引用**
  - `prism:outlet/locatedInRegion` → `prism:outlet/locatedInAdministrativeRegion`
  - `prism:outlet/belongsToTerritory` → `prism:outlet/coveredBySalesTerritory`
  - `prism:metric/RoomCount` → `prism:metric/CtripRoomCount`
  - `prism:metric/RevenuePotential` → `prism:metric/RevenuePotentialWithAgreement`
- [ ] **Step 2: 修复 metric-definitions.yaml 中 ActualSalesCrates**
  完善其物理列描述，修正 `interpretation_boundary`，消除字面量 `「None」`。
- [ ] **Step 3: 治理 concepts.yaml 中 7 个未定义概念**
  补齐或治理未定义概念。
- [ ] **Step 4: 编写 test_profile_registry_integrity.py 强闭包测试**
  验证 YAML 中每个受管 URI 均存在于 TTL RDF Graph 中。
- [ ] **Step 5: 验证测试**
  运行 `.venv/bin/pytest -v tests/test_profile_registry_integrity.py`。

---

### Task 3: 观测模型与证据结构健全 (对应 Issue #2)

**涉及文件**：
- 修改：`ontology/core/core.ttl`
- 修改：`ontology/core/core.shacl.ttl`
- 修改：`profiles/outlet-insight/relations.yaml`
- 测试：`tests/test_ontology_integrity.py`

- [ ] **Step 1: 在 core.ttl 中增加观测元数据属性**
  补充 `observedAt`、`hasSource`、`hasResultValue` 等。
- [ ] **Step 2: 丰富 Evidence 类定义与关联属性**
  为 `prism-core:Evidence` 定义必要溯源属性。
- [ ] **Step 3: 在 core.shacl.ttl 中编写强制非空形状**
  定义 `prism-core:ObservationShape` 约束。
- [ ] **Step 4: 运行本体一致性与 SHACL 测试**
  运行 `.venv/bin/pytest -v tests/test_ontology_integrity.py`。

---

### Task 4: 治理红线治理与宽表物理列剥离 (对应 Issue #1)

**涉及文件**：
- 新增：`profiles/outlet-insight/field-mapping.yaml`
- 修改：`profiles/outlet-insight/relations.yaml`
- 修改：`scripts/build_profile_release.py`

- [ ] **Step 1: 提取并创建 field-mapping.yaml**
  将宽表物理直通列迁移至映射层。
- [ ] **Step 2: 精简并净化 relations.yaml**
  仅保留真正受管关系。
- [ ] **Step 3: 更新发布脚本打包清单**
  更新 `build_profile_release.py`。

---

### Task 5: 分类学（SKOS）与销售服务关系重构 (对应 Issue #4)

**涉及文件**：
- 修改：`ontology/outlet/outlet.ttl`
- 修改：`ontology/sales-visit/sales-visit.ttl`
- 修改：`ontology/outlet/outlet.shacl.ttl`
- 修改：`ontology/sales-visit/sales-visit.shacl.ttl`

- [ ] **Step 1: outlet.ttl 业态与辖区重构**
  `ChannelType` 对齐 `skos:Concept`；`Territory` 增加组织单元语义。
- [ ] **Step 2: sales-visit.ttl 概念与关系深化**
  `VisitPurpose`/`VisitMode` 对齐 `skos:Concept`；`ServiceRelationship` 增加 `hasServiceProvider` 与 `validDuring`。
- [ ] **Step 3: 运行完整性与推理测试**
  运行 `.venv/bin/pytest -v`。

---

### Task 6: 销售拜访业务骨架补齐 (对应 Issue #5)

**涉及文件**：
- 修改：`ontology/sales-visit/sales-visit.ttl`
- 修改：`profiles/outlet-insight/relations.yaml`
- 修改：`profiles/outlet-insight/concepts.yaml`

- [ ] **Step 1: 补充 SalesRep 与 Route 实体类**
- [ ] **Step 2: 建立计划分配与频次属性**
- [ ] **Step 3: 同步注册到 Profile 并通过测试**

---

### Task 7: 6 态治理提案归档与全新发布包编译 (对应 Issue #6 及发布)

**涉及文件**：
- 新增：`proposals/mousheng/MS-PROP-021-product-category-taxonomy.yaml`
- 新增：`proposals/mousheng/MS-PROP-022-bitemporal-temporal-semantics.yaml`
- 产出：`dist/outlet-insight/0.1.0-rc3/`
- 脚本执行：`python scripts/build_profile_release.py`

- [ ] **Step 1: 编写提案立项文件**
- [ ] **Step 2: 全量自动化测试回归**
- [ ] **Step 3: 重新编译发布包并检验 sha256**
