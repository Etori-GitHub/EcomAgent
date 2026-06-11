import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "product_master.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查 translation_status = 'pending' 的数量
cursor.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE translation_status = 'pending' AND name IS NOT NULL AND name != ''
""")
pending_count = cursor.fetchone()[0]
print(f"Pending translation (translation_status='pending'): {pending_count}")

# 检查没有 short_name 或 short_name 为空的数量
cursor.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') AND name IS NOT NULL AND name != ''
""")
no_short_name_count = cursor.fetchone()[0]
print(f"No short_name: {no_short_name_count}")

# 检查 short_name 是英文的数量
cursor.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE short_name IS NOT NULL AND short_name != ''
""")
has_short_name = cursor.fetchone()[0]
print(f"Has short_name: {has_short_name}")

# 查看一些样例
cursor.execute("""
    SELECT ecom_code, name, short_name, translation_status 
    FROM product_master 
    WHERE translation_status = 'pending' AND name IS NOT NULL AND name != ''
    LIMIT 5
""")
print("\nSample pending items:")
for row in cursor.fetchall():
    ecom_code, name, short_name, status = row
    print(f"  {ecom_code}: {name[:50]}... | short_name: {short_name} | status: {status}")

conn.close()
