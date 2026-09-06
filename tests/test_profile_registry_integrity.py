# -*- coding: utf-8 -*-
"""
test_profile_registry_integrity.py
==================================
强闭包一致性测试：
1. 校验 concepts.yaml 中所有注册概念在本体 RDF 图中均有合法定义 (Subject 且具备 rdf:type)；
2. 校验 relations.yaml 中所有非物理列受管关系在本体 RDF 图中均有合法定义；
3. 校验 ontology_crosswalk.yaml 中的概念、属性与度量均存在于受管集合中；
4. 校验 metric-definitions.yaml 无 null 或「None」异常文本。
"""
import pytest
import yaml
from pathlib import Path
from rdflib import Graph, URIRef, RDF, RDFS, OWL

import json
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREFIX_MAP_FILE = PROJECT_ROOT / "profiles" / "outlet-insight" / "prefix-map.json"

with open(PREFIX_MAP_FILE, "r", encoding="utf-8") as f:
    PREFIX_MAP = json.load(f)["prefixes"]

def expand_uri(curie: str) -> URIRef:
    for prefix, full in PREFIX_MAP.items():
        if curie.startswith(prefix):
            return URIRef(curie.replace(prefix, full))
    if curie.startswith("prism://"):
        return URIRef(curie)
    raise ValueError(f"Unknown URI prefix for CURIE: {curie}")


@pytest.fixture(scope="module")
def ontology_graph():
    g = Graph()
    ttl_files = [
        PROJECT_ROOT / "ontology" / "core" / "core.ttl",
        PROJECT_ROOT / "ontology" / "outlet" / "outlet.ttl",
        PROJECT_ROOT / "ontology" / "insight" / "insight-artifact.ttl",
        PROJECT_ROOT / "ontology" / "sales-visit" / "sales-visit.ttl",
    ]
    for ttl in ttl_files:
        g.parse(str(ttl), format="turtle")
    return g


def test_concepts_defined_in_ontology(ontology_graph):
    """concepts.yaml 中每个受管概念必须在合并 TTL 图中作为合法类定义存在。"""
    concepts_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "concepts.yaml"
    with open(concepts_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for item in data["concepts"]:
        curie = item["uri"]
        uri = expand_uri(curie)
        # 必须作为 subject 存在，且拥有 rdf:type
        types = list(ontology_graph.objects(uri, RDF.type))
        assert len(types) > 0, f"Concept '{curie}' ({uri}) is registered in concepts.yaml but has no rdf:type definition in ontology TTLs!"


def test_managed_relations_defined_in_ontology(ontology_graph):
    """relations.yaml 中的核心领域关系必须在合并 TTL 图中作为合法属性定义存在（100% 闭包，不得漏定义）。"""
    relations_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "relations.yaml"
    with open(relations_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for item in data["relations"]:
        curie = item["uri"]
        uri = expand_uri(curie)
        types = list(ontology_graph.objects(uri, RDF.type))
        assert len(types) > 0, f"Relation '{curie}' ({uri}) is registered in relations.yaml but has no rdf:type definition in ontology TTLs!"


def test_field_mapping_cleanliness():
    """field-mapping.yaml 中的物理列全部属于 mapping_only 治理范围，且不应混入 relations.yaml。"""
    fm_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "field-mapping.yaml"
    rel_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "relations.yaml"

    with open(fm_file, "r", encoding="utf-8") as f:
        fm_data = yaml.safe_load(f)
    with open(rel_file, "r", encoding="utf-8") as f:
        rel_data = yaml.safe_load(f)

    rel_uris = set(r["uri"] for r in rel_data["relations"])
    assert fm_data["governance_status"] == "mapping_only"
    assert len(fm_data["field_mappings"]) == 44
    for m in fm_data["field_mappings"]:
        assert m["uri"] not in rel_uris, f"Physical column {m['uri']} must not leak into relations.yaml!"


def test_crosswalk_integrity(ontology_graph):
    """proposals/mousheng/ontology_crosswalk.yaml 映射引用的概念与属性必须存在。"""
    cw_file = PROJECT_ROOT / "proposals" / "mousheng" / "ontology_crosswalk.yaml"
    metrics_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "metric-definitions.yaml"
    
    with open(cw_file, "r", encoding="utf-8") as f:
        cw_data = yaml.safe_load(f)
    with open(metrics_file, "r", encoding="utf-8") as f:
        metrics_data = yaml.safe_load(f)
    
    managed_metrics = set(m["uri"] for m in metrics_data["metrics"])

    for entry in cw_data["crosswalk"]:
        if "ontology_concept_uri" in entry:
            c_uri = expand_uri(entry["ontology_concept_uri"])
            assert (c_uri, RDF.type, None) in ontology_graph, f"Crosswalk references undefined concept: {entry['ontology_concept_uri']}"
        if "ontology_property" in entry:
            p_uri = expand_uri(entry["ontology_property"])
            assert (p_uri, RDF.type, None) in ontology_graph, f"Crosswalk references undefined property: {entry['ontology_property']}"
        if "metric_concept_uri" in entry:
            m_curie = entry["metric_concept_uri"]
            assert m_curie in managed_metrics, f"Crosswalk references unregistered metric: {m_curie}"
        if "ontology_insight_type" in entry:
            i_uri = expand_uri(entry["ontology_insight_type"])
            assert (i_uri, RDF.type, None) in ontology_graph, f"Crosswalk references undefined insight type: {entry['ontology_insight_type']}"


def test_metric_definitions_no_literal_none():
    """metric-definitions.yaml 中不应存在字面量「None」或关键字段 null。"""
    metrics_file = PROJECT_ROOT / "profiles" / "outlet-insight" / "metric-definitions.yaml"
    with open(metrics_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "「None」" not in content, "Found literal string '「None」' in metric-definitions.yaml!"
    
    data = yaml.safe_load(content)
    for m in data["metrics"]:
        assert m.get("interpretation_boundary") is not None, f"Metric {m['uri']} missing interpretation_boundary"
        assert "None" not in m["interpretation_boundary"], f"Metric {m['uri']} interpretation_boundary contains 'None'"


def test_dist_directories_validity():
    """校验 dist/outlet-insight/ 下不存在孤儿目录，每个发行目录均具备完整 manifest 与 sha256 校验和，且若已签署 tag 则目录与 tag 提交逐字节一致。"""
    dist_root = PROJECT_ROOT / "dist" / "outlet-insight"
    if not dist_root.exists():
        return
    valid_dirs = {"0.1.0-rc1", "0.1.0-rc2", "0.1.0-rc3", "0.1.0-rc4"}
    actual_dirs = {d.name for d in dist_root.iterdir() if d.is_dir()}
    unexpected = actual_dirs - valid_dirs
    assert not unexpected, f"Found unregistered orphaned distribution directories in dist/outlet-insight: {unexpected}"
    for d_name in actual_dirs:
        d_path = dist_root / d_name
        assert (d_path / "profile-manifest.json").exists(), f"Dist package {d_name} missing profile-manifest.json"
        assert (d_path / "checksums.sha256").exists(), f"Dist package {d_name} missing checksums.sha256"

        # 校验已签署 Git Tag 的历史发行目录绝对不可变（与 tag commit 树逐字节无差异）
        tag_name = f"outlet-insight-v{d_name}"
        tag_check = subprocess.run(
            ["git", "rev-parse", "--verify", f"refs/tags/{tag_name}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if tag_check.returncode == 0:
            diff_res = subprocess.run(
                ["git", "diff", f"{tag_name}^{{commit}}", "--", f"dist/outlet-insight/{d_name}"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            assert diff_res.returncode == 0 and not diff_res.stdout.strip(), (
                f"Immutability Violation: Release directory dist/outlet-insight/{d_name} has drifted from its signed tag {tag_name}!\n"
                f"Diff:\n{diff_res.stdout[:1000]}"
            )

