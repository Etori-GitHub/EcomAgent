"""
更新 product_master 表的 short_name 字段
从 translated 文件夹读取翻译好的 JSON 文件，同步到 product_master.db
"""

import json
import sqlite3
from pathlib import Path

# 路径配置
TRANSLATED_DIR = Path("data/name_processing/translated")
DATA_DIR = Path("data")

def get_tiktokshop_id_from_id(tiktok_id: str) -> str:
    """从 tiktok_products 表的 id 查找 tiktokshop_id"""
    db_path = DATA_DIR / "tiktok.db"
    if not db_path.exists():
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT tiktokshop_id FROM tiktok_products WHERE id = ?", (tiktok_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    finally:
        conn.close()

def update_product_master(platform: str, product_id: str, short_name: str) -> bool:
    """更新 product_master 表的 short_name"""
    db_path = DATA_DIR / "product_master.db"
    if not db_path.exists():
        print(f"  [ERROR] 数据库不存在: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 根据平台确定 platform_id 的值
        if platform == "amazon":
            platform_id_value = product_id  # product_id 就是 ASIN
        elif platform == "tiktok":
            # product_id 是 tiktok_products 表的自增 id
            # 需要先查 tiktokshop_id
            platform_id_value = get_tiktokshop_id_from_id(product_id)
            if not platform_id_value:
                print(f"  [WARN] TikTok 商品 ID 不存在: {product_id}")
                return False
        else:
            print(f"  [WARN] 未知平台: {platform}")
            return False
        
        # 检查记录是否存在
        cursor.execute(
            "SELECT id FROM product_master WHERE platform = ? AND platform_id = ?",
            (platform, platform_id_value)
        )
        result = cursor.fetchone()
        
        if not result:
            print(f"  [WARN] 商品不存在: {platform}/{platform_id_value}")
            return False
        
        # 更新 short_name
        cursor.execute(
            "UPDATE product_master SET short_name = ? WHERE platform = ? AND platform_id = ?",
            (short_name, platform, platform_id_value)
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
    print("更新 product_master 表 short_name 字段")
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
            
            if update_product_master(platform, product_id, short_name):
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
