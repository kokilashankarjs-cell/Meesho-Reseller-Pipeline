import sqlite3
import csv

db_path = r"..\data\meesho_reseller.db"
output_path = r"output\top5_resellers.csv"

conn = sqlite3.connect(db_path)

query = """
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

cursor = conn.execute(query)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "total_spend"])
    writer.writerows(cursor.fetchall())

conn.close()

print("Created:", output_path)