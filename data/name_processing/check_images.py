import sqlite3
import os

# 检查图片文件名是否包含商品名称信息
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()

c.execute("""
    SELECT ecom_code, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    LIMIT 10
""")
pending_items = c.fetchall()
conn.close()

image_dir = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\images\amazon'
print(f"Checking images in: {image_dir}")

for ecom_code, platform, platform_id in pending_items:
    if platform == 'amazon':
        # 查找对应的图片文件
        expected_file = os.path.join(image_dir, f'amazon_{platform_id}.jpg')
        if os.path.exists(expected_file):
            print(f"Found image: {expected_file}")
        else:
            # 尝试其他扩展名
            for ext in ['.jpg', '.png', '.jpeg', '.webp']:
                test_file = os.path.join(image_dir, f'amazon_{platform_id}{ext}')
                if os.path.exists(test_file):
                    print(f"Found image with ext {ext}: {test_file}")
                    break
            else:
                print(f"No image for {ecom_code} (ASIN: {platform_id})")