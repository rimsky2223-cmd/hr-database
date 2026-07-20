#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遞迴掃描 repo 根目錄下所有子資料夾（含巢狀子資料夾）與 .md 檔案，
重新產生支援多層縮排的 _sidebar.md。
用法：把這支腳本放在 repo 根目錄下執行
    python3 gen_sidebar.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_FILES = {"_sidebar.md", "README.md", "index.md"}
EXCLUDE_DIRS = {".git", ".github", "node_modules", ".vercel"}

lines = []
lines.append("- [🏠 首頁](index.md)")
lines.append("- [README](README.md)")


def add_dir(dir_path, rel_path, depth):
    """遞迴處理資料夾：depth 決定縮排層級（每層 2 個空白）"""
    indent = "  " * depth
    entries = sorted(os.listdir(dir_path))

    subdirs = [
        e for e in entries
        if os.path.isdir(os.path.join(dir_path, e)) and e not in EXCLUDE_DIRS
    ]
    md_files = [
        e for e in entries
        if e.lower().endswith(".md") and os.path.isfile(os.path.join(dir_path, e))
    ]

    for f in md_files:
        title = os.path.splitext(f)[0]
        link = f"{rel_path}/{f}" if rel_path else f
        lines.append(f"{indent}- [{title}]({link})")

    for d in subdirs:
        lines.append(f"{indent}- {d}")
        add_dir(
            os.path.join(dir_path, d),
            f"{rel_path}/{d}" if rel_path else d,
            depth + 1,
        )


top_level_dirs = sorted(
    d for d in os.listdir(ROOT)
    if os.path.isdir(os.path.join(ROOT, d)) and d not in EXCLUDE_DIRS
)

for folder in top_level_dirs:
    lines.append(f"- {folder}")
    add_dir(os.path.join(ROOT, folder), folder, 1)

root_md_files = sorted(
    f for f in os.listdir(ROOT)
    if f.lower().endswith(".md") and f not in EXCLUDE_FILES
)
for f in root_md_files:
    title = os.path.splitext(f)[0]
    lines.append(f"- [{title}]({f})")

output = "\n".join(lines) + "\n"

with open(os.path.join(ROOT, "_sidebar.md"), "w", encoding="utf-8") as fp:
    fp.write(output)

print(f"已產生 _sidebar.md，共 {len(lines)} 行。")
