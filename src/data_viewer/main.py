"""
EcomAgent Data Viewer - FastAPI 服务
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "src" / "data_viewer" / "static"

# 创建 FastAPI 应用
app = FastAPI(
    title="EcomAgent Data Viewer API",
    description="电商数据抓取与分析平台 - 数据展示 API",
    version="0.1.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 数据模型 ====================

class StatsResponse(BaseModel):
    """数据概览响应"""
    amazon: Dict[str, Any]
    tiktok: Dict[str, Any]
    product_master: Dict[str, Any]


class ProductResponse(BaseModel):
    """产品响应"""
    id: int
    name: str
    short_name: Optional[str] = None
    search_keyword: Optional[str] = None
    platform: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    rank: Optional[int] = None
    sales_count: Optional[str] = None
    tiktokshop_id: Optional[str] = None
    product_url: Optional[str] = None
    created_at: Optional[str] = None


class PaginationResponse(BaseModel):
    """分页响应"""
    page: int
    limit: int
    total: int
    pages: int


# ==================== 数据库工具 ====================

def get_db_connection(db_path: Path):
    """获取数据库连接"""
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_stats() -> Dict[str, Any]:
    """获取数据概览"""
    stats = {
        "amazon": {"products": 0, "sales": 0, "last_updated": None, "today": 0},
        "tiktok": {"products": 0, "sales": 0, "last_updated": None, "today": 0},
        "product_master": {"total": 0, "amazon": 0, "tiktok": 0, "today": 0, "last_updated": None}
    }
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Amazon 统计
    amazon_db = DATA_DIR / "amazon.db"
    if amazon_db.exists():
        conn = get_db_connection(amazon_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM products")
        stats["amazon"]["products"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM daily_sales")
        stats["amazon"]["sales"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(timestamp) FROM daily_sales")
        result = cursor.fetchone()[0]
        stats["amazon"]["last_updated"] = result
        
        # 今日抓取数量
        cursor.execute("SELECT COUNT(*) FROM daily_sales WHERE date = ?", (today,))
        stats["amazon"]["today"] = cursor.fetchone()[0]
        
        conn.close()
    
    # TikTok 统计
    tiktok_db = DATA_DIR / "tiktok.db"
    if tiktok_db.exists():
        conn = get_db_connection(tiktok_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tiktok_products")
        stats["tiktok"]["products"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales")
        stats["tiktok"]["sales"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(timestamp) FROM tiktok_daily_sales")
        result = cursor.fetchone()[0]
        stats["tiktok"]["last_updated"] = result
        
        # 今日抓取数量
        cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales WHERE date = ?", (today,))
        stats["tiktok"]["today"] = cursor.fetchone()[0]
        
        conn.close()
    
    # 商品总库统计
    master_db = DATA_DIR / "product_master.db"
    if master_db.exists():
        conn = get_db_connection(master_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM product_master")
        stats["product_master"]["total"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_master WHERE platform = 'amazon'")
        stats["product_master"]["amazon"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_master WHERE platform = 'tiktok'")
        stats["product_master"]["tiktok"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_master WHERE date(first_seen_at) = ?", (today,))
        stats["product_master"]["today"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(last_updated_at) FROM product_master")
        stats["product_master"]["last_updated"] = cursor.fetchone()[0]
        
        conn.close()
    
    return stats


# ==================== API 端点 ====================

@app.get("/", response_class=HTMLResponse)
async def root():
    """首页 - 重定向到数据概览"""
    with open(STATIC_DIR / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats_endpoint():
    """获取数据概览"""
    stats = get_stats()
    return StatsResponse(**stats)


@app.get("/api/product-master")
async def get_product_master(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    platform: Optional[str] = None,
    category: Optional[str] = None
):
    """获取商品主库列表"""
    db_path = DATA_DIR / "product_master.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Product master database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询
    base_query = "SELECT * FROM product_master WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM product_master WHERE 1=1"
    params = []
    
    if search:
        base_query += " AND name LIKE ?"
        count_query += " AND name LIKE ?"
        params.append(f"%{search}%")
    
    if platform:
        base_query += " AND platform = ?"
        count_query += " AND platform = ?"
        params.append(platform)
    
    if category:
        base_query += " AND category LIKE ?"
        count_query += " AND category LIKE ?"
        params.append(f"%{category}%")
    
    # 分页
    offset = (page - 1) * limit
    base_query += f" ORDER BY id DESC LIMIT {limit} OFFSET {offset}"
    
    # 执行查询
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # 获取统计
    cursor.execute("SELECT COUNT(*) FROM product_master")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE platform = 'amazon'")
    amazon_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE platform = 'tiktok'")
    tiktok_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE date(first_seen_at) = date('now')")
    today_count = cursor.fetchone()[0]
    
    products = [dict(row) for row in rows]
    
    # 关联平台数据获取价格和评分
    amazon_db_path = DATA_DIR / "amazon.db"
    tiktok_db_path = DATA_DIR / "tiktok.db"
    
    for product in products:
        product['price'] = None
        product['rating'] = None
        product['last_updated_at'] = product.get('last_updated_at')
        
        if product['platform'] == 'amazon' and amazon_db_path.exists():
            try:
                amazon_conn = get_db_connection(amazon_db_path)
                amazon_cursor = amazon_conn.cursor()
                amazon_cursor.execute("""
                    SELECT ds.price, ds.rating, ds.date
                    FROM products p
                    LEFT JOIN daily_sales ds ON p.id = ds.product_id
                        AND ds.date = (SELECT MAX(date) FROM daily_sales WHERE product_id = p.id)
                    WHERE p.master_id = ?
                    LIMIT 1
                """, (product['id'],))
                result = amazon_cursor.fetchone()
                if result:
                    product['price'] = result['price']
                    product['rating'] = result['rating']
                    if result['date']:
                        product['last_updated_at'] = result['date']
                amazon_conn.close()
            except:
                pass
        
        elif product['platform'] == 'tiktok' and tiktok_db_path.exists():
            try:
                tiktok_conn = get_db_connection(tiktok_db_path)
                tiktok_cursor = tiktok_conn.cursor()
                tiktok_cursor.execute("""
                    SELECT ds.price, ds.rating, ds.date
                    FROM tiktok_products p
                    LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
                        AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
                    WHERE p.master_id = ?
                    LIMIT 1
                """, (product['id'],))
                result = tiktok_cursor.fetchone()
                if result:
                    product['price'] = result['price']
                    product['rating'] = result['rating']
                    if result['date']:
                        product['last_updated_at'] = result['date']
                tiktok_conn.close()
            except:
                pass
    
    conn.close()
    
    pages = (total + limit - 1) // limit
    
    return {
        "data": products,
        "stats": {
            "total": total_count,
            "amazon": amazon_count,
            "tiktok": tiktok_count,
            "today": today_count
        },
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@app.get("/api/amazon/products")
async def get_amazon_products(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """获取 Amazon 产品列表"""
    db_path = DATA_DIR / "amazon.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Amazon database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询 - JOIN daily_sales 获取最新价格和评分
    base_query = """
        SELECT 
            p.id, p.asin, p.name, p.short_name, p.search_keyword, p.product_url,
            p.category, p.subcategory, p.platform,
            ds.price, ds.rating, ds.rating_count, ds.rank, ds.date
        FROM products p
        LEFT JOIN daily_sales ds ON p.id = ds.product_id
            AND ds.date = (SELECT MAX(date) FROM daily_sales WHERE product_id = p.id)
        WHERE 1=1
    """
    count_query = "SELECT COUNT(*) FROM products WHERE 1=1"
    params = []
    
    if search:
        base_query += " AND p.name LIKE ?"
        count_query += " AND name LIKE ?"
        params.append(f"%{search}%")
    
    if category:
        base_query += " AND p.category = ?"
        count_query += " AND category = ?"
        params.append(category)
    
    # 分页
    offset = (page - 1) * limit
    base_query += f" ORDER BY p.id LIMIT {limit} OFFSET {offset}"
    
    # 执行查询
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # 转换为字典列表
    products = [dict(row) for row in rows]
    
    # 计算总页数
    pages = (total + limit - 1) // limit
    
    return {
        "data": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@app.get("/api/amazon/sales")
async def get_amazon_sales(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    date: Optional[str] = None,
    product_id: Optional[int] = None
):
    """获取 Amazon 销售记录"""
    db_path = DATA_DIR / "amazon.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Amazon database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询
    base_query = "SELECT * FROM daily_sales WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM daily_sales WHERE 1=1"
    params = []
    
    if date:
        base_query += " AND date = ?"
        count_query += " AND date = ?"
        params.append(date)
    
    if product_id:
        base_query += " AND product_id = ?"
        count_query += " AND product_id = ?"
        params.append(product_id)
    
    # 分页
    offset = (page - 1) * limit
    base_query += f" ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}"
    
    # 执行查询
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # 转换为字典列表
    sales = [dict(row) for row in rows]
    
    # 计算总页数
    pages = (total + limit - 1) // limit
    
    return {
        "data": sales,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@app.get("/api/tiktok/products")
async def get_tiktok_products(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """获取 TikTok 产品列表"""
    db_path = DATA_DIR / "tiktok.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="TikTok database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询 - JOIN daily_sales 获取最新价格和评分
    base_query = """
        SELECT 
            p.id, p.name, p.short_name, p.search_keyword, p.product_url,
            p.category, p.platform, p.tiktokshop_id,
            ds.price, ds.original_price, ds.rating, ds.sales_count, ds.date
        FROM tiktok_products p
        LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
            AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
        WHERE 1=1
    """
    count_query = "SELECT COUNT(*) FROM tiktok_products WHERE 1=1"
    params = []
    
    if search:
        base_query += " AND p.name LIKE ?"
        count_query += " AND name LIKE ?"
        params.append(f"%{search}%")
    
    if category:
        base_query += " AND p.category = ?"
        count_query += " AND category = ?"
        params.append(category)
    
    # 分页
    offset = (page - 1) * limit
    base_query += f" ORDER BY p.id LIMIT {limit} OFFSET {offset}"
    
    # 执行查询
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # 转换为字典列表
    products = [dict(row) for row in rows]
    
    # 计算总页数
    pages = (total + limit - 1) // limit
    
    return {
        "data": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@app.get("/api/tiktok/sales")
async def get_tiktok_sales(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    date: Optional[str] = None,
    product_id: Optional[int] = None
):
    """获取 TikTok 销售记录"""
    db_path = DATA_DIR / "tiktok.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="TikTok database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询
    base_query = "SELECT * FROM tiktok_daily_sales WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM tiktok_daily_sales WHERE 1=1"
    params = []
    
    if date:
        base_query += " AND date = ?"
        count_query += " AND date = ?"
        params.append(date)
    
    if product_id:
        base_query += " AND product_id = ?"
        count_query += " AND product_id = ?"
        params.append(product_id)
    
    # 分页
    offset = (page - 1) * limit
    base_query += f" ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}"
    
    # 执行查询
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # 转换为字典列表
    sales = [dict(row) for row in rows]
    
    # 计算总页数
    pages = (total + limit - 1) // limit
    
    return {
        "data": sales,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@app.get("/api/amazon/top-by-category")
async def get_amazon_top_by_category():
    """获取 Amazon 各分类 TOP 榜"""
    db_path = DATA_DIR / "amazon.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Amazon database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 获取所有分类
    cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]
    
    result = {}
    for category in categories:
        # 每个分类取 TOP 10，按 rank 排序
        cursor.execute("""
            SELECT 
                p.id, p.asin, p.name, p.short_name, p.search_keyword, p.product_url,
                p.category, ds.price, ds.rating, ds.rank
            FROM products p
            LEFT JOIN daily_sales ds ON p.id = ds.product_id
                AND ds.date = (SELECT MAX(date) FROM daily_sales WHERE product_id = p.id)
            WHERE p.category = ? AND ds.rank IS NOT NULL
            ORDER BY ds.rank ASC
            LIMIT 10
        """, (category,))
        rows = cursor.fetchall()
        result[category] = [dict(row) for row in rows]
    
    conn.close()
    return result


@app.get("/api/tiktok/top-by-category")
async def get_tiktok_top_by_category():
    """获取 TikTok 各分类 TOP 榜"""
    db_path = DATA_DIR / "tiktok.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="TikTok database not found")
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 获取所有分类
    cursor.execute("SELECT DISTINCT category FROM tiktok_products WHERE category IS NOT NULL ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]
    
    result = {}
    for category in categories:
        # 每个分类取 TOP 10，按 rank 排序
        cursor.execute("""
            SELECT 
                p.id, p.name, p.short_name, p.search_keyword, p.product_url,
                p.category, p.tiktokshop_id, p.rank, ds.price, ds.rating
            FROM tiktok_products p
            LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
                AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
            WHERE p.category = ?
            ORDER BY p.rank ASC
            LIMIT 10
        """, (category,))
        rows = cursor.fetchall()
        result[category] = [dict(row) for row in rows]
    
    conn.close()
    return result


@app.get("/api/product-trend")
async def get_product_trend(
    master_id: int = Query(..., description="商品主库ID"),
    platform: str = Query(..., description="平台: amazon/tiktok"),
    range: str = Query("30", description="时间范围: 7/30/90/all")
):
    """获取商品趋势数据"""
    records = []
    
    if platform == "amazon":
        db_path = DATA_DIR / "amazon.db"
        if not db_path.exists():
            return {"records": []}
        
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # 构建时间条件
        date_filter = ""
        if range == "7":
            date_filter = "AND date >= date('now', '-7 days')"
        elif range == "30":
            date_filter = "AND date >= date('now', '-30 days')"
        elif range == "90":
            date_filter = "AND date >= date('now', '-90 days')"
        
        cursor.execute(f"""
            SELECT date, price, rating, rank
            FROM daily_sales
            WHERE product_id = (SELECT id FROM products WHERE master_id = ? LIMIT 1)
            {date_filter}
            ORDER BY date ASC
        """, (master_id,))
        rows = cursor.fetchall()
        records = [dict(row) for row in rows]
        conn.close()
    
    elif platform == "tiktok":
        db_path = DATA_DIR / "tiktok.db"
        if not db_path.exists():
            return {"records": []}
        
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        date_filter = ""
        if range == "7":
            date_filter = "AND date >= date('now', '-7 days')"
        elif range == "30":
            date_filter = "AND date >= date('now', '-30 days')"
        elif range == "90":
            date_filter = "AND date >= date('now', '-90 days')"
        
        cursor.execute(f"""
            SELECT date, price, rating
            FROM tiktok_daily_sales
            WHERE product_id = (SELECT id FROM tiktok_products WHERE master_id = ? LIMIT 1)
            {date_filter}
            ORDER BY date ASC
        """, (master_id,))
        rows = cursor.fetchall()
        records = [dict(row) for row in rows]
        conn.close()
    
    return {"records": records}


@app.get("/api/tracked-products")
async def get_tracked_products(ids: str = Query(..., description="商品ID列表，逗号分隔")):
    """获取追踪商品列表"""
    id_list = [int(x) for x in ids.split(',') if x.strip().isdigit()]
    if not id_list:
        return {"products": []}
    
    products = []
    master_db = DATA_DIR / "product_master.db"
    
    if master_db.exists():
        conn = get_db_connection(master_db)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in id_list])
        cursor.execute(f"""
            SELECT id, ecom_code, platform, name, short_name, product_url
            FROM product_master
            WHERE id IN ({placeholders})
        """, id_list)
        rows = cursor.fetchall()
        
        for row in rows:
            product = dict(row)
            # 获取价格和评分
            if product['platform'] == 'amazon':
                amazon_db = DATA_DIR / "amazon.db"
                if amazon_db.exists():
                    aconn = get_db_connection(amazon_db)
                    acursor = aconn.cursor()
                    acursor.execute("""
                        SELECT ds.price, ds.rating
                        FROM products p
                        LEFT JOIN daily_sales ds ON p.id = ds.product_id
                            AND ds.date = (SELECT MAX(date) FROM daily_sales WHERE product_id = p.id)
                        WHERE p.master_id = ?
                        LIMIT 1
                    """, (product['id'],))
                    result = acursor.fetchone()
                    if result:
                        product['price'] = result['price']
                        product['rating'] = result['rating']
                    aconn.close()
            
            elif product['platform'] == 'tiktok':
                tiktok_db = DATA_DIR / "tiktok.db"
                if tiktok_db.exists():
                    tconn = get_db_connection(tiktok_db)
                    tcursor = tconn.cursor()
                    tcursor.execute("""
                        SELECT ds.price, ds.rating
                        FROM tiktok_products p
                        LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
                            AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
                        WHERE p.master_id = ?
                        LIMIT 1
                    """, (product['id'],))
                    result = tcursor.fetchone()
                    if result:
                        product['price'] = result['price']
                        product['rating'] = result['rating']
                    tconn.close()
            
            products.append(product)
        
        conn.close()
    
    return {"products": products}


# ==================== 服务启动 ====================

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务"""
    import uvicorn
    
    # 挂载静态文件
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    
    print(f"\n{'='*60}")
    print(f"EcomAgent Data Viewer")
    print(f"{'='*60}")
    print(f"服务地址：http://{host}:{port}")
    print(f"API 文档：http://{host}:{port}/docs")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run_server()
