import sqlite3

conn = sqlite3.connect('data/product_master.db')
c = conn.cursor()

# 清除 ECAM26000059 之后的所有简称（脚本翻译的）
c.execute('''
    UPDATE product_master 
    SET short_name = NULL 
    WHERE ecom_code >= 'ECAM26000059'
''')

affected = c.rowcount
conn.commit()
conn.close()

print(f"已清除 {affected} 个脚本翻译的简称")