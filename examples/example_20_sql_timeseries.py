"""
SQL with time-series data, using sqlite3 (built into Python - nothing to install).
Interview tip: know SELECT/WHERE/GROUP BY/HAVING/JOIN/ORDER BY, window functions,
indexes, primary/foreign keys, and ALWAYS use parameterised queries (?) not f-strings.
"""
import sqlite3
from datetime import datetime, timedelta
import math

conn = sqlite3.connect(":memory:")  # In-memory database, use a filename to save to disk
conn.row_factory = sqlite3.Row      # Rows behave like dicts: row["site_name"]
cur = conn.cursor()

# Relational modelling: two tables linked by a foreign key
cur.executescript("""
CREATE TABLE sites (
    site_id   INTEGER PRIMARY KEY,
    site_name TEXT NOT NULL,
    site_type TEXT NOT NULL            -- e.g. 'solar', 'office'
);

CREATE TABLE readings (
    site_id INTEGER NOT NULL REFERENCES sites(site_id),
    ts      TEXT    NOT NULL,          -- ISO 8601 timestamp, sorts correctly as text
    kwh     REAL,                      -- energy used/produced in that half hour
    PRIMARY KEY (site_id, ts)          -- one reading per site per timestamp
);

-- Index: makes "WHERE site_id = ? AND ts BETWEEN ? AND ?" fast (time-series pattern)
CREATE INDEX idx_readings_site_ts ON readings(site_id, ts);
""")

cur.executemany("INSERT INTO sites VALUES (?, ?, ?)", [
    (1, "Solar Farm", "solar"),
    (2, "Head Office", "office"),
])

# Generate 2 days of half-hourly readings (48 per day)
start = datetime(2026, 11, 1)
rows = []
for i in range(96):
    ts = start + timedelta(minutes=30 * i)
    hour = ts.hour + ts.minute / 60
    solar = max(0.0, 50 * math.sin(math.pi * (hour - 6) / 12))  # Daylight curve, 6am-6pm
    office = 20 + (30 if 8 <= hour < 18 else 0)                 # Busy during work hours
    rows.append((1, ts.isoformat(), round(solar, 2)))
    rows.append((2, ts.isoformat(), office))
rows[10] = (1, rows[10][1], None)  # A missing reading - real data always has gaps!

cur.executemany("INSERT INTO readings VALUES (?, ?, ?)", rows)  # Parameterised: safe from SQL injection
conn.commit()


def show(title, sql, params=()):
    print(f"\n--- {title}")
    for row in cur.execute(sql, params):
        print(dict(row))


# Aggregate per day with JOIN + GROUP BY
show("Total kWh per site per day", """
    SELECT s.site_name, DATE(r.ts) AS day, ROUND(SUM(r.kwh), 1) AS total_kwh
    FROM readings r
    JOIN sites s ON s.site_id = r.site_id
    GROUP BY s.site_name, day
    ORDER BY s.site_name, day
""")

# Filter on a time range with parameters
show("Office readings, 8am to 10am on day 1", """
    SELECT ts, kwh FROM readings
    WHERE site_id = ? AND ts >= ? AND ts < ?
    ORDER BY ts
""", (2, "2026-11-01T08:00:00", "2026-11-01T10:00:00"))

# Time bucketing: half-hourly -> hourly (downsampling)
show("Hourly totals for the solar farm, midday", """
    SELECT strftime('%Y-%m-%d %H:00', ts) AS hour, SUM(kwh) AS kwh
    FROM readings
    WHERE site_id = 1 AND ts LIKE '2026-11-01T1%'
    GROUP BY hour
    LIMIT 3
""")

# Peak demand: the single highest half hour per site
# (SQLite-specific shortcut: with MAX(), `ts` comes from the max row. In PostgreSQL use a window function)
show("Peak half hour per site", """
    SELECT site_id, ts, MAX(kwh) AS peak_kwh
    FROM readings
    GROUP BY site_id
""")

# HAVING filters AFTER grouping (WHERE filters before)
show("Days where the office used more than 1500 kWh", """
    SELECT DATE(ts) AS day, SUM(kwh) AS total
    FROM readings WHERE site_id = 2
    GROUP BY day
    HAVING total > 1500
""")

# Window functions: moving average and change from the previous reading
show("Solar: 3-reading moving average and change (LAG)", """
    SELECT ts, kwh,
        ROUND(AVG(kwh) OVER (PARTITION BY site_id ORDER BY ts
                             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg,
        ROUND(kwh - LAG(kwh) OVER (PARTITION BY site_id ORDER BY ts), 2) AS change
    FROM readings
    WHERE site_id = 1 AND ts BETWEEN '2026-11-01T07:00' AND '2026-11-01T09:00'
""")

# Finding data quality problems
show("Missing readings (NULL)", "SELECT site_id, ts FROM readings WHERE kwh IS NULL")

# EXPLAIN shows whether the index is used
show("Query plan", "EXPLAIN QUERY PLAN SELECT * FROM readings WHERE site_id = 1 AND ts > '2026-11-02'")

conn.close()
