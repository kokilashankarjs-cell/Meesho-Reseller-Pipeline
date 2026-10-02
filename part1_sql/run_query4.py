import sqlite3
import csv

db_path = r"..\data\meesho_reseller.db"

conn = sqlite3.connect(db_path)

# Query 4A: Find resellers with no orders
query1 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

rows1 = conn.execute(query1).fetchall()

with open(r"output\zero_order_resellers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "region"])
    writer.writerows(rows1)

# Query 4B: COUNT(*) vs COUNT(order_id)
query2 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;
"""

rows2 = conn.execute(query2).fetchall()

with open(r"output\zero_order_count_check.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "count_star", "count_order_id"])
    writer.writerows(rows2)

conn.close()

print("Created Query 4 output files.")