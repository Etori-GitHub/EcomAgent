import sqlite3
import json
from pathlib import Path

DATA_DIR = Path("data")
ASSETS_DIR = DATA_DIR / "assets"

# 连接数据库
assets_db = DATA_DIR / "assets.db"
conn = sqlite3.connect(str(assets_db))

# 查找视频文件
video_dir = ASSETS_DIR / "ECTK26000403" / "video" / "group_1"
files = []
for f in video_dir.iterdir():
    if f.suffix in [".mp4", ".png", ".jpg"]:
        files.append(str(f.relative_to(ASSETS_DIR.parent)))

print(f"Found {len(files)} files:")
for f in files:
    print(f"  {f}")

# 插入数据库
conn.execute("""
    INSERT INTO sourcing_assets (ecom_code, asset_type, group_index, files, params, task_id)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "ECTK26000403",
    "video",
    1,
    json.dumps(files),
    json.dumps({"ecom_code": "ECTK26000403", "group_index": 1}),
    "manual_insert"
))

conn.commit()
conn.close()

print("\n已写入数据库！")