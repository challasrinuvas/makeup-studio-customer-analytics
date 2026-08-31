import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Makeup Studio Analytics", layout="wide")

df = pd.read_csv("bookings_clean.csv")
df["booking_date"] = pd.to_datetime(df["booking_date"])

st.title("💄 Raju Vadhuvu — Customer Analytics Dashboard")
st.caption("Bridal & event makeup studio, Hyderabad")

# ---- Filters ----
col1, col2 = st.columns(2)
service_filter = col1.multiselect("Filter by Service", df["service"].unique(), default=df["service"].unique())
ceremony_filter = col2.multiselect("Filter by Ceremony", df["ceremony_type"].unique(), default=df["ceremony_type"].unique())

filtered = df[df["service"].isin(service_filter) & df["ceremony_type"].isin(ceremony_filter)]

# ---- KPI cards ----
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Bookings", len(filtered))
k2.metric("Total Revenue", f"₹{filtered['price'].sum():,.0f}")
k3.metric("Avg Rating", f"{filtered['rating'].mean():.2f} ⭐")
k4.metric("Services Offered", filtered["service"].nunique())

st.divider()

# ---- Charts ----
c1, c2 = st.columns(2)

demand = filtered["service"].value_counts().reset_index()
demand.columns = ["service", "bookings"]
fig1 = px.bar(demand, x="bookings", y="service", orientation="h", title="Service Demand", color="bookings")
c1.plotly_chart(fig1, use_container_width=True)

revenue = filtered.groupby("ceremony_type")["price"].sum().reset_index()
fig2 = px.pie(revenue, values="price", names="ceremony_type", title="Revenue by Ceremony Type")
c2.plotly_chart(fig2, use_container_width=True)

monthly = filtered.groupby(filtered["booking_date"].dt.to_period("M").astype(str))["booking_id"].count().reset_index()
monthly.columns = ["month", "bookings"]
fig3 = px.line(monthly, x="month", y="bookings", markers=True, title="Monthly Booking Trend")
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.subheader("Raw Data")
st.dataframe(filtered, use_container_width=True)