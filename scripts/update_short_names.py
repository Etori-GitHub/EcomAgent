"""
更新数据库中的 short_name 字段
从 translated 文件夹读取翻译好的 JSON 文件，更新对应的数据库记录
"""

import json
import sqlite3
from pathlib import Path

# 路径配置
TRANSLATED_DIR = Path("data/name_processing/translated")
DATA_DIR = Path("data")

def get_db_path(platform: str) -> Path:
    """根据平台获取数据库路径"""
    return DATA_DIR / f"{platform}.db"

def get_table_info(platform: str) -> tuple:
    """根据平台获取表名和ID字段名"""
    if platform == "amazon":
        return "products", "asin"
    elif platform == "tiktok":
        # TikTok 翻译文件里的 id 对应数据库的自增主键 id
        return "tiktok_products", "id"
    else:
        return None, None

def update_short_name(platform: str, product_id: str, short_name: str) -> bool:
    """更新单个商品的 short_name"""
    db_path = get_db_path(platform)
    if not db_path.exists():
        print(f"  [WARN] 数据库不存在: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 根据平台获取表名和ID字段名
        table_name, id_field = get_table_info(platform)
        if not table_name:
            print(f"  [WARN] 未知平台: {platform}")
            return False
        
        # 检查记录是否存在
        cursor.execute(f"SELECT id FROM {table_name} WHERE {id_field} = ?", (product_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"  [WARN] 商品不存在: {platform}/{product_id}")
            return False
        
        # 更新 short_name
        cursor.execute(
            f"UPDATE {table_name} SET short_name = ? WHERE {id_field} = ?",
            (short_name, product_id)
        )
        conn.commit()
        return True
        
    except Exception as e:
        print(f"  [ERROR] 更新失败: {platform}/{product_id} - {e}")
        return False
    finally:
        conn.close()

def main():
    """主函数"""
    print("=" * 60)
    print("更新数据库 short_name 字段")
    print("=" * 60)
    
    # 统计
    total_files = 0
    total_records = 0
    success_count = 0
    fail_count = 0
    
    # 遍历所有 JSON 文件
    json_files = sorted(TRANSLATED_DIR.glob("batch_*.json"))
    
    for json_file in json_files:
        total_files += 1
        print(f"\n处理文件: {json_file.name}")
        
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        translations = data.get("translations", [])
        batch_success = 0
        batch_fail = 0
        
        for item in translations:
            total_records += 1
            platform = item.get("platform")
            product_id = item.get("id")
            short_name = item.get("short_name")
            
            if not all([platform, product_id, short_name]):
                print(f"  [WARN] 数据不完整: {item}")
                batch_fail += 1
                continue
            
            if update_short_name(platform, product_id, short_name):
                batch_success += 1
            else:
                batch_fail += 1
        
        success_count += batch_success
        fail_count += batch_fail
        print(f"  成功: {batch_success}, 失败: {batch_fail}")
    
    # 输出统计
    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"文件总数: {total_files}")
    print(f"记录总数: {total_records}")
    print(f"成功更新: {success_count}")
    print(f"更新失败: {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
