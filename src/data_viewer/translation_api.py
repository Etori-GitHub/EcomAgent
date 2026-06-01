

# ==================== 翻译状态 API ====================

@app.post('/api/products/{ecom_code}/reset-translation')
async def reset_translation(ecom_code: str):
    """重置商品翻译状态为待翻译"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 检查商品是否存在
    cursor.execute('SELECT id, short_name FROM product_master WHERE ecom_code = ?', (ecom_code,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail='Product not found')
    
    # 更新翻译状态为 pending
    cursor.execute(
        'UPDATE product_master SET translation_status = ? WHERE ecom_code = ?',
        ('pending', ecom_code)
    )
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': f'商品 {ecom_code} 翻译状态已重置为待翻译'}


@app.get('/api/products/pending-translation')
async def get_pending_translations(limit: int = Query(10, ge=1, le=100)):
    """获取待翻译的商品列表"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, ecom_code, name, short_name, platform, category
        FROM product_master
        WHERE translation_status = 'pending' AND name IS NOT NULL AND name != ''
        ORDER BY last_updated_at DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    products = [dict(row) for row in rows]
    conn.close()
    
    return {'products': products, 'count': len(products)}


@app.post('/api/products/{ecom_code}/set-translated')
async def set_translated(ecom_code: str, short_name: str = Query(..., description='翻译后的中文名称')):
    """设置商品翻译完成"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 检查商品是否存在
    cursor.execute('SELECT id FROM product_master WHERE ecom_code = ?', (ecom_code,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail='Product not found')
    
    # 更新翻译状态和 short_name
    cursor.execute(
        'UPDATE product_master SET translation_status = ?, short_name = ? WHERE ecom_code = ?',
        ('translated', short_name, ecom_code)
    )
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': f'商品 {ecom_code} 翻译已完成'}
