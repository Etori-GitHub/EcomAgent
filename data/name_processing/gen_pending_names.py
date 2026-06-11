import sqlite3
import json

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 获取所有记录
cursor.execute("SELECT id, ecom_code, name, short_name FROM product_master")
rows = cursor.fetchall()

# 筛选需要重新翻译的记录
# 条件：short_name 以英文字母结尾（非中文字符结尾）
import re

def needs_retranslate(short_name, name):
    """判断是否需要重新翻译"""
    if not short_name or not name:
        return True
    
    # 以英文字母结尾的（可能是截断）
    if re.search(r'[a-zA-Z]$', short_name):
        return True
    
    # 包含英文字母但不是纯品牌名的情况（中英混杂）
    # 检查是否有英文单词被截断
    if re.search(r'\b[A-Za-z]{3,}\b', short_name) and re.search(r'[\u4e00-\u9fff]', short_name):
        # 有英文单词且混杂中文，可能是质量问题
        return True
    
    return False

pending_items = []
for row in rows:
    id_, ecom_code, name, short_name = row
    if needs_retranslate(short_name, name):
        pending_items.append({
            "id": ecom_code,
            "name": name
        })

print(f"需要重新翻译的商品数量: {len(pending_items)}")

# 保存到 pending_names.json
output = {
    "batch_id": "retranslate-20260609",
    "items": pending_items[:100]  # 先处理前100条测试
}

with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"已生成 pending_names.json，包含 {len(pending_items[:100])} 条记录")

conn.close()
