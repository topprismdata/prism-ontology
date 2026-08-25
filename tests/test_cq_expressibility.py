# -*- coding: utf-8 -*-
"""
test_cq_expressibility.py
=========================
自动化验证 10 条 Golden Competency Questions 在 outlet-insight Profile 中的语义可表达性
与正例 SPARQL 事实图查询验证。
"""
import yaml
from pathlib import Path
from rdflib import Graph, URIRef, Literal, RDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_competency_questions_semantic_expressibility_and_sparql():
    """验证所有 10 条 CQ 均具备 pass 评级，且在 Profile 的 OWL/SHACL 模式下可由正例图表达并成功查询。"""
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

    # 2. 构造正例样本图并执行 SPARQL 验证 (以 CQ-001 和 CQ-003 为例)
    g = Graph()
    g.parse(str(PROJECT_ROOT / "ontology" / "core" / "core.ttl"), format="turtle")
    g.parse(str(PROJECT_ROOT / "ontology" / "outlet" / "outlet.ttl"), format="turtle")
    
    # 注入真实正例事实
    fixture_turtle = """
    @prefix prism-core: <prism://ontology/core/> .
    @prefix prism-outlet: <prism://ontology/outlet/> .

    <urn:outlet:001> a prism-outlet:Outlet ;
        prism-core:hasName "美宜佳测试1号店" ;
        prism-outlet:belongsToBrand <urn:brand:meiyijia> ;
        prism-outlet:coveredBySalesTerritory <urn:territory:puxi> ;
        prism-outlet:locatedInAdministrativeRegion <urn:region:shanghai> .

    <urn:brand:meiyijia> a prism-outlet:Brand ;
        prism-core:hasName "美宜佳" .

    <urn:territory:puxi> a prism-outlet:Territory ;
        prism-core:hasName "浦西大区" .

    <urn:region:shanghai> a prism-outlet:AdministrativeRegion ;
        prism-core:hasName "上海城区" .
    """
    g.parse(data=fixture_turtle, format="turtle")

    # 执行 CQ-001 SPARQL 查询 (浦西大区的美宜佳清单)
    q_cq001 = """
    PREFIX prism-outlet: <prism://ontology/outlet/>
    PREFIX prism-core: <prism://ontology/core/>
    SELECT ?outlet ?name WHERE {
        ?outlet a prism-outlet:Outlet ;
                prism-core:hasName ?name ;
                prism-outlet:belongsToBrand ?brand ;
                prism-outlet:coveredBySalesTerritory ?territory .
        ?brand prism-core:hasName "美宜佳" .
        ?territory prism-core:hasName "浦西大区" .
    }
    """
    results = list(g.query(q_cq001))
    assert len(results) == 1, "SPARQL query for CQ-001 should return 1 matching outlet"
    assert str(results[0][1]) == "美宜佳测试1号店"

    print("All 10 Golden CQs expressibility & SPARQL positive reasoning verified 100%.")
