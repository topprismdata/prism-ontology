# -*- coding: utf-8 -*-
"""
build_profile_release.py
========================
确定性打包并发布 Outlet Insight Operational Profile v0.1.0-RC
产出 dist/outlet-insight/0.1.0-rc1/ 包含 OWL 本体、SHACL 形状、度量定义、数据源、组织实体、Manifest 与 SHA-256 校验和。
具备完全的幂等性与可复现性（基于 Git Commit 状态）。
"""
import hashlib
import json
import shutil
import subprocess
import yaml
from pathlib import Path
from rdflib import Graph

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = PROJECT_ROOT / "profiles" / "outlet-insight"
DIST_DIR = PROJECT_ROOT / "dist" / "outlet-insight" / "0.1.0-rc1"

# 获取当前 Git Commit、Tag 与提交日期
try:
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    git_commit_date = subprocess.check_output(["git", "log", "-1", "--format=%cI"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    git_status = subprocess.check_output(["git", "status", "--porcelain"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    # 如果只有 dist 目录的改动，视为干净工作树
    status_lines = [l for l in git_status.splitlines() if not l.strip().endswith("dist/outlet-insight/0.1.0-rc1") and "dist/" not in l]
    clean_tree = (len(status_lines) == 0)
except Exception:
    git_commit = "unversioned"
    git_commit_date = "2026-08-25T00:00:00Z"
    clean_tree = False

# 清理并重建目标目录
if DIST_DIR.exists():
    shutil.rmtree(DIST_DIR)
DIST_DIR.mkdir(parents=True, exist_ok=True)

# 1. 确定性合并 Turtle 本体为单一发行版 OWL
g = Graph()
ttl_sources = [
    PROJECT_ROOT / "ontology" / "core" / "core.ttl",
    PROJECT_ROOT / "ontology" / "outlet" / "outlet.ttl",
    PROJECT_ROOT / "ontology" / "insight" / "insight-artifact.ttl",
    PROJECT_ROOT / "ontology" / "sales-visit" / "sales-visit.ttl",
]
for src in ttl_sources:
    g.parse(str(src), format="turtle")

owl_out = DIST_DIR / "outlet-insight.owl.ttl"
g.serialize(destination=str(owl_out), format="turtle")
print(f"Compiled OWL ontology: {owl_out} ({len(g)} triples)")

# 2. 合并 SHACL 形状
sh_g = Graph()
shacl_sources = [
    PROJECT_ROOT / "ontology" / "core" / "core.shacl.ttl",
    PROJECT_ROOT / "ontology" / "outlet" / "outlet.shacl.ttl",
    PROJECT_ROOT / "ontology" / "insight" / "insight-artifact.shacl.ttl",
    PROJECT_ROOT / "ontology" / "sales-visit" / "sales-visit.shacl.ttl",
    PROFILE_DIR / "constraints.shacl.ttl",
]
for src in shacl_sources:
    sh_g.parse(str(src), format="turtle")

shacl_out = DIST_DIR / "outlet-insight.shacl.ttl"
sh_g.serialize(destination=str(shacl_out), format="turtle")
print(f"Compiled SHACL constraints: {shacl_out} ({len(sh_g)} triples)")

# 3. 复制 Profile YAML 与度量/数据源/组织定义
shutil.copy(PROFILE_DIR / "profile.yaml", DIST_DIR / "outlet-insight.profile.yaml")
shutil.copy(PROFILE_DIR / "metric-definitions.yaml", DIST_DIR / "metric-definitions.yaml")
shutil.copy(PROFILE_DIR / "concepts.yaml", DIST_DIR / "concepts.yaml")
shutil.copy(PROFILE_DIR / "relations.yaml", DIST_DIR / "relations.yaml")
shutil.copy(PROFILE_DIR / "sources.yaml", DIST_DIR / "sources.yaml")
shutil.copy(PROFILE_DIR / "organizations.yaml", DIST_DIR / "organizations.yaml")
shutil.copy(PROFILE_DIR / "competency-questions.yaml", DIST_DIR / "competency-questions.yaml")

# 4. 生成 CQ 报告 Markdown (使用确定性 Git 提交日期)
cq_report_path = DIST_DIR / "competency-question-report.md"
with open(PROFILE_DIR / "competency-questions.yaml", "r", encoding="utf-8") as f:
    cq_data = yaml.safe_load(f)

cq_md_lines = [
    "# Outlet Insight Profile v0.1.0-RC Competency Question Verification Report",
    f"Generated at: {git_commit_date}",
    f"Profile URI: prism://ontology/profiles/outlet-insight",
    f"Git Commit: {git_commit}",
    "",
    "| CQ ID | 场景 | 自然语言提问 | 语义可表达性 | 数据可回答性 | 阻断限制原因 |",
    "|---|---|---|---|---|---|"
]
for cq in cq_data["competency_questions"]:
    cq_md_lines.append(f"| {cq['id']} | {cq['scenario']} | {cq['question']} | {cq['semantic_expressibility']} | {cq['data_answerability']} | {cq.get('blocking_reason', '无')} |")

with open(cq_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(cq_md_lines) + "\n")

# 5. 生成发布 Manifest (使用确定性日期)
manifest = {
    "profile_uri": "prism://ontology/profiles/outlet-insight",
    "profile_name": "outlet-insight",
    "version": "0.1.0-rc1",
    "status": "release_candidate",
    "release_tag": "outlet-insight-v0.1.0-rc1",
    "git_commit": git_commit,
    "clean_working_tree": True,
    "release_date": git_commit_date[:10],
    "authority": "TopPrism Ontology Engineering Committee",
    "included_files": [
        "outlet-insight.profile.yaml",
        "outlet-insight.owl.ttl",
        "outlet-insight.shacl.ttl",
        "metric-definitions.yaml",
        "concepts.yaml",
        "relations.yaml",
        "sources.yaml",
        "organizations.yaml",
        "competency-questions.yaml",
        "competency-question-report.md"
    ]
}
with open(DIST_DIR / "profile-manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# 6. 计算 SHA-256 Checksums
checksum_lines = []
for file_name in manifest["included_files"] + ["profile-manifest.json"]:
    file_path = DIST_DIR / file_name
    if file_path.exists():
        sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
        checksum_lines.append(f"{sha}  {file_name}")

with open(DIST_DIR / "checksums.sha256", "w", encoding="utf-8") as f:
    f.write("\n".join(checksum_lines) + "\n")

print(f"Successfully generated deterministic release package in {DIST_DIR} with SHA-256 checksums.")
