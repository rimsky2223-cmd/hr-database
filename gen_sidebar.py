#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動掃描 repo 根目錄下的所有子資料夾與 .md 檔案，重新產生 _sidebar.md
用法：把這支腳本放在 repo 根目錄下執行
    python3 gen_sidebar.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# 不列入側邊欄的檔案/資料夾
EXCLUDE_FILES = {"_sidebar.md", "README.md", "index.md"}
EXCLUDE_DIRS = {".git", ".github", "node_modules", ".vercel"}

lines = []

# 固定放在最上面的首頁與 README
lines.append("- [🏠 首頁](index.md)")
lines.append("- [README](README.md)")

# 掃描根目錄下所有資料夾（略過檔案與排除清單）
top_level_dirs = sorted(
    d for d in os.listdir(ROOT)
    if os.path.isdir(os.path.join(ROOT, d)) and d not in EXCLUDE_DIRS
)

for folder in top_level_dirs:
    folder_path = os.path.join(ROOT, folder)
    md_files = sorted(
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".md")
    )
    if not md_files:
        continue
    lines.append(f"- {folder}")
    for f in md_files:
        title = os.path.splitext(f)[0]
        link = f"{folder}/{f}"
        lines.append(f"  - [{title}]({link})")

root_md_files = sorted(
    f for f in os.listdir(ROOT)
    if f.lower().endswith(".md") and f not in EXCLUDE_FILES
)
if root_md_files:
    for f in root_md_files:
        title = os.path.splitext(f)[0]
        lines.append(f"- [{title}]({f})")

output = "\n".join(lines) + "\n"

with open(os.path.join(ROOT, "_sidebar.md"), "w", encoding="utf-8") as fp:
    fp.write(output)

print("已產生 _sidebar.md，內容預覽：\n")
print(output)
