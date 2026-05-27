"""
批量翻译商品名称为中文简称
使用 OpenClaw 配置的模型进行翻译
"""
import sqlite3
import json
import time
import requests
import os

# 配置
BATCH_SIZE = 20  # 每批翻译数量
MODEL = "astroncodingplan/astron-code-latest"  # 使用配置的模型
API_URL = "http://127.0.0.1:18789/v1/chat/completions"  # OpenClaw Gateway API

def translate_batch(items):
    """
    批量翻译商品名称
    items: [(id, name), ...]
    返回: [(id, short_name), ...]
    """
    if not items:
        return []
    
    # 构建翻译提示
    names_list = "\n".join([f"{i+1}. [{item[0]}] {item[1]}" for i, item in enumerate(items)])
    
    prompt = f"""请将以下商品名称翻译成简洁的中文简称。

## 翻译规则
1. 提取核心信息：品牌 + 产品类型 + 关键特性
2. 翻译成简洁的中文（不超过 15 字）
3. 知名品牌保留英文名（如 Apple、Samsung、Nike 等）
4. 型号用数字+代/版表示
5. 如果名称本身就是中文或已包含中文，适当精简即可

## 商品列表
{names_list}

## 输出格式
请严格按照以下 JSON 格式输出，不要添加任何其他内容：
```json
[
  {{"id": "商品ID", "short_name": "中文简称"}},
  ...
]
```

注意：
- 必须输出 JSON 数组
- 每个商品都要有翻译结果
- short_name 不超过 15 个中文字符"""

    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "你是一个专业的电商商品名称翻译助手，擅长将英文商品名称翻译成简洁的中文简称。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"API 错误: {response.status_code} - {response.text}")
            return []
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 提取 JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        translations = json.loads(content)
        return [(t["id"], t["short_name"]) for t in translations]
        
    except Exception as e:
        print(f"翻译出错: {e}")
        return []

def translate_amazon_products():
    """翻译 Amazon 商品"""
    conn = sqlite3.connect('data/amazon.db')
    cursor = conn.cursor()
    
    # 获取需要翻译的商品
    cursor.execute('SELECT asin, name FROM products WHERE short_name IS NULL OR short_name = ""')
    products = cursor.fetchall()
    
    print(f"Amazon: 需要翻译 {len(products)} 个商品")
    
    translated = 0
    failed = 0
    
    # 分批处理
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i:i+BATCH_SIZE]
        print(f"\n处理批次 {i//BATCH_SIZE + 1}/{(len(products)-1)//BATCH_SIZE + 1} ({len(batch)} 个商品)...")
        
        results = translate_batch(batch)
        
        if results:
            # 更新数据库
            for asin, short_name in results:
                try:
                    cursor.execute('UPDATE products SET short_name = ? WHERE asin = ?', (short_name, asin))
                    translated += 1
                except Exception as e:
                    print(f"  更新失败 [{asin}]: {e}")
                    failed += 1
            conn.commit()
            print(f"  成功翻译 {len(results)} 个")
        else:
            print(f"  批次翻译失败")
            failed += len(batch)
        
        # 避免请求过快
        time.sleep(1)
    
    conn.close()
    print(f"\nAmazon 翻译完成: 成功 {translated}, 失败 {failed}")
    return translated, failed

def translate_tiktok_products():
    """翻译 TikTok 商品"""
    conn = sqlite3.connect('data/tiktok.db')
    cursor = conn.cursor()
    
    # 获取需要翻译的商品
    cursor.execute('SELECT id, name FROM tiktok_products WHERE short_name IS NULL OR short_name = ""')
    products = cursor.fetchall()
    
    print(f"\nTikTok: 需要翻译 {len(products)} 个商品")
    
    translated = 0
    failed = 0
    
    # 分批处理
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i:i+BATCH_SIZE]
        print(f"\n处理批次 {i//BATCH_SIZE + 1}/{(len(products)-1)//BATCH_SIZE + 1} ({len(batch)} 个商品)...")
        
        results = translate_batch(batch)
        
        if results:
            # 更新数据库
            for product_id, short_name in results:
                try:
                    cursor.execute('UPDATE tiktok_products SET short_name = ? WHERE id = ?', (short_name, int(product_id)))
                    translated += 1
                except Exception as e:
                    print(f"  更新失败 [{product_id}]: {e}")
                    failed += 1
            conn.commit()
            print(f"  成功翻译 {len(results)} 个")
        else:
            print(f"  批次翻译失败")
            failed += len(batch)
        
        # 避免请求过快
        time.sleep(1)
    
    conn.close()
    print(f"\nTikTok 翻译完成: 成功 {translated}, 失败 {failed}")
    return translated, failed

if __name__ == "__main__":
    print("=" * 50)
    print("商品名称批量翻译")
    print("=" * 50)
    
    # 翻译 Amazon
    amazon_ok, amazon_fail = translate_amazon_products()
    
    # 翻译 TikTok
    tiktok_ok, tiktok_fail = translate_tiktok_products()
    
    print("\n" + "=" * 50)
    print("翻译完成统计")
    print("=" * 50)
    print(f"Amazon: 成功 {amazon_ok}, 失败 {amazon_fail}")
    print(f"TikTok: 成功 {tiktok_ok}, 失败 {tiktok_fail}")
    print(f"总计: 成功 {amazon_ok + tiktok_ok}, 失败 {amazon_fail + tiktok_fail}")
