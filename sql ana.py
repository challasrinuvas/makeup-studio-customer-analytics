import pandas as pd
import sqlite3

df = pd.read_csv("bookings_clean.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("bookings", conn, index=False, if_exists="replace")

query1 = """
SELECT service, COUNT(*) as total_bookings, ROUND(AVG(rating),2) as avg_rating
FROM bookings
GROUP BY service
ORDER BY total_bookings DESC;
"""
print(pd.read_sql(query1, conn))

query2 = """
SELECT ceremony_type, SUM(price) as total_revenue
FROM bookings
GROUP BY ceremony_type
ORDER BY total_revenue DESC;
"""
print(pd.read_sql(query2, conn))

conn.close()