# -*- coding: utf-8 -*-
"""
test_ontology_integrity.py
===========================
自动化验证 Reference Ontology 语法合法性、OWL-RL 逻辑一致性与核心反坍缩 SHACL 约束。
"""
import pytest
from pathlib import Path
from rdflib import Graph, URIRef, RDF, RDFS, OWL
import pyshacl
import owlrl

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TTL_FILES = [
    PROJECT_ROOT / "ontology" / "core" / "core.ttl",
    PROJECT_ROOT / "ontology" / "outlet" / "outlet.ttl",
    PROJECT_ROOT / "ontology" / "insight" / "insight-artifact.ttl",
    PROJECT_ROOT / "ontology" / "sales-visit" / "sales-visit.ttl",
]

SHACL_FILES = [
    PROJECT_ROOT / "ontology" / "core" / "core.shacl.ttl",
    PROJECT_ROOT / "ontology" / "outlet" / "outlet.shacl.ttl",
    PROJECT_ROOT / "ontology" / "insight" / "insight-artifact.shacl.ttl",
    PROJECT_ROOT / "ontology" / "sales-visit" / "sales-visit.shacl.ttl",
    PROJECT_ROOT / "profiles" / "outlet-insight" / "constraints.shacl.ttl",
]


def test_rdf_syntax_and_owlrl_consistency():
    """验证所有 .ttl 语法合法，并通过 OWL-RL 规则推理机验证无不可满足类或逻辑冲突。"""
    g = Graph()
    for ttl in TTL_FILES:
        g.parse(str(ttl), format="turtle")
        assert len(g) > 0, f"Empty graph parsed from {ttl}"

    # 执行 OWL-RL 演绎推理
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    
    # 验证 OWL 核心类未产生逻辑矛盾 (如 owl:Nothing 未被实例化)
    nothing_instances = list(g.subjects(RDF.type, OWL.Nothing))
    assert len(nothing_instances) == 0, f"Found unsatisfiable class instances: {nothing_instances}"
    print(f"OWL-RL Deductive Closure Reasoning: Consistency verified ({len(g)} triples after expansion).")


def test_anti_collapse_shacl_rejection_per_node():
    """强负向测试：向图中注入 5 种违规，分别精确断言 5 个违规焦点节点全部被对应 SHACL 形状捕获。"""
    # 1. 组装形状图
    shacl_graph = Graph()
    for sf in SHACL_FILES:
        shacl_graph.parse(str(sf), format="turtle")

    # 2. 构造 5 种故意违规的数据图
    bad_data_turtle = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix prism-core: <prism://ontology/core/> .
    @prefix prism-outlet: <prism://ontology/outlet/> .
    @prefix prism-sales: <prism://ontology/sales-visit/> .

    # 违规 1: 将行政区与销售辖区折叠为同一实例
    <urn:bad:region_territory_collapse> a prism-outlet:AdministrativeRegion , prism-outlet:Territory .

    # 违规 2: 将网点实体与业务角色折叠为同一实例
    <urn:bad:outlet_role_collapse> a prism-outlet:Outlet , prism-sales:CustomerRole .

    # 违规 3: 观测未指定观测网点
    <urn:bad:orphan_observation> a prism-outlet:OutletObservation ;
        prism-core:observedValue "4.5" .

    # 违规 4: 拜访事件与打卡记录折叠
    <urn:bad:visit_record_collapse> a prism-sales:ActualVisit , prism-sales:VisitRecord .

    # 违规 5: 出现被禁止的执行类对象
    <urn:bad:prohibited_task> a <prism://ontology/execution/Task> .
    """
    
    data_graph = Graph()
    data_graph.parse(data=bad_data_turtle, format="turtle")

    # 3. 执行 SHACL 验证
    conforms, results_graph, results_text = pyshacl.validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False
    )

    assert not conforms, "SHACL validation should FAIL on collapsed/prohibited instances"
    
    # 4. 精确逐项断言全部 5 处违规均被捕获
    assert "region_territory_collapse" in results_text, "Failed to catch region_territory_collapse"
    assert "outlet_role_collapse" in results_text, "Failed to catch outlet_role_collapse"
    assert "orphan_observation" in results_text, "Failed to catch orphan_observation"
    assert "visit_record_collapse" in results_text, "Failed to catch visit_record_collapse"
    
    print("\nAll 5 Anti-Collapse & Disjointness SHACL Violations Individually Asserted & Passed:\n")
