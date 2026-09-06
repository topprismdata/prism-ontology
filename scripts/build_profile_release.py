# -*- coding: utf-8 -*-
"""
build_profile_release.py
========================
确定性打包并发布 Outlet Insight Operational Profile v0.1.0-rc2
产出 dist/outlet-insight/0.1.0-rc2/ 包含 OWL 本体、SHACL 形状、度量定义、数据源、组织实体、Manifest 与 SHA-256 校验和。
具备完全的幂等性与可复现性（基于 Git Commit 状态）。
"""
import datetime
import hashlib
import json
import shutil
import subprocess
import yaml
from pathlib import Path
from rdflib import Graph

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = PROJECT_ROOT / "profiles" / "outlet-insight"

import os

# 固化签署发布日期与确定性构建时间戳
with open(PROFILE_DIR / "profile.yaml", "r", encoding="utf-8") as f:
    profile_data = yaml.safe_load(f)
profile_meta = profile_data.get("profile_metadata", {})
release_version = profile_meta.get("version", "0.1.0-rc4")
release_date = profile_meta.get("governance", {}).get("release_date", "2026-08-25")

DIST_DIR = PROJECT_ROOT / "dist" / "outlet-insight" / release_version

# 获取当前 Git Commit 与提交状态
try:
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    git_commit_date = subprocess.check_output(["git", "log", "-1", "--format=%cI"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    git_status = subprocess.check_output(["git", "status", "--porcelain"], cwd=PROJECT_ROOT).decode("utf-8").strip()
    status_lines = [l for l in git_status.splitlines() if not l.strip().endswith(f"dist/outlet-insight/{release_version}") and f"dist/outlet-insight/{release_version}" not in l]
    clean_tree = (len(status_lines) == 0)
except Exception:
    git_commit = "unversioned"
    git_commit_date = "2026-08-25T00:00:00Z"
    clean_tree = False

# 确定性时间戳：优先使用环境变量 SOURCE_DATE_EPOCH 或 Git Commit 提交日期，确保同一提交重构建哈希绝对可复现
build_timestamp = os.environ.get("SOURCE_DATE_EPOCH", git_commit_date if git_commit_date else datetime.datetime.now(datetime.timezone.utc).isoformat())

# 严格门禁 1：源内容完备提交检验 (Stage 1 clean tree requirement)
if not clean_tree:
    raise RuntimeError(
        f"Governance Release Gate Error: Working tree is dirty! "
        f"According to GOVERNANCE.md v0.2.0 §两阶段发行协议, Stage 1 commit must be completed before building dist.\n"
        f"Dirty files:\n" + "\n".join(status_lines)
    )

# 严格门禁 2：遵守 GOVERNANCE.md v0.2.0 发行不可变性铁律：已签署或已发布的发行目录严禁原地覆写
if DIST_DIR.exists() and any(DIST_DIR.iterdir()):
    raise RuntimeError(
        f"Governance Release Gate Error: Release directory {DIST_DIR} already exists and is non-empty! "
        f"According to GOVERNANCE.md v0.2.0 §发行条款, historical release candidates are immutable. "
        f"To release fixes or updates, please bump the version in profile.yaml first."
    )
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
shutil.copy(PROFILE_DIR / "field-mapping.yaml", DIST_DIR / "field-mapping.yaml")
shutil.copy(PROFILE_DIR / "prefix-map.json", DIST_DIR / "prefix-map.json")
shutil.copy(PROFILE_DIR / "context.jsonld", DIST_DIR / "context.jsonld")
shutil.copy(PROFILE_DIR / "competency-questions.yaml", DIST_DIR / "competency-questions.yaml")

# 4. 生成 CQ 报告 Markdown (使用确定性 Git 提交日期)
cq_report_path = DIST_DIR / "competency-question-report.md"
with open(PROFILE_DIR / "competency-questions.yaml", "r", encoding="utf-8") as f:
    cq_data = yaml.safe_load(f)

cq_md_lines = [
    f"# Outlet Insight Profile v{release_version} Competency Question Verification Report",
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
    "version": release_version,
    "status": "release_candidate",
    "release_tag": f"outlet-insight-v{release_version}",
    "git_commit": git_commit,
    "clean_working_tree": clean_tree,
    "release_date": release_date,
    "build_timestamp": build_timestamp,
    "authority": "TopPrism Ontology Engineering Committee",
    "included_files": [
        "outlet-insight.profile.yaml",
        "outlet-insight.owl.ttl",
        "outlet-insight.shacl.ttl",
        "metric-definitions.yaml",
        "concepts.yaml",
        "relations.yaml",
        "field-mapping.yaml",
        "prefix-map.json",
        "context.jsonld",
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
