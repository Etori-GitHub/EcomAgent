import sqlite3

# 清空 Amazon 商品的 short_name
conn_amazon = sqlite3.connect('data/amazon.db')
cursor_amazon = conn_amazon.cursor()
cursor_amazon.execute('UPDATE products SET short_name = NULL')
conn_amazon.commit()
print(f"Amazon: 已清空 {cursor_amazon.rowcount} 个商品的简称")
conn_amazon.close()

# 清空 TikTok 商品的 short_name
conn_tiktok = sqlite3.connect('data/tiktok.db')
cursor_tiktok = conn_tiktok.cursor()
cursor_tiktok.execute('UPDATE tiktok_products SET short_name = NULL')
conn_tiktok.commit()
print(f"TikTok: 已清空 {cursor_tiktok.rowcount} 个商品的简称")
conn_tiktok.close()

print("\n清空完成，准备重新翻译")
