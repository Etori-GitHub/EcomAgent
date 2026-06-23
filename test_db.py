import sqlite3
from pathlib import Path

OPENCLAW_STATE_DB = Path.home() / '.openclaw' / 'state' / 'openclaw.sqlite'
print(f'DB path: {OPENCLAW_STATE_DB}')
print(f'DB exists: {OPENCLAW_STATE_DB.exists()}')

if OPENCLAW_STATE_DB.exists():
    conn = sqlite3.connect(OPENCLAW_STATE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT job_id, name FROM cron_jobs WHERE name LIKE 'ecomagent%'")
    rows = cursor.fetchall()
    print(f'Found {len(rows)} ecomagent jobs:')
    for row in rows:
        print(f'  {row}')
    conn.close()
