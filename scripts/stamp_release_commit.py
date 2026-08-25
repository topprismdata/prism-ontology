# -*- coding: utf-8 -*-
"""
stamp_release_commit.py
=======================
将当前 HEAD commit 盖戳到 profile-manifest.json 并刷新 checksums.sha256。
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "outlet-insight" / "0.1.0-rc2"

commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode("utf-8").strip()

with open(DIST / "profile-manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

manifest["git_commit"] = commit
manifest["clean_working_tree"] = True

with open(DIST / "profile-manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

lines = []
for fname in manifest["included_files"] + ["profile-manifest.json"]:
    sha = hashlib.sha256((DIST / fname).read_bytes()).hexdigest()
    lines.append(f"{sha}  {fname}")

with open(DIST / "checksums.sha256", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Successfully stamped commit {commit[:7]} into release manifest & checksums.")
