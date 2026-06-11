import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "product_master.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看一些样例
cursor.execute("""
    SELECT ecom_code, name, short_name 
    FROM product_master 
    ORDER BY id ASC
    LIMIT 10
""")
print("Sample items:")
for row in cursor.fetchall():
    ecom_code, name, short_name = row
    print(f"  {ecom_code}: {name[:40]}... | short_name: {short_name}")

conn.close()
