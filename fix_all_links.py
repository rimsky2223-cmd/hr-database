import os
import re
import urllib.parse

def clean_and_encode_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 尋找所有像 [xxx](yyy.md) 的語法
    # (針對可能帶有括號的 yyy 進行精準匹配)
    pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    
    def replace_match(match):
        alias = match.group(1)
        link_target = match.group(2) # 這裡會拿到 "公保跟公退(公教人員退撫基金).md"
        
        # 移除結尾的 .md 來做純檔名編碼
        if link_target.endswith('.md'):
            filename = link_target[:-3]
            # 把檔名部分的括號和中文全部強制轉成網址編碼
            encoded_filename = urllib.parse.quote(filename.strip())
            return f"[{alias}]({encoded_filename}.md)"
        return match.group(0)

    # 重複匹配確保沒有漏網之魚
    new_content = re.sub(pattern, replace_match, content)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# 掃描並修正所有的 .md 檔案（包含 index.md 與所有子頁面）
count = 0
for file in os.listdir('.'):
    if file.endswith('.md'):
        if clean_and_encode_links(file):
            count += 1

print(f"🎉 深度修復完成！共強制修正了 {count} 個 MD 檔案中的特殊括號連結。")
