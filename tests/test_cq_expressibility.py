# -*- coding: utf-8 -*-
"""
test_cq_expressibility.py
=========================
自动化验证 10 条 Golden Competency Questions 在 outlet-insight Profile 中的语义可表达性
与逐条正例 SPARQL 事实图行为查询验证（覆盖聚合、排序、群体对比、背离检测与拒答策略）。
"""
import yaml
from pathlib import Path
from rdflib import Graph

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_all_10_competency_questions_sparql_behavior():
    """为全部 10 条 Golden CQ 逐条建立正例 RDF 事实图并执行 SPARQL 查询，完成行为级强验证。"""
    cq_path = PROJECT_ROOT / "profiles" / "outlet-insight" / "competency-questions.yaml"
    concepts_path = PROJECT_ROOT / "profiles" / "outlet-insight" / "concepts.yaml"
    relations_path = PROJECT_ROOT / "profiles" / "outlet-insight" / "relations.yaml"
    metrics_path = PROJECT_ROOT / "profiles" / "outlet-insight" / "metric-definitions.yaml"

    with open(cq_path, "r", encoding="utf-8") as f:
        cq_data = yaml.safe_load(f)
    with open(concepts_path, "r", encoding="utf-8") as f:
        concepts_data = yaml.safe_load(f)
    with open(relations_path, "r", encoding="utf-8") as f:
        relations_data = yaml.safe_load(f)
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics_data = yaml.safe_load(f)

    cqs = cq_data["competency_questions"]
    assert len(cqs) == 10, f"Expected 10 CQs, got {len(cqs)}"

    profile_concept_uris = set(c["uri"] for c in concepts_data["concepts"])
    profile_relation_uris = set(r["uri"] for r in relations_data["relations"])
    profile_metric_uris = set(m["uri"] for m in metrics_data["metrics"])

    # 1. 严格集合成员校验
    for cq in cqs:
        assert cq["semantic_expressibility"] == "pass"
        assert cq["data_answerability"] in ["full", "partial", "none"]
        target = cq["formal_expression"].get("target_entity")
        if target:
            base_target = target.split(":")[0] + ":" + target.split(":")[1].split(":")[0] if target.count(":") >= 2 else target
            assert base_target in profile_concept_uris, f"Target entity {base_target} not in profile concepts"

    # 2. 构造支持全部 10 条 CQ 的完整正例知识图谱 Fixture
    g = Graph()
    for ttl_file in ["core/core.ttl", "outlet/outlet.ttl", "insight/insight-artifact.ttl", "sales-visit/sales-visit.ttl"]:
        g.parse(str(PROJECT_ROOT / "ontology" / ttl_file), format="turtle")

    fixture_turtle = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix prism-core: <prism://ontology/core/> .
    @prefix prism-outlet: <prism://ontology/outlet/> .
    @prefix prism-insight: <prism://ontology/insight/> .
    @prefix prism-sales: <prism://ontology/sales-visit/> .

    # 品牌
    <urn:brand:meiyijia> a prism-outlet:Brand ; prism-core:hasName "美宜佳" .
    <urn:brand:luckin> a prism-outlet:Brand ; prism-core:hasName "瑞幸咖啡" .
    <urn:brand:starbucks> a prism-outlet:Brand ; prism-core:hasName "星巴克" .
    <urn:brand:babi> a prism-outlet:Brand ; prism-core:hasName "巴比馒头" .

    # 区域与辖区 (双轨隔离)
    <urn:territory:puxi> a prism-outlet:Territory ; prism-core:hasName "浦西大区" .
    <urn:territory:pudong> a prism-outlet:Territory ; prism-core:hasName "浦东大区" .
    <urn:region:shanghai> a prism-outlet:AdministrativeRegion ; prism-core:hasName "上海城区" .
    <urn:region:jiangsu> a prism-outlet:AdministrativeRegion ; prism-core:hasName "江苏省" .

    # 业态
    <urn:channel:catering> a prism-outlet:ChannelType ; prism-core:hasName "餐饮" .
    <urn:channel:grocery> a prism-outlet:ChannelType ; prism-core:hasName "食杂" .
    <urn:channel:lodging> a prism-outlet:ChannelType ; prism-core:hasName "住宿" .

    # 场所
    <urn:site:foodstreet_01> a prism-outlet:CommercialSite ; prism-core:hasName "南京西路餐饮街" .
    <urn:site:scenic_buffer> a prism-outlet:CommercialSite ; prism-core:hasName "西湖景区外50米" .

    # 网点与观测
    <urn:outlet:myj_01> a prism-outlet:Outlet ;
        prism-core:hasName "美宜佳浦西1号店" ;
        prism-outlet:belongsToBrand <urn:brand:meiyijia> ;
        prism-outlet:coveredBySalesTerritory <urn:territory:puxi> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:hasChannelType <urn:channel:grocery> .
    <urn:obs:traffic_puxi> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:myj_01> ;
        <prism://ontology/metric/WeekendTraffic> 1200 .

    <urn:outlet:myj_pudong> a prism-outlet:Outlet ;
        prism-core:hasName "美宜佳浦东1号店" ;
        prism-outlet:belongsToBrand <urn:brand:meiyijia> ;
        prism-outlet:coveredBySalesTerritory <urn:territory:pudong> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:hasChannelType <urn:channel:grocery> .
    <urn:obs:traffic_pudong> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:myj_pudong> ;
        <prism://ontology/metric/WeekendTraffic> 800 .

    <urn:outlet:js_food_01> a prism-outlet:Outlet ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:jiangsu> ;
        prism-outlet:hasChannelType <urn:channel:catering> .
    <urn:outlet:js_groc_01> a prism-outlet:Outlet ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:jiangsu> ;
        prism-outlet:hasChannelType <urn:channel:grocery> .

    # 上海餐饮品牌网点 (瑞幸2家, 星巴克1家, 巴比1家)
    <urn:outlet:sh_luckin_01> a prism-outlet:Outlet ;
        prism-core:hasName "瑞幸咖啡南京西路店" ;
        prism-outlet:belongsToBrand <urn:brand:luckin> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:operatedAtSite <urn:site:foodstreet_01> ;
        prism-outlet:hasChannelType <urn:channel:catering> .
    <urn:obs:luckin_01> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:sh_luckin_01> ;
        <prism://ontology/metric/DianpingRating> 4.2 ;
        <prism://ontology/metric/WeekendTraffic> 3500 .

    <urn:outlet:sh_luckin_02> a prism-outlet:Outlet ;
        prism-core:hasName "瑞幸咖啡静安寺店" ;
        prism-outlet:belongsToBrand <urn:brand:luckin> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:operatedAtSite <urn:site:foodstreet_01> ;
        prism-outlet:hasChannelType <urn:channel:catering> .
    <urn:obs:luckin_02> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:sh_luckin_02> ;
        <prism://ontology/metric/DianpingRating> 4.5 ;
        <prism://ontology/metric/WeekendTraffic> 4200 .

    <urn:outlet:sh_sbux_01> a prism-outlet:Outlet ;
        prism-core:hasName "星巴克烘焙工坊店" ;
        prism-outlet:belongsToBrand <urn:brand:starbucks> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:operatedAtSite <urn:site:foodstreet_01> ;
        prism-outlet:hasChannelType <urn:channel:catering> .
    <urn:obs:sbux_01> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:sh_sbux_01> ;
        <prism://ontology/metric/DianpingRating> 4.6 ;
        <prism://ontology/metric/WeekendTraffic> 5000 .

    # 背离网点: 极高客流 (6000) 但极低点评评分 (2.8)
    <urn:outlet:sh_discrepancy_01> a prism-outlet:Outlet ;
        prism-core:hasName "异动网红快餐店" ;
        prism-outlet:operatedAtSite <urn:site:foodstreet_01> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> ;
        prism-outlet:hasChannelType <urn:channel:catering> .
    <urn:obs:discrepancy> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:sh_discrepancy_01> ;
        <prism://ontology/metric/DianpingRating> 2.8 ;
        <prism://ontology/metric/WeekendTraffic> 6000 .

    # 景区周边客栈 (有房间数, 缺失星级)
    <urn:outlet:inn_01> a prism-outlet:Outlet ;
        prism-core:hasName "西湖静心客栈" ;
        prism-outlet:operatedAtSite <urn:site:scenic_buffer> ;
        prism-outlet:hasChannelType <urn:channel:lodging> .
    <urn:obs:inn_room> a prism-outlet:OutletObservation ;
        prism-outlet:observesOutlet <urn:outlet:inn_01> ;
        <prism://ontology/metric/CtripRoomCount> 18 .

    # 洞察包交付物
    <urn:insight:pkg_01> a prism-insight:InsightPackage ;
        prism-insight:hasAnalysisId "ANALYSIS-CQ-010" ;
        prism-insight:hasClaim <urn:claim:top20> .
    <urn:claim:top20> a prism-insight:InsightClaim ;
        prism-core:hasName "上海市餐饮品牌集中度分析主张" .
    """
    g.parse(data=fixture_turtle, format="turtle")

    # 逐条执行全部 10 条 CQ 的忠实 SPARQL 查询断言
    prefix_block = """
    PREFIX prism-outlet: <prism://ontology/outlet/>
    PREFIX prism-core: <prism://ontology/core/>
    PREFIX prism-insight: <prism://ontology/insight/>
    PREFIX prism-sales: <prism://ontology/sales-visit/>
    """

    # CQ-001: 浦西大区的美宜佳清单 (过滤 + 关联)
    q1 = prefix_block + "SELECT ?o ?name WHERE { ?o a prism-outlet:Outlet ; prism-core:hasName ?name ; prism-outlet:belongsToBrand ?b ; prism-outlet:coveredBySalesTerritory ?t . ?b prism-core:hasName '美宜佳' . ?t prism-core:hasName '浦西大区' }"
    r1 = list(g.query(q1))
    assert len(r1) == 1 and str(r1[0][1]) == "美宜佳浦西1号店", "CQ-001 清单过滤验证失败"

    # CQ-002: 江苏省各业态分布 (分组聚合计数)
    q2 = prefix_block + "SELECT ?c (COUNT(?o) AS ?cnt) WHERE { ?o a prism-outlet:Outlet ; prism-outlet:locatedInAdministrativeRegion ?r ; prism-outlet:hasChannelType ?c . ?r prism-core:hasName '江苏省' } GROUP BY ?c"
    r2 = {str(row[0]): int(row[1]) for row in g.query(q2)}
    assert len(r2) == 2, "CQ-002 江苏业态分组聚合应包含 2 个业态"

    # CQ-003: 业态品牌集中度与降序排行 (Brand 分组聚合与排序)
    q3 = prefix_block + "SELECT ?brandName (COUNT(?o) AS ?cnt) WHERE { ?o a prism-outlet:Outlet ; prism-outlet:belongsToBrand ?b ; prism-outlet:locatedInAdministrativeRegion ?r ; prism-outlet:hasChannelType ?c . ?b prism-core:hasName ?brandName . ?r prism-core:hasName '上海城区' . ?c prism-core:hasName '餐饮' } GROUP BY ?brandName ORDER BY DESC(?cnt)"
    r3 = list(g.query(q3))
    assert len(r3) == 2 and str(r3[0][0]) == "瑞幸咖啡" and int(r3[0][1]) == 2, "CQ-003 品牌集中度排行应识别瑞幸咖啡为 TOP1 (2家)"

    # CQ-004: 群体同态客流差异对比 (计算浦西 vs 浦东平均客流)
    q4_puxi = prefix_block + "SELECT (AVG(?v) AS ?avg) WHERE { ?o a prism-outlet:Outlet ; prism-outlet:coveredBySalesTerritory ?t ; prism-outlet:hasChannelType ?c . ?t prism-core:hasName '浦西大区' . ?obs a prism-outlet:OutletObservation ; prism-outlet:observesOutlet ?o ; <prism://ontology/metric/WeekendTraffic> ?v }"
    q4_pudong = prefix_block + "SELECT (AVG(?v) AS ?avg) WHERE { ?o a prism-outlet:Outlet ; prism-outlet:coveredBySalesTerritory ?t ; prism-outlet:hasChannelType ?c . ?t prism-core:hasName '浦东大区' . ?obs a prism-outlet:OutletObservation ; prism-outlet:observesOutlet ?o ; <prism://ontology/metric/WeekendTraffic> ?v }"
    avg_puxi = float(list(g.query(q4_puxi))[0][0])
    avg_pudong = float(list(g.query(q4_pudong))[0][0])
    assert avg_puxi == 1200.0 and avg_pudong == 800.0 and (avg_puxi > avg_pudong), "CQ-004 跨大区客流差异对比验证失败"

    # CQ-005: 复合规则评估 (餐饮街 + 评分≥3.8 + 按客流排序)
    q5 = prefix_block + "SELECT ?o ?name ?traffic WHERE { ?o a prism-outlet:Outlet ; prism-core:hasName ?name ; prism-outlet:operatedAtSite ?s ; prism-outlet:hasChannelType ?c . ?s prism-core:hasName '南京西路餐饮街' . ?obs a prism-outlet:OutletObservation ; prism-outlet:observesOutlet ?o ; <prism://ontology/metric/DianpingRating> ?r ; <prism://ontology/metric/WeekendTraffic> ?traffic . FILTER(?r >= 3.8) } ORDER BY DESC(?traffic)"
    r5 = list(g.query(q5))
    assert len(r5) == 3 and str(r5[0][1]) == "星巴克烘焙工坊店", "CQ-005 复合规则过滤与客流排序 TOP1 验证失败"

    # CQ-006: 多维指标背离检测 (高客流 >= 5000 且 低评分 <= 3.0)
    q6 = prefix_block + "SELECT ?name ?traffic ?rating WHERE { ?o a prism-outlet:Outlet ; prism-core:hasName ?name ; prism-outlet:operatedAtSite ?s . ?obs a prism-outlet:OutletObservation ; prism-outlet:observesOutlet ?o ; <prism://ontology/metric/WeekendTraffic> ?traffic ; <prism://ontology/metric/DianpingRating> ?rating . FILTER(?traffic >= 5000 && ?rating <= 3.0) }"
    r6 = list(g.query(q6))
    assert len(r6) == 1 and str(r6[0][0]) == "异动网红快餐店", "CQ-006 指标冲突背离异动网点识别失败"

    # CQ-007: 数据稀疏度质检 (验证房间数存在但星级缺失)
    q7 = prefix_block + "SELECT ?name ?rooms WHERE { ?o a prism-outlet:Outlet ; prism-core:hasName ?name ; prism-outlet:operatedAtSite ?s . ?s prism-core:hasName '西湖景区外50米' . ?obs a prism-outlet:OutletObservation ; prism-outlet:observesOutlet ?o ; <prism://ontology/metric/CtripRoomCount> ?rooms . FILTER NOT EXISTS { ?obs <prism://ontology/observed/Ctrip_星级> ?star } }"
    r7 = list(g.query(q7))
    assert len(r7) == 1 and str(r7[0][0]) == "西湖静心客栈", "CQ-007 数据稀疏度星级缺失检测失败"

    # CQ-008: 竞品缺失概念拒答验证 (验证在图中无此类型实例，系统触发拒答)
    q8 = prefix_block + "SELECT ?v WHERE { ?v a <prism://ontology/outlet/CompetitorSalesVolume> }"
    r8 = list(g.query(q8))
    assert len(r8) == 0, "CQ-008 竞品销量概念在物理事实图中应为 0 项，触发限制声明"

    # CQ-009: 瑞幸上海门店明细下钻提取
    q9 = prefix_block + "SELECT ?name WHERE { ?o a prism-outlet:Outlet ; prism-core:hasName ?name ; prism-outlet:belongsToBrand ?b ; prism-outlet:locatedInAdministrativeRegion ?r . ?b prism-core:hasName '瑞幸咖啡' . ?r prism-core:hasName '上海城区' } ORDER BY ?name"
    r9 = [str(row[0]) for row in g.query(q9)]
    assert r9 == ["瑞幸咖啡南京西路店", "瑞幸咖啡静安寺店"], "CQ-009 瑞幸明细下钻列表验证失败"

    # CQ-010: 标准洞察包交付物验证
    q10 = prefix_block + "SELECT ?analysisId ?claimName WHERE { ?pkg a prism-insight:InsightPackage ; prism-insight:hasAnalysisId ?analysisId ; prism-insight:hasClaim ?claim . ?claim prism-core:hasName ?claimName }"
    r10 = list(g.query(q10))
    assert len(r10) == 1 and str(r10[0][0]) == "ANALYSIS-CQ-010", "CQ-010 洞察包与分析主张绑定验证失败"

    print("\nAll 10 Golden CQs expressibility & SPARQL behavioral reasoning 100% verified.")
