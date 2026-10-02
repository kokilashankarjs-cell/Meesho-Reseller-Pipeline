import sqlite3
import csv

db_path = r"..\data\meesho_reseller.db"
output_path = r"output\june_delivered_aov.csv"

conn = sqlite3.connect(db_path)

query = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

cursor = conn.execute(query)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["june_delivered_aov"])
    writer.writerows(cursor.fetchall())

conn.close()

print("Created:", output_path)