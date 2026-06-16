#!/usr/bin/env python3
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / "data" / "amazon.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM products')
print(f'Total products in DB: {c.fetchone()[0]}')

c.execute('SELECT COUNT(*) FROM daily_sales')
print(f'Total daily_sales records: {c.fetchone()[0]}')

c.execute('SELECT COUNT(*) FROM daily_sales WHERE date = "2026-06-14"')
print(f'Today (2026-06-14) daily_sales records: {c.fetchone()[0]}')

conn.close()