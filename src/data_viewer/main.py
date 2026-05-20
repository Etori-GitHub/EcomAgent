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


@app.get("/api/categories")
async def get_categories(platform: Optional[str] = None):
    """获取分类列表"""
    categories = set()
    
    # Amazon 分类
    amazon_db = DATA_DIR / "amazon.db"
    if amazon_db.exists() and (platform is None or platform == "amazon"):
        conn = get_db_connection(amazon_db)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")
        for row in cursor.fetchall():
            if row[0]:
                categories.add(("amazon", row[0]))
        conn.close()
    
    # TikTok 分类
    tiktok_db = DATA_DIR / "tiktok.db"
    if tiktok_db.exists() and (platform is None or platform == "tiktok"):
        conn = get_db_connection(tiktok_db)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM tiktok_products WHERE category IS NOT NULL")
        for row in cursor.fetchall():
            if row[0]:
                categories.add(("tiktok", row[0]))
        conn.close()
    
    # 按平台分组
    result = {"amazon": [], "tiktok": [], "all": []}
    for p, c in categories:
        result[p].append(c)
        result["all"].append({"platform": p, "category": c})
    
    result["amazon"].sort()
    result["tiktok"].sort()
    
    return result


@app.get("/api/product-master")
async def get_product_master(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    platform: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="排序字段: price, rating, sales_count"),
    sort_order: Optional[str] = Query("desc", description="排序方向: asc, desc")
):
    """获取商品主库列表"""
    db_path = DATA_DIR / "product_master.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Product master database not found")

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 构建查询 - 不分页，先获取所有数据
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

    # 执行查询 - 获取所有数据
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
        product['sales_count'] = None
        product['last_updated_at'] = product.get('last_updated_at')

        if product['platform'] == 'amazon' and amazon_db_path.exists():
            try:
                amazon_conn = get_db_connection(amazon_db_path)
                amazon_cursor = amazon_conn.cursor()
                amazon_cursor.execute("""
                    SELECT ds.price, ds.rating, ds.date, ds.sales_count, p.local_image_path
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
                    product['sales_count'] = result['sales_count']
                    product['local_image_path'] = result['local_image_path']
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
                    SELECT ds.price, ds.rating, ds.date, ds.sales_count, p.local_image_path
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
                    product['sales_count'] = result['sales_count']
                    product['local_image_path'] = result['local_image_path']
                    if result['date']:
                        product['last_updated_at'] = result['date']
                tiktok_conn.close()
            except:
                pass
    
    # 排序
    if sort_by in ['price', 'rating', 'sales_count']:
        reverse = sort_order == 'desc'
        # 处理 None 值，排序时放到最后
        products.sort(
            key=lambda x: (x.get(sort_by) is None, x.get(sort_by) or 0),
            reverse=reverse
        )

    conn.close()

    # 分页 - 排序后再分页
    pages = (total + limit - 1) // limit
    offset = (page - 1) * limit
    paginated_products = products[offset:offset + limit]

    return {
        "data": paginated_products,
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
            p.category, p.subcategory, p.platform, p.image_url, p.local_image_path,
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
            p.category, p.platform, p.tiktokshop_id, p.image_url, p.local_image_path,
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


@app.get("/api/product-trend/{ecom_code}")
async def get_product_trend(
    ecom_code: str,
    days: int = Query(7, ge=1, le=90),
    start_date: Optional[str] = Query(None, description="自定义开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="自定义结束日期 YYYY-MM-DD"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """获取商品趋势数据（图表+详细表格）"""
    from datetime import timedelta
    
    master_db = DATA_DIR / "product_master.db"
    if not master_db.exists():
        raise HTTPException(status_code=404, detail="Product master database not found")
    
    conn = get_db_connection(master_db)
    cursor = conn.cursor()
    
    # 查询商品信息
    cursor.execute("SELECT * FROM product_master WHERE ecom_code = ?", (ecom_code,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = dict(row)
    platform = product['platform']
    product_id = product['id']
    
    # 计算日期范围
    if start_date and end_date:
        # 自定义时间区间
        query_start = start_date
        query_end = end_date
    else:
        # 快速选择
        query_end = datetime.now().strftime("%Y-%m-%d")
        query_start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    trend = []
    details = []
    total_records = 0
    
    if platform == 'amazon':
        amazon_db = DATA_DIR / "amazon.db"
        if amazon_db.exists():
            aconn = get_db_connection(amazon_db)
            acursor = aconn.cursor()
            
            # 查询平台产品ID
            acursor.execute("SELECT id, name, search_keyword FROM products WHERE master_id = ?", (product_id,))
            p_row = acursor.fetchone()
            if p_row:
                platform_product_id = p_row['id']
                platform_name = p_row['name']
                platform_keyword = p_row['search_keyword']
                
                # 获取趋势数据（图表用）
                acursor.execute("""
                    SELECT date, price, rating, rank, sales_count
                    FROM daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date ASC
                """, (platform_product_id, query_start, query_end))
                for r in acursor.fetchall():
                    trend.append(dict(r))
                
                # 获取详细数据总数
                acursor.execute("""
                    SELECT COUNT(*) FROM daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                """, (platform_product_id, query_start, query_end))
                total_records = acursor.fetchone()[0]
                
                # 获取详细数据（分页）
                offset = (page - 1) * limit
                acursor.execute("""
                    SELECT date, timestamp, price, rating, rank, sales_count
                    FROM daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date DESC
                    LIMIT ? OFFSET ?
                """, (platform_product_id, query_start, query_end, limit, offset))
                for r in acursor.fetchall():
                    record = dict(r)
                    record['short_name'] = product.get('short_name')
                    record['search_keyword'] = platform_keyword
                    record['events'] = ''  # 暂不支持事件
                    details.append(record)
            
            aconn.close()
    
    elif platform == 'tiktok':
        tiktok_db = DATA_DIR / "tiktok.db"
        if tiktok_db.exists():
            tconn = get_db_connection(tiktok_db)
            tcursor = tconn.cursor()
            
            # 查询平台产品ID
            tcursor.execute("SELECT id, name, search_keyword FROM tiktok_products WHERE master_id = ?", (product_id,))
            p_row = tcursor.fetchone()
            if p_row:
                platform_product_id = p_row['id']
                platform_name = p_row['name']
                platform_keyword = p_row['search_keyword']
                
                # 获取趋势数据（图表用）
                tcursor.execute("""
                    SELECT date, price, rating, sales_count
                    FROM tiktok_daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date ASC
                """, (platform_product_id, query_start, query_end))
                for r in tcursor.fetchall():
                    trend.append({
                        'date': r['date'],
                        'price': r['price'],
                        'rating': r['rating'],
                        'rank': None,
                        'sales_count': r['sales_count']
                    })
                
                # 获取详细数据总数
                tcursor.execute("""
                    SELECT COUNT(*) FROM tiktok_daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                """, (platform_product_id, query_start, query_end))
                total_records = tcursor.fetchone()[0]
                
                # 获取详细数据（分页）
                offset = (page - 1) * limit
                tcursor.execute("""
                    SELECT date, timestamp, price, rating, sales_count
                    FROM tiktok_daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date DESC
                    LIMIT ? OFFSET ?
                """, (platform_product_id, query_start, query_end, limit, offset))
                for r in tcursor.fetchall():
                    record = dict(r)
                    record['short_name'] = product.get('short_name')
                    record['search_keyword'] = platform_keyword
                    record['rank'] = None
                    record['events'] = ''  # 暂不支持事件
                    details.append(record)
            
            tconn.close()
    
    conn.close()
    
    pages = (total_records + limit - 1) // limit if total_records > 0 else 1
    
    return {
        "product": product,
        "trend": trend,
        "details": details,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_records,
            "pages": pages
        },
        "date_range": {
            "start": query_start,
            "end": query_end
        }
    }


@app.get("/api/sales-trend/{ecom_code}")
async def get_sales_trend_mini(ecom_code: str, days: int = Query(7, ge=1, le=30)):
    """获取商品销售趋势小图数据"""
    from datetime import timedelta
    
    master_db = DATA_DIR / "product_master.db"
    if not master_db.exists():
        raise HTTPException(status_code=404, detail="Product master database not found")
    
    conn = get_db_connection(master_db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, platform FROM product_master WHERE ecom_code = ?", (ecom_code,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    master_id = row['id']
    platform = row['platform']
    
    # 计算日期范围
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days-1)).strftime("%Y-%m-%d")
    
    trend = []
    
    if platform == 'amazon':
        amazon_db = DATA_DIR / "amazon.db"
        if amazon_db.exists():
            aconn = get_db_connection(amazon_db)
            acursor = aconn.cursor()
            acursor.execute("""
                SELECT p.id FROM products p WHERE p.master_id = ?
            """, (master_id,))
            p_row = acursor.fetchone()
            if p_row:
                acursor.execute("""
                    SELECT date, sales_count
                    FROM daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date ASC
                """, (p_row['id'], start_date, end_date))
                for r in acursor.fetchall():
                    trend.append({"date": r['date'], "value": r['sales_count']})
            aconn.close()
    
    elif platform == 'tiktok':
        tiktok_db = DATA_DIR / "tiktok.db"
        if tiktok_db.exists():
            tconn = get_db_connection(tiktok_db)
            tcursor = tconn.cursor()
            tcursor.execute("""
                SELECT p.id FROM tiktok_products p WHERE p.master_id = ?
            """, (master_id,))
            p_row = tcursor.fetchone()
            if p_row:
                tcursor.execute("""
                    SELECT date, sales_count
                    FROM tiktok_daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date ASC
                """, (p_row['id'], start_date, end_date))
                for r in tcursor.fetchall():
                    trend.append({"date": r['date'], "value": r['sales_count']})
            tconn.close()
    
    conn.close()
    return {"ecom_code": ecom_code, "trend": trend}


@app.get("/api/amazon/top-by-category")
async def get_amazon_top_by_category():
    """获取 Amazon 各分类 TOP 榜"""
    db_path = DATA_DIR / "amazon.db"
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Amazon database not found")

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 获取今天和昨天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    # 计算昨天的日期
    from datetime import timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # 获取所有分类
    cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]

    result = {}
    for category in categories:
        # 每个分类取 TOP 15，按 rank 排序
        cursor.execute("""
            SELECT
                p.id, p.asin, p.name, p.short_name, p.search_keyword, p.product_url,
                p.category, ds.price, ds.rating, ds.rank, ds.date
            FROM products p
            LEFT JOIN daily_sales ds ON p.id = ds.product_id
                AND ds.date = (SELECT MAX(date) FROM daily_sales WHERE product_id = p.id)
            WHERE p.category = ? AND ds.rank IS NOT NULL
            ORDER BY ds.rank ASC
            LIMIT 15
        """, (category,))
        rows = cursor.fetchall()
        
        products = []
        for row in rows:
            product = dict(row)
            # 查询昨天的排名
            cursor.execute("""
                SELECT rank FROM daily_sales 
                WHERE product_id = ? AND date = ?
            """, (product['id'], yesterday))
            yesterday_rank = cursor.fetchone()
            
            if yesterday_rank:
                product['rank_change'] = yesterday_rank['rank'] - product['rank']  # 正数=上升
                product['is_new'] = False
            else:
                # 检查是否有更早的数据
                cursor.execute("""
                    SELECT MIN(date) FROM daily_sales WHERE product_id = ?
                """, (product['id'],))
                first_date = cursor.fetchone()[0]
                product['is_new'] = first_date == today if first_date else True
                product['rank_change'] = None
            
            products.append(product)
        
        result[category] = products

    conn.close()
    return result

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
        # 每个分类取 TOP 10,按 rank 排序
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
async def get_tracked_products(ids: str = Query(..., description="商品编码列表,逗号分隔")):
    """获取追踪商品列表"""
    # 支持按 ecom_code 查询
    code_list = [x.strip() for x in ids.split(',') if x.strip()]
    if not code_list:
        return {"products": []}

    products = []
    master_db = DATA_DIR / "product_master.db"

    if master_db.exists():
        conn = get_db_connection(master_db)
        cursor = conn.cursor()

        placeholders = ','.join(['?' for _ in code_list])
        cursor.execute(f"""
            SELECT id, ecom_code, platform, name, short_name, product_url, category
            FROM product_master
            WHERE ecom_code IN ({placeholders})
        """, code_list)
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
                        SELECT ds.price, ds.rating, ds.date
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
                        product['last_updated_at'] = result['date']
                    aconn.close()

            elif product['platform'] == 'tiktok':
                tiktok_db = DATA_DIR / "tiktok.db"
                if tiktok_db.exists():
                    tconn = get_db_connection(tiktok_db)
                    tcursor = tconn.cursor()
                    tcursor.execute("""
                        SELECT ds.price, ds.rating, ds.date
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
                        product['last_updated_at'] = result['date']
                    tconn.close()

            products.append(product)

        conn.close()

    return {"products": products}


# ==================== 配置管理 API ====================

CONFIG_DIR = BASE_DIR / "config"
BACKUP_DIR = BASE_DIR / "config" / "backups"

# 确保备份目录存在
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/api/config/list")
async def list_configs():
    """列出所有配置文件"""
    configs = []

    for config_file in CONFIG_DIR.glob("*.json"):
        # 跳过模板文件
        if "template" in config_file.name:
            continue

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            import json
            data = json.loads(content)

            configs.append({
                "name": config_file.stem,
                "filename": config_file.name,
                "size": len(content),
                "modified": datetime.fromtimestamp(config_file.stat().st_mtime).isoformat(),
                "keys": list(data.keys()) if isinstance(data, dict) else []
            })
        except Exception as e:
            configs.append({
                "name": config_file.stem,
                "filename": config_file.name,
                "error": str(e)
            })

    return {"configs": configs}


@app.get("/api/config/{config_name}")
async def get_config(config_name: str):
    """获取单个配置文件内容"""
    # 安全检查,防止路径遍历
    if ".." in config_name or "/" in config_name or "\\" in config_name:
        raise HTTPException(status_code=400, detail="Invalid config name")

    config_path = CONFIG_DIR / f"{config_name}.json"

    if not config_path.exists():
        raise HTTPException(status_code=404, detail=f"Config file not found: {config_name}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()

        import json
        data = json.loads(content)

        return {
            "name": config_name,
            "filename": f"{config_name}.json",
            "content": content,
            "data": data,
            "modified": datetime.fromtimestamp(config_path.stat().st_mtime).isoformat()
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON parse error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/{config_name}")
async def update_config(config_name: str, request: dict):
    """更新配置文件"""
    import json
    import shutil

    # 安全检查
    if ".." in config_name or "/" in config_name or "\\" in config_name:
        raise HTTPException(status_code=400, detail="Invalid config name")

    config_path = CONFIG_DIR / f"{config_name}.json"

    if not config_path.exists():
        raise HTTPException(status_code=404, detail=f"Config file not found: {config_name}")

    # 获取新内容
    new_content = request.get("content")
    if not new_content:
        raise HTTPException(status_code=400, detail="Missing 'content' field")

    # 验证 JSON 格式
    try:
        data = json.loads(new_content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")

    # 创建备份
    backup_name = f"{config_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(config_path, backup_path)

    # 写入新内容
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "message": f"Config {config_name} updated successfully",
            "backup": backup_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/backups/list")
async def list_backups():
    """列出所有配置备份"""
    backups = []

    for backup_file in BACKUP_DIR.glob("*.json"):
        try:
            # 解析文件名: {config_name}_{YYYYMMDD_HHMMSS}.json
            parts = backup_file.stem.rsplit("_", 2)
            if len(parts) >= 3:
                config_name = parts[0]
                timestamp_str = f"{parts[1]}_{parts[2]}"
            else:
                config_name = backup_file.stem
                timestamp_str = ""

            backups.append({
                "filename": backup_file.name,
                "config_name": config_name,
                "timestamp": timestamp_str,
                "size": backup_file.stat().st_size,
                "created": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
            })
        except Exception:
            backups.append({
                "filename": backup_file.name,
                "error": "Failed to parse"
            })

    # 按时间倒序排列
    backups.sort(key=lambda x: x.get("created", ""), reverse=True)

    return {"backups": backups}


@app.get("/api/config/backups/{backup_filename}")
async def get_backup(backup_filename: str):
    """获取备份文件内容"""
    import json

    # 安全检查
    if ".." in backup_filename or "/" in backup_filename or "\\" in backup_filename:
        raise HTTPException(status_code=400, detail="Invalid backup filename")

    backup_path = BACKUP_DIR / backup_filename

    if not backup_path.exists():
        raise HTTPException(status_code=404, detail=f"Backup file not found: {backup_filename}")

    try:
        with open(backup_path, "r", encoding="utf-8") as f:
            content = f.read()

        data = json.loads(content)

        return {
            "filename": backup_filename,
            "content": content,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/config/backups/{backup_filename}/restore")
async def restore_backup(backup_filename: str):
    """还原备份文件"""
    import shutil

    # 安全检查
    if ".." in backup_filename or "/" in backup_filename or "\\" in backup_filename:
        raise HTTPException(status_code=400, detail="Invalid backup filename")

    backup_path = BACKUP_DIR / backup_filename

    if not backup_path.exists():
        raise HTTPException(status_code=404, detail=f"Backup file not found: {backup_filename}")

    # 解析目标配置文件名
    parts = backup_filename.rsplit("_", 2)
    if len(parts) >= 3:
        config_name = parts[0]
    else:
        raise HTTPException(status_code=400, detail="Invalid backup filename format")

    config_path = CONFIG_DIR / f"{config_name}.json"

    if not config_path.exists():
        raise HTTPException(status_code=404, detail=f"Target config file not found: {config_name}")

    try:
        # 创建当前配置的备份
        current_backup = f"{config_name}_pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy2(config_path, BACKUP_DIR / current_backup)

        # 还原备份
        shutil.copy2(backup_path, config_path)

        return {
            "success": True,
            "message": f"Backup {backup_filename} restored to {config_name}.json",
            "pre_restore_backup": current_backup
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/config/backups/{backup_filename}")
async def delete_backup(backup_filename: str):
    """删除备份文件"""
    # 安全检查
    if ".." in backup_filename or "/" in backup_filename or "\\" in backup_filename:
        raise HTTPException(status_code=400, detail="Invalid backup filename")

    backup_path = BACKUP_DIR / backup_filename

    if not backup_path.exists():
        raise HTTPException(status_code=404, detail=f"Backup file not found: {backup_filename}")

    try:
        backup_path.unlink()
        return {"success": True, "message": f"Backup {backup_filename} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/config/backup-all")
async def backup_all_configs():
    """备份所有配置文件"""
    import shutil

    backed_up = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for config_file in CONFIG_DIR.glob("*.json"):
        if "template" in config_file.name:
            continue

        backup_name = f"{config_file.stem}_{timestamp}.json"
        backup_path = BACKUP_DIR / backup_name
        shutil.copy2(config_file, backup_path)
        backed_up.append(backup_name)

    return {
        "success": True,
        "message": f"Backed up {len(backed_up)} config files",
        "backups": backed_up,
        "timestamp": timestamp
    }


# ==================== 服务启动 ====================

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务"""
    import uvicorn
    import sys
    import os

    # 挂载静态文件 - assets 目录
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    # 挂载静态文件 - 根目录(用于 index.html 等)
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    
    # 挂载图片目录 - 用于商品图片访问
    images_dir = DATA_DIR / "images"
    if images_dir.exists():
        app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

    print(f"\n{'='*60}")
    print(f"EcomAgent Data Viewer")
    print(f"{'='*60}")
    print(f"服务地址:http://{host}:{port}")
    print(f"API 文档:http://{host}:{port}/docs")
    print(f"{'='*60}\n")

    # Windows CMD 不支持 ANSI 颜色码,设置环境变量禁用颜色
    if sys.platform == "win32":
        os.environ["NO_COLOR"] = "1"
        # uvicorn 使用的 colorama 也需要禁用
        os.environ["COLORAMA_DISABLE"] = "1"

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        use_colors=False  # 明确禁用颜色
    )


if __name__ == "__main__":
    run_server()
