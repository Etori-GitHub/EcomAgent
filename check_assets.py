import sqlite3
import json

conn = sqlite3.connect('data/assets.db')
conn.row_factory = sqlite3.Row

# 查看所有素材
cursor = conn.execute("SELECT * FROM sourcing_assets ORDER BY created_at DESC")
rows = cursor.fetchall()

print(f"Total assets: {len(rows)}")
print()

for row in rows:
    asset = dict(row)
    print(f"ID: {asset['id']}")
    print(f"  ecom_code: {asset['ecom_code']}")
    print(f"  asset_type: {asset['asset_type']}")
    print(f"  group_index: {asset['group_index']}")
    files = json.loads(asset['files']) if asset['files'] else []
    print(f"  files count: {len(files)}")
    print(f"  created_at: {asset['created_at']}")
    print()

conn.close()