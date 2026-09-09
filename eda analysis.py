import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("bookings_clean.csv")

# 1. Most demanded services
demand = df["service"].value_counts()
print("\nService demand:\n", demand)

# 2. Average rating per service
avg_rating = df.groupby("service")["rating"].mean().sort_values(ascending=False)
print("\nAverage rating per service:\n", avg_rating)

# 3. Revenue by ceremony type
revenue = df.groupby("ceremony_type")["price"].sum().sort_values(ascending=False)
print("\nRevenue by ceremony type:\n", revenue)

# 4. Monthly booking trend
monthly_trend = df.groupby("month")["booking_id"].count()

# --- Visualizations ---
plt.figure(figsize=(8,5))
sns.barplot(x=demand.values, y=demand.index, palette="flare")
plt.title("Service Demand")
plt.xlabel("Number of Bookings")
plt.tight_layout()
plt.savefig("service_demand.png")

plt.figure(figsize=(10,5))
monthly_trend.plot(kind="line", marker="o", color="goldenrod")
plt.title("Monthly Booking Trend")
plt.xlabel("Month")
plt.ylabel("Bookings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_trend.png")

plt.show()