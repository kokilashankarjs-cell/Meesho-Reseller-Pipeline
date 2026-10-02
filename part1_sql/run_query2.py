import sqlite3
import csv

db_path = r"..\data\meesho_reseller.db"
output_path = r"output\region_revenue.csv"

conn = sqlite3.connect(db_path)

query = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(o.order_id) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""

cursor = conn.execute(query)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "total_revenue", "n_orders"])
    writer.writerows(cursor.fetchall())

conn.close()

print("Created:", output_path)