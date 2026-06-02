"""
EcomAgent Data Viewer - FastAPI 服务
"""

# -*- coding: utf-8 -*-
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, Response
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


# 自定义 JSON 响应,确保 UTF-8
class UnicodeJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


# 创建 FastAPI 应用(使用自定义响应类)
app.default_response_class = UnicodeJSONResponse


app.default_response_class = UnicodeJSONResponse


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
        try:
            conn = get_db_connection(amazon_db)
            cursor = conn.cursor()

            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM products")
                stats["amazon"]["products"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM daily_sales")
                stats["amazon"]["sales"] = cursor.fetchone()[0]

                cursor.execute("SELECT MAX(date) FROM daily_sales")
                result = cursor.fetchone()[0]
                stats["amazon"]["last_updated"] = result

                cursor.execute("SELECT COUNT(*) FROM daily_sales WHERE date = ?", (today,))
                stats["amazon"]["today"] = cursor.fetchone()[0]

            conn.close()
        except Exception as e:
            print(f"[ERROR] Amazon stats: {e}")

    # TikTok 统计
    tiktok_db = DATA_DIR / "tiktok.db"
    if tiktok_db.exists():
        try:
            conn = get_db_connection(tiktok_db)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tiktok_products'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM tiktok_products")
                stats["tiktok"]["products"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales")
                stats["tiktok"]["sales"] = cursor.fetchone()[0]

                cursor.execute("SELECT MAX(date) FROM tiktok_daily_sales")
                result = cursor.fetchone()[0]
                stats["tiktok"]["last_updated"] = result

                cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales WHERE date = ?", (today,))
                stats["tiktok"]["today"] = cursor.fetchone()[0]

            conn.close()
        except Exception as e:
            print(f"[ERROR] TikTok stats: {e}")

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
async def get_categories_api(platform: Optional[str] = None):
    """获取分类列表(优先从 categories.db，回退到 product_master.db)"""
    result = {"amazon": [], "tiktok": [], "all": []}

    # 先从 categories.db 获取
    conn = get_categories_db()
    cursor = conn.cursor()

    amazon_cats = []
    tiktok_cats = []

    cursor.execute("SELECT platform, name FROM categories WHERE platform = 'amazon' AND enabled = 1")
    amazon_cats = [row[1] for row in cursor.fetchall()]

    cursor.execute("SELECT platform, name FROM categories WHERE platform = 'tiktok' AND enabled = 1")
    tiktok_cats = [row[1] for row in cursor.fetchall()]
    conn.close()

    # 如果某个平台在 categories.db 为空，回退到 product_master.db
    master_db = DATA_DIR / "product_master.db"
    if master_db.exists():
        conn = get_db_connection(master_db)
        cursor = conn.cursor()

        if not amazon_cats:
            cursor.execute("SELECT DISTINCT category FROM product_master WHERE platform = 'amazon' AND category IS NOT NULL ORDER BY category")
            amazon_cats = [row[0] for row in cursor.fetchall()]

        if not tiktok_cats:
            cursor.execute("SELECT DISTINCT category FROM product_master WHERE platform = 'tiktok' AND category IS NOT NULL ORDER BY category")
            tiktok_cats = [row[0] for row in cursor.fetchall()]

        conn.close()

    # 构建 all_list
    all_list = [{"platform": "amazon", "category": c} for c in amazon_cats] + \
               [{"platform": "tiktok", "category": c} for c in tiktok_cats]

    result["amazon"] = amazon_cats
    result["tiktok"] = tiktok_cats
    result["all"] = all_list

    # 如果指定了 platform，只返回该平台的分类
    if platform == "amazon":
        result["tiktok"] = []
        result["all"] = [{"platform": "amazon", "category": c} for c in amazon_cats]
    elif platform == "tiktok":
        result["amazon"] = []
        result["all"] = [{"platform": "tiktok", "category": c} for c in tiktok_cats]

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

    # 构建查询 - 不分页,先获取所有数据
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
                    SELECT ds.price, ds.rating, ds.date, ds.rank, p.local_image_path, p.image_url
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
                    product['sales_count'] = result['rank']  # Amazon 用 rank 代替
                    product['local_image_path'] = result['local_image_path']
                    product['image_url'] = result['image_url']
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
                    SELECT ds.price, ds.rating, ds.date, ds.sales_count, p.local_image_path, p.image_url
                    FROM tiktok_products p
                    LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
                        AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
                    WHERE p.master_id = ?
                    LIMIT 1
                """, (product['id'],))
                result = tiktok_cursor.fetchone()
                if result:
                    product['price'] = result[0]
                    product['rating'] = result[1]
                    product['sales_count'] = result[3]
                    product['local_image_path'] = result[4]
                    product['image_url'] = result[5]
                    if result[2]:
                        product['last_updated_at'] = result[2]
                tiktok_conn.close()
            except Exception as e:
                print(f"[ERROR] TikTok query failed for product {product['id']}: {e}")

    # 排序
    if sort_by in ['price', 'rating', 'sales_count', 'total_sales']:
        reverse = sort_order == 'desc'
        # 计算总销售额
        for p in products:
            price = p.get('price')
            sales = p.get('sales_count')
            if price is not None and sales is not None and price > 0 and sales > 0:
                p['total_sales'] = price * sales
            else:
                p['total_sales'] = 0
        
        # 排序时 None/0 值始终排最后
        def sort_key(x):
            val = x.get(sort_by)
            if val is None or val == 0:
                # 降序时用 -inf 确保排在最后，升序时用 inf 确保排在最后
                return float('-inf') if reverse else float('inf')
            return val
        
        products.sort(key=sort_key, reverse=reverse)
    else:
        print(f"[DEBUG] sort_by '{sort_by}' not in sort fields, skipping sort")

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
            p.id, p.asin, p.name, p.product_url,
            p.category, p.image_url,
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
            p.id, p.name, p.product_url,
            p.category, p.tiktokshop_id, p.image_url,
            ds.price, ds.rating, ds.sales_count, ds.date
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
    """获取商品趋势数据(图表+详细表格)"""
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

                # 获取趋势数据(图表用)
                acursor.execute("""
                    SELECT date, price, rating, rank
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

                # 获取详细数据(分页)
                offset = (page - 1) * limit
                acursor.execute("""
                    SELECT date, timestamp, price, rating, rank
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

                # 获取趋势数据(图表用)
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

                # 获取详细数据(分页)
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
                # Amazon daily_sales 没有 sales_count，用 rank 代替
                acursor.execute("""
                    SELECT date, rank
                    FROM daily_sales
                    WHERE product_id = ? AND date >= ? AND date <= ?
                    ORDER BY date ASC
                """, (p_row['id'], start_date, end_date))
                for r in acursor.fetchall():
                    trend.append({"date": r['date'], "value": r['rank']})
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
        # 每个分类取 TOP 15,按 rank 排序
        cursor.execute("""
            SELECT
                p.id, p.asin, p.name, p.product_url,
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
        # 每个分类取 TOP 10,按销量排序
        cursor.execute("""
            SELECT
                p.id, p.name, p.product_url,
                p.category, p.tiktokshop_id, ds.price, ds.rating, ds.sales_count
            FROM tiktok_products p
            LEFT JOIN tiktok_daily_sales ds ON p.id = ds.product_id
                AND ds.date = (SELECT MAX(date) FROM tiktok_daily_sales WHERE product_id = p.id)
            WHERE p.category = ?
            ORDER BY ds.sales_count DESC
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


# ==================== 1688 搜索 URL API ====================

@app.get("/api/1688-search-url")
async def get_1688_search_url(keyword: str = Query(..., description="搜索关键词")):
    """生成 1688 搜索 URL(GBK 编码)"""
    import urllib.parse

    # 将关键词编码为 GBK,然后转为 URL 编码
    gbk_encoded = keyword.encode('gbk')
    encoded_keyword = urllib.parse.quote(gbk_encoded, safe='')

    url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_keyword}"
    return {"url": url, "keyword": keyword}


# ==================== 类目管理 API ====================

CATEGORIES_DB = DATA_DIR / "categories.db"
DAILY_DB = DATA_DIR / "category_daily.db"
TASKS_DB = DATA_DIR / "tasks.db"
TASKS_DIR = BASE_DIR / "output" / "tasks"

from datetime import date

def get_categories_db():
    """获取类目数据库连接"""
    conn = sqlite3.connect(CATEGORIES_DB)
    conn.row_factory = sqlite3.Row
    return conn

def get_daily_db():
    """获取每日记录数据库连接"""
    conn = sqlite3.connect(DAILY_DB)
    conn.row_factory = sqlite3.Row
    return conn

def get_tasks_db():
    """获取任务数据库连接"""
    conn = sqlite3.connect(TASKS_DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/categories/{platform}")
async def get_categories(platform: str):
    """获取平台的类目列表"""
    if platform not in ['amazon', 'tiktok']:
        raise HTTPException(status_code=400, detail="Invalid platform")

    conn = get_categories_db()
    cursor = conn.cursor()

    # 获取类目列表
    cursor.execute('''
        SELECT id, name, url, enabled, added_at, last_scraped_at,
               last_products_count, total_scrapes, total_products
        FROM categories
        WHERE platform = ?
        ORDER BY name
    ''', (platform,))

    categories = []
    today = date.today().isoformat()

    for row in cursor.fetchall():
        cat = dict(row)

        # 查询今日抓取记录
        daily_conn = get_daily_db()
        daily_cursor = daily_conn.cursor()
        daily_cursor.execute('''
            SELECT products_count, scraped_at
            FROM category_daily
            WHERE category_id = ? AND date = ?
        ''', (cat['id'], today))
        daily = daily_cursor.fetchone()
        daily_conn.close()

        if daily:
            cat['today_status'] = 'done'
            cat['today_count'] = daily['products_count']
            cat['today_time'] = daily['scraped_at']
        else:
            cat['today_status'] = 'pending'
            cat['today_count'] = None
            cat['today_time'] = None

        categories.append(cat)

    conn.close()

    return {
        "platform": platform,
        "categories": categories,
        "total": len(categories),
        "enabled": sum(1 for c in categories if c['enabled'])
    }

@app.post("/api/categories/{platform}/refresh")
async def refresh_categories(platform: str):
    """刷新类目列表(从平台重新获取)"""
    if platform not in ['amazon', 'tiktok']:
        raise HTTPException(status_code=400, detail="Invalid platform")

    import subprocess

    script_path = BASE_DIR / 'scripts' / 'extract_categories.py'

    print(f"[API] 开始刷新 {platform} 类目...")
    print(f"[API] 脚本路径: {script_path}")

    # 运行类目提取脚本 - 实时输出
    process = subprocess.Popen(
        ['python', str(script_path), platform],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=str(BASE_DIR),
        bufsize=1
    )

    # 实时打印输出
    output_lines = []
    for line in process.stdout:
        print(line, end='')
        output_lines.append(line)

    process.wait(timeout=300)

    output = ''.join(output_lines)

    if process.returncode == 0:
        return {
            "success": True,
            "message": "类目刷新成功",
            "output": output
        }
    else:
        return {
            "success": False,
            "message": output or "刷新失败"
        }

@app.put("/api/categories/{category_id}/enabled")
async def set_category_enabled(category_id: int, enabled: bool):
    """启用/禁用类目"""
    conn = get_categories_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE categories SET enabled = ? WHERE id = ?", (1 if enabled else 0, category_id))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    conn.commit()
    conn.close()

    return {"success": True, "id": category_id, "enabled": enabled}


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


# ==================== 货源采集 API ====================

SOURCING_DB_PATH = DATA_DIR / "sourcing.db"
SOURCING_IMAGE_DIR = DATA_DIR / "images" / "sourcing"

def download_sourcing_image(image_url: str, offer_id: str) -> str:
    """下载货源图片到本地"""
    import urllib.request
    import os

    # 确保目录存在
    SOURCING_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"1688_{offer_id}_{timestamp}.jpg"
    filepath = SOURCING_IMAGE_DIR / filename

    # 下载图片
    request = urllib.request.Request(
        image_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://s.1688.com/'
        }
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        with open(filepath, 'wb') as f:
            f.write(response.read())

    # 返回相对路径
    return f"sourcing/{filename}"

def get_sourcing_db():
    """获取货源数据库连接"""
    conn = sqlite3.connect(SOURCING_DB_PATH)
    conn.row_factory = sqlite3.Row

    # 创建表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sourcing_1688 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecom_code TEXT NOT NULL,
            offer_id TEXT NOT NULL,
            title TEXT,
            price REAL,
            min_order INTEGER DEFAULT 1,
            shop_name TEXT,
            shop_url TEXT,
            product_url TEXT,
            image_url TEXT,
            local_image_path TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(ecom_code, offer_id)
        )
    ''')

    # 迁移:添加 local_image_path 字段(如果不存在)
    try:
        conn.execute('ALTER TABLE sourcing_1688 ADD COLUMN local_image_path TEXT')
    except:
        pass  # 字段已存在

    conn.commit()
    return conn


@app.post("/api/sourcing")
async def add_sourcing(request: Request):
    """添加货源记录"""
    data = await request.json()

    ecom_code = data.get("ecom_code")
    offer_id = data.get("offerId")

    if not ecom_code or not offer_id:
        raise HTTPException(status_code=400, detail="缺少 ecom_code 或 offerId")

    # 下载图片到本地
    image_url = data.get("image", "")
    local_image_path = ""
    if image_url:
        try:
            local_image_path = download_sourcing_image(image_url, offer_id)
        except Exception as e:
            print(f"[Sourcing] 图片下载失败: {e}")

    conn = get_sourcing_db()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO sourcing_1688
            (ecom_code, offer_id, title, price, min_order, shop_name, shop_url, product_url, image_url, local_image_path, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ecom_code,
            offer_id,
            data.get("title", "")[:200],
            data.get("price", 0),
            data.get("minOrder", 1),
            data.get("shopName", "")[:100],
            data.get("shopUrl", ""),
            data.get("productUrl", ""),
            image_url,
            local_image_path,
            data.get("collected_at", datetime.now().isoformat())
        ))
        conn.commit()

        return {"success": True, "ecom_code": ecom_code, "offer_id": offer_id, "local_image": local_image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/api/sourcing/list")
async def list_sourcing(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    ecom_code: Optional[str] = None
):
    """获取货源列表(分页、搜索)"""
    conn = get_sourcing_db()
    try:
        # 构建查询
        base_query = "SELECT * FROM sourcing_1688 WHERE 1=1"
        count_query = "SELECT COUNT(*) FROM sourcing_1688 WHERE 1=1"
        params = []

        if search:
            base_query += " AND (title LIKE ? OR shop_name LIKE ? OR offer_id LIKE ? OR ecom_code LIKE ?)"
            count_query += " AND (title LIKE ? OR shop_name LIKE ? OR offer_id LIKE ? OR ecom_code LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])

        if ecom_code:
            base_query += " AND ecom_code = ?"
            count_query += " AND ecom_code = ?"
            params.append(ecom_code)

        # 获取总数
        cursor = conn.execute(count_query, params)
        total = cursor.fetchone()[0]

        # 分页
        offset = (page - 1) * limit
        base_query += " ORDER BY collected_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor = conn.execute(base_query, params)
        rows = cursor.fetchall()

        # 计算页数
        pages = (total + limit - 1) // limit if limit > 0 else 0

        return {
            "data": [dict(row) for row in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages
            }
        }
    finally:
        conn.close()


@app.get("/api/sourcing/stats")
async def get_sourcing_stats():
    """获取货源统计信息"""
    conn = get_sourcing_db()
    try:
        # 总数
        cursor = conn.execute("SELECT COUNT(*) FROM sourcing_1688")
        total = cursor.fetchone()[0]

        # 关联商品数
        cursor = conn.execute("SELECT COUNT(DISTINCT ecom_code) FROM sourcing_1688")
        products_linked = cursor.fetchone()[0]

        # 今日采集数
        cursor = conn.execute("SELECT COUNT(*) FROM sourcing_1688 WHERE date(collected_at) = date('now')")
        today_count = cursor.fetchone()[0]

        # 最后更新时间
        cursor = conn.execute("SELECT MAX(collected_at) FROM sourcing_1688")
        last_updated = cursor.fetchone()[0]

        return {
            "total": total,
            "products_linked": products_linked,
            "today_count": today_count,
            "last_updated": last_updated
        }
    finally:
        conn.close()


@app.get("/api/sourcing/{ecom_code}")
async def get_sourcing(ecom_code: str):
    """获取商品关联的货源列表"""
    conn = get_sourcing_db()
    try:
        cursor = conn.execute('''
            SELECT * FROM sourcing_1688
            WHERE ecom_code = ?
            ORDER BY collected_at DESC
        ''', (ecom_code,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.delete("/api/sourcing/{ecom_code}/{offer_id}")
async def delete_sourcing(ecom_code: str, offer_id: str):
    """删除货源记录"""
    conn = get_sourcing_db()
    try:
        conn.execute('''
            DELETE FROM sourcing_1688
            WHERE ecom_code = ? AND offer_id = ?
        ''', (ecom_code, offer_id))
        conn.commit()
        return {"success": True}
    finally:
        conn.close()


# ==================== 手动触发 API ====================

import subprocess
import threading

# 后台任务状态
task_status = {
    "amazon_fetch": {"running": False, "last_run": None, "message": ""},
    "tiktok_fetch": {"running": False, "last_run": None, "message": ""},
    "data_import": {"running": False, "last_run": None, "message": ""}
}

def run_script_async(script_path: str, task_name: str):
    """异步运行脚本"""
    global task_status
    task_status[task_name]["running"] = True
    task_status[task_name]["message"] = "正在执行..."

    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(BASE_DIR)
        )

        if result.returncode == 0:
            task_status[task_name]["message"] = "执行成功"
        else:
            task_status[task_name]["message"] = f"执行失败: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        task_status[task_name]["message"] = "执行超时"
    except Exception as e:
        task_status[task_name]["message"] = f"执行错误: {str(e)}"
    finally:
        task_status[task_name]["running"] = False
        task_status[task_name]["last_run"] = datetime.now().isoformat()


@app.post("/api/tasks/amazon-fetch")
async def trigger_amazon_fetch():
    """触发 Amazon 数据抓取"""
    global task_status

    if task_status["amazon_fetch"]["running"]:
        return {"success": False, "message": "Amazon 抓取任务正在运行中"}

    script_path = str(BASE_DIR / "skills" / "amazon-fetcher" / "src" / "fetch_amazon_all_categories.py")

    # 启动后台线程
    thread = threading.Thread(target=run_script_async, args=(script_path, "amazon_fetch"))
    thread.start()

    return {"success": True, "message": "Amazon 抓取任务已启动"}


@app.post("/api/tasks/tiktok-fetch")
async def trigger_tiktok_fetch():
    """触发 TikTok 数据抓取"""
    global task_status

    if task_status["tiktok_fetch"]["running"]:
        return {"success": False, "message": "TikTok 抓取任务正在运行中"}

    script_path = str(BASE_DIR / "skills" / "tiktok-fetcher" / "src" / "fetch_tiktok_categories.py")

    thread = threading.Thread(target=run_script_async, args=(script_path, "tiktok_fetch"))
    thread.start()

    return {"success": True, "message": "TikTok 抓取任务已启动"}


@app.post("/api/tasks/data-import")
async def trigger_data_import():
    """触发数据导入"""
    global task_status

    if task_status["data_import"]["running"]:
        return {"success": False, "message": "数据导入任务正在运行中"}

    script_path = str(BASE_DIR / "skills" / "db-importer" / "src" / "import_to_db.py")

    thread = threading.Thread(target=run_script_async, args=(script_path, "data_import"))
    thread.start()

    return {"success": True, "message": "数据导入任务已启动"}


@app.get("/api/tasks/status")
async def get_tasks_status():
    """获取任务状态"""
    return task_status


# ==================== 抓取任务 API ====================

import subprocess
import threading
import sys

# 抓取任务状态
fetch_tasks = {
    'amazon': {'status': 'idle', 'message': '', 'started_at': None},
    'tiktok': {'status': 'idle', 'message': '', 'started_at': None}
}

def run_fetch_task(platform: str):
    """后台运行抓取任务"""
    global fetch_tasks

    fetch_tasks[platform]['status'] = 'running'
    fetch_tasks[platform]['started_at'] = datetime.now().isoformat()
    fetch_tasks[platform]['message'] = '正在启动...'

    try:
        # 使用新的任务脚本
        script_path = BASE_DIR / 'scripts' / 'fetch_task.py'

        print(f"[API] 启动 {platform} 抓取任务...")
        print(f"[API] 脚本路径: {script_path}")

        # 实时输出 - 使用 unbuffered 模式
        process = subprocess.Popen(
            ['python', '-u', str(script_path), platform],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(BASE_DIR),
            encoding='utf-8',
            errors='replace'
        )

        # 实时打印输出
        for line in process.stdout:
            print(line, end='')
            sys.stdout.flush()  # 强制刷新

        process.wait(timeout=600)

        if process.returncode == 0:
            fetch_tasks[platform]['status'] = 'completed'
            fetch_tasks[platform]['message'] = '抓取完成'
            print(f"[API] {platform} 抓取完成")
        else:
            fetch_tasks[platform]['status'] = 'failed'
            fetch_tasks[platform]['message'] = '抓取失败'
            print(f"[API] {platform} 抓取失败")

    except subprocess.TimeoutExpired:
        fetch_tasks[platform]['status'] = 'failed'
        fetch_tasks[platform]['message'] = '抓取超时(10分钟)'
        print(f"[API] {platform} 抓取超时")
    except Exception as e:
        fetch_tasks[platform]['status'] = 'failed'
        fetch_tasks[platform]['message'] = str(e)
        print(f"[API] {platform} 抓取异常: {e}")

@app.post('/api/tasks/{platform}/fetch')
async def start_fetch(platform: str):
    """启动抓取任务"""
    if platform not in ['amazon', 'tiktok']:
        raise HTTPException(status_code=400, detail='Invalid platform')

    if fetch_tasks[platform]['status'] == 'running':
        return {'success': False, 'message': f'{platform} 抓取任务正在进行中'}

    # 后台启动抓取
    thread = threading.Thread(target=run_fetch_task, args=(platform,))
    thread.daemon = True
    thread.start()

    return {'success': True, 'message': f'{platform} 抓取任务已启动'}

@app.get('/api/tasks/{platform}/fetch/status')
async def get_fetch_status(platform: str):
    """获取抓取任务状态"""
    if platform not in ['amazon', 'tiktok']:
        raise HTTPException(status_code=400, detail='Invalid platform')

    return fetch_tasks[platform]


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


# ==================== 翻译日志 API ====================

@app.get('/api/translation-logs')
async def get_translation_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description='筛选状态: pending, running, completed, failed')
):
    """获取翻译日志列表"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 构建查询
    base_query = 'SELECT * FROM translation_logs'
    count_query = 'SELECT COUNT(*) FROM translation_logs'
    params = []
    
    if status:
        base_query += ' WHERE status = ?'
        count_query += ' WHERE status = ?'
        params.append(status)
    
    # 获取总数
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # 分页
    offset = (page - 1) * limit
    base_query += f' ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}'
    
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    logs = [dict(row) for row in rows]
    
    # 计算分页信息
    pages = (total + limit - 1) // limit
    
    conn.close()
    
    return {
        'data': logs,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': pages
        }
    }


@app.post('/api/translation-logs')
async def create_translation_log(
    batch_id: str = Query(..., description='批次ID'),
    total_count: int = Query(..., description='待翻译数量')
):
    """创建翻译日志记录"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO translation_logs (batch_id, status, total_count, started_at)
        VALUES (?, 'running', ?, ?)
    ''', (batch_id, total_count, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {'success': True, 'log_id': log_id, 'message': f'翻译日志已创建，批次: {batch_id}'}


@app.patch('/api/translation-logs/{log_id}')
async def update_translation_log(
    log_id: int,
    status: Optional[str] = Query(None, description='状态: pending, running, completed, failed'),
    success_count: Optional[int] = Query(None, description='成功数量'),
    failed_count: Optional[int] = Query(None, description='失败数量'),
    error_message: Optional[str] = Query(None, description='错误信息')
):
    """更新翻译日志状态"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 检查日志是否存在
    cursor.execute('SELECT id FROM translation_logs WHERE id = ?', (log_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail='Log not found')
    
    # 构建更新
    updates = []
    params = []
    
    if status:
        updates.append('status = ?')
        params.append(status)
        if status == 'completed' or status == 'failed':
            updates.append('completed_at = ?')
            params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    if success_count is not None:
        updates.append('success_count = ?')
        params.append(success_count)
    
    if failed_count is not None:
        updates.append('failed_count = ?')
        params.append(failed_count)
    
    if error_message:
        updates.append('error_message = ?')
        params.append(error_message)
    
    if updates:
        query = f"UPDATE translation_logs SET {', '.join(updates)} WHERE id = ?"
        params.append(log_id)
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    
    return {'success': True, 'message': f'翻译日志 {log_id} 已更新'}


@app.get('/api/translation-logs/stats')
async def get_translation_logs_stats():
    """获取翻译日志统计"""
    db_path = DATA_DIR / 'product_master.db'
    if not db_path.exists():
        raise HTTPException(status_code=404, detail='Database not found')
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 总任务数
    cursor.execute('SELECT COUNT(*) FROM translation_logs')
    total_tasks = cursor.fetchone()[0]
    
    # 各状态数量
    cursor.execute('SELECT status, COUNT(*) FROM translation_logs GROUP BY status')
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 总翻译数量
    cursor.execute('SELECT SUM(total_count) FROM translation_logs')
    total_count = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(success_count) FROM translation_logs WHERE status = "completed"')
    success_count = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(failed_count) FROM translation_logs WHERE status = "failed"')
    failed_count = cursor.fetchone()[0] or 0
    
    # 最近一次运行
    cursor.execute('SELECT * FROM translation_logs ORDER BY created_at DESC LIMIT 1')
    last_run = cursor.fetchone()
    last_run_data = dict(last_run) if last_run else None
    
    conn.close()
    
    return {
        'total_tasks': total_tasks,
        'status_counts': status_counts,
        'total_count': total_count,
        'success_count': success_count,
        'failed_count': failed_count,
        'last_run': last_run_data
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
    print(f"服务地址: http://127.0.0.1:{port}")
    print(f"API 文档: http://127.0.0.1:{port}/docs")
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
