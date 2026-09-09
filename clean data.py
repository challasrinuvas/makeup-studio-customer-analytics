import pandas as pd

df = pd.read_csv("bookings.csv")

print("Before cleaning:", df.shape)
print(df.isnull().sum())

# Fix invalid prices
df = df[df["price"] > 0]

# Fill missing ratings with the service's average rating
df["rating"] = df.groupby("service")["rating"].transform(
    lambda x: x.fillna(x.mean())
)

# Convert date column
df["booking_date"] = pd.to_datetime(df["booking_date"])
df["month"] = df["booking_date"].dt.to_period("M").astype(str)

df.to_csv("bookings_clean.csv", index=False)
print("After cleaning:", df.shape)