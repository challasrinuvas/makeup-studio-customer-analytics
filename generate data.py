import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

services = {
    "Bridal Makeup": 15000,
    "Party & Event": 5000,
    "HD & Airbrush": 8000,
    "Mehndi/Sangeet Look": 6000,
    "Engagement Glam": 7000,
    "Pre-Wedding Shoot": 9000
}

ceremony_types = ["Telugu Hindu Wedding", "Muslim Wedding", "Christian Wedding","North Indian Wedding", "Fusion/Other"]

n = 400
start_date = datetime(2024, 1, 1)

rows = []
for i in range(n):
    service = random.choice(list(services.keys()))
    base_price = services[service]
    price = base_price + random.choice([0, 0, 500, 1000, -500])  # small variation
    booking_date = start_date + timedelta(days=random.randint(0, 600))
    rating = round(np.random.normal(4.7, 0.3), 1)
    rating = min(5.0, max(3.0, rating))
    rows.append({
        "booking_id": i + 1,
        "customer_name": f"Customer_{i+1}",
        "service": service,
        "ceremony_type": random.choice(ceremony_types),
        "price": price,
        "booking_date": booking_date.strftime("%Y-%m-%d"),
        "rating": rating,
        "city": random.choice(["Hyderabad", "Secunderabad", "Warangal", "Vijayawada"])
    })

df = pd.DataFrame(rows)
# introduce a few messy values on purpose, like real-world data
df.loc[5:8, "rating"] = np.nan
df.loc[10, "price"] = -100
df.to_csv("bookings.csv", index=False)
print("bookings.csv created:", df.shape)