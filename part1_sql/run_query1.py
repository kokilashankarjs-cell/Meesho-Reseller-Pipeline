import sqlite3
import csv

db_path = r"..\data\meesho_reseller.db"
output_path = r"output\monthly_category_revenue.csv"

conn = sqlite3.connect(db_path)

query = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;
"""

cursor = conn.execute(query)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(cursor.fetchall())

conn.close()

print("Created:", output_path)