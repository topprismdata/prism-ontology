# Outlet Insight Profile v0.1.0-RC Competency Question Verification Report
Generated at: 2026-08-25T12:46:11+08:00
Profile URI: prism://ontology/profiles/outlet-insight
Git Commit: 34d165e71ab8adc5ace90981e271fb59d161f087

| CQ ID | 场景 | 自然语言提问 | 语义可表达性 | 数据可回答性 | 阻断限制原因 |
|---|---|---|---|---|---|
| CQ-001 | 指定品牌与区域清单 | 浦西大区的美宜佳清单 | pass | full | 无 |
| CQ-002 | 区域业态结构分布 | 江苏省各业态的售点数量分布 | pass | full | 无 |
| CQ-003 | 业态品牌集中度分析 | 上海城区餐饮连锁品牌的集中度与头部排行 | pass | full | 无 |
| CQ-004 | 群体同态指标对比 | 浦东大区与浦西大区在食杂店平均客流上的差异 | pass | full | 无 |
| CQ-005 | 多因子规则符合度评估 | 餐饮街门店数≥20家，周末客流排序，评分3.8占比超50%的街道候选 | pass | full | 无 |
| CQ-006 | 多维指标背离检测 | 哪些商圈存在高客流但大众点评评分显著偏低的背离现象？ | pass | full | 无 |
| CQ-007 | 数据稀疏度质检 | 景区周边客栈的客房数与星级分布 | pass | partial | 部分小微客栈缺少携程星级数据，触发质量限制提示并降级置信度 |
| CQ-008 | 外部竞品销量份额 (拒绝计算) | 可口可乐 vs 百事可乐在华东食杂店的真实销售箱数份额 | pass | none | 物理宽表缺失竞品在途销量 POS 数据，系统显式拒绝计算并输出限制 |
| CQ-009 | 统计到明细下钻 | 看排第一的瑞幸咖啡在上海城区的具体门店清单 | pass | full | 无 |
| CQ-010 | 视觉证据生成 | 生成上海市餐饮连锁品牌 TOP20 的门店数与评分双轴图 | pass | full | 无 |
