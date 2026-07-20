import os
import re
import urllib.parse

def encode_markdown_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 標準 Markdown 連結 [text](target.md)
    # 排除已經是 http 或 https 的外部連結
    pattern = r'\[([^\]]+)\]\((?!http)([^)]+)\.md\)'
    
    def replace_match(match):
        alias = match.group(1)
        target = match.group(2)
        # 對檔名部分進行網址編碼，確保括號、中文、空格不會斷掉
        encoded_target = urllib.parse.quote(target.strip())
        return f"[{alias}]({encoded_target}.md)"

    new_content = re.sub(pattern, replace_match, content)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# 掃描根目錄下所有的 md 檔案進行修正
updated_count = 0
for file in os.listdir('.'):
    if file.endswith('.md'):
        if encode_markdown_links(file):
            updated_count += 1

print(f"🎉 網址編碼最佳化完成！共修正了 {updated_count} 個檔案的內部連結。")
