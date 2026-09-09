import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- STEP 1: Generate Data ----------
random.seed(42)
np.random.seed(42)

services = {
    "Bridal Makeup": 15000, "Party & Event": 5000, "HD & Airbrush": 8000,
    "Mehndi/Sangeet Look": 6000, "Engagement Glam": 7000, "Pre-Wedding Shoot": 9000
}
ceremony_types = ["Telugu Hindu Wedding", "Muslim Wedding", "Christian Wedding",
                   "North Indian Wedding", "Fusion/Other"]

rows = []
start_date = datetime(2024, 1, 1)
for i in range(400):
    service = random.choice(list(services.keys()))
    price = services[service] + random.choice([0, 0, 500, 1000, -500])
    booking_date = start_date + timedelta(days=random.randint(0, 600))
    rating = min(5.0, max(3.0, round(np.random.normal(4.7, 0.3), 1)))
    rows.append({
        "booking_id": i + 1, "customer_name": f"Customer_{i+1}", "service": service,
        "ceremony_type": random.choice(ceremony_types), "price": price,
        "booking_date": booking_date.strftime("%Y-%m-%d"), "rating": rating,
        "city": random.choice(["Hyderabad", "Secunderabad", "Warangal", "Vijayawada"])
    })
df = pd.DataFrame(rows)
df.loc[5:8, "rating"] = np.nan
df.loc[10, "price"] = -100
print("Raw data generated:", df.shape)

# ---------- STEP 2: Clean Data ----------
df = df[df["price"] > 0]
df["rating"] = df.groupby("service")["rating"].transform(lambda x: x.fillna(x.mean()))
df["booking_date"] = pd.to_datetime(df["booking_date"])
df["month"] = df["booking_date"].dt.to_period("M").astype(str)
print("Cleaned data:", df.shape)

# ---------- STEP 3: EDA ----------
demand = df["service"].value_counts()
avg_rating = df.groupby("service")["rating"].mean().sort_values(ascending=False)
revenue = df.groupby("ceremony_type")["price"].sum().sort_values(ascending=False)
monthly_trend = df.groupby("month")["booking_id"].count()

print("\nService demand:\n", demand)
print("\nAverage rating per service:\n", avg_rating)
print("\nRevenue by ceremony type:\n", revenue)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(x=demand.values, y=demand.index, palette="flare", ax=axes[0])
axes[0].set_title("Service Demand")

monthly_trend.plot(kind="line", marker="o", color="goldenrod", ax=axes[1])
axes[1].set_title("Monthly Booking Trend")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("combined_charts.png")
plt.show()

# ---------- STEP 4: SQL ----------
conn = sqlite3.connect(":memory:")
df.to_sql("bookings", conn, index=False, if_exists="replace")

print("\nSQL - Bookings by service:")
print(pd.read_sql("""
    SELECT service, COUNT(*) as total_bookings, ROUND(AVG(rating),2) as avg_rating
    FROM bookings GROUP BY service ORDER BY total_bookings DESC
""", conn))

print("\nSQL - Revenue by ceremony type:")
print(pd.read_sql("""
    SELECT ceremony_type, SUM(price) as total_revenue
    FROM bookings GROUP BY ceremony_type ORDER BY total_revenue DESC
""", conn))

conn.close()