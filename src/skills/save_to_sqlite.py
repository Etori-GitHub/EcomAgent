import sqlite3
import json
from datetime import datetime

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "amazon.db")

def init_database():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        sales INTEGER,
        price REAL,
        platform TEXT DEFAULT 'amazon',
        url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales ON products(sales)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_platform ON products(platform)")
    
    conn.commit()
    conn.close()
    print(f"✓ 数据库初始化完成: {DB_PATH}")

def save_product(name, sales, price, platform="amazon", url=""):
    """保存单个商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 插入或更新
    cursor.execute("""
    INSERT INTO products (name, sales, price, platform, url)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(name) DO UPDATE SET
        sales = excluded.sales,
        price = excluded.price
    """, (name, sales, price, platform, url))
    
    conn.commit()
    conn.close()
    print(f"✓ 保存成功: {name}")

def save_products_batch(products):
    """批量保存商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for product in products:
        cursor.execute("""
        INSERT INTO products (name, sales, price, platform, url)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            sales = excluded.sales,
            price = excluded.price
        """, (
            product['name'],
            product['sales'],
            product['price'],
            product['platform'],
            product['url']
        ))
    
    conn.commit()
    conn.close()
    print(f"✓ 批量保存完成: {len(products)} 个商品")

def get_top_products(limit=10):
    """获取热销商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name, sales, price, platform, created_at
    FROM products
    ORDER BY sales DESC
    LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def main():
    """主函数"""
    # 初始化数据库
    init_database()
    
    # 示例数据（实际从网页抓取）
    products = [
        {
            'name': 'Owala FreeSip 保温不锈钢水瓶',
            'sales': 112690,
            'price': 206.05,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0BZYCJK89'
        },
        {
            'name': 'Etekcity 厨房电子秤',
            'sales': 144205,
            'price': 70.91,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0113UZJE2'
        },
        {
            'name': 'STANLEY Quencher H2.0 平底杯',
            'sales': 88037,
            'price': 299.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0CP9YB3Q4'
        }
    ]
    
    # 批量保存
    save_products_batch(products)
    
    # 查询热销商品
    print("\n=== 热销商品 Top 5 ===")
    top_products = get_top_products(5)
    for i, (name, sales, price, platform, created_at) in enumerate(top_products, 1):
        print(f"{i}. {name}")
        print(f"   销量: {sales:,} | 价格: CNY {price:.2f}")

if __name__ == "__main__":
    main()
