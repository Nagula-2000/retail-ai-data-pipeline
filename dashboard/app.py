"""Interactive retail analytics dashboard powered by cleaned ETL outputs."""
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")
st.title("Retail Sales Analytics")
st.caption("Portfolio demonstration using synthetic retail transactions")

file_path = Path("outputs/clean_sales.csv")
if not file_path.exists():
    st.warning("No processed data found. First run: python -m src.pipeline")
    st.stop()

sales = pd.read_csv(file_path, parse_dates=["date"])
if sales.empty:
    st.info("No valid sales records are available.")
    st.stop()

stores = sorted(sales["store_id"].dropna().unique().tolist())
products = sorted(sales["product"].dropna().unique().tolist())
selected_stores = st.sidebar.multiselect("Stores", stores, default=stores)
selected_products = st.sidebar.multiselect("Products", products, default=products)

filtered = sales[
    sales["store_id"].isin(selected_stores) & sales["product"].isin(selected_products)
].copy()

if filtered.empty:
    st.info("No transactions match the selected filters.")
    st.stop()

a, b, c = st.columns(3)
a.metric("Total revenue", f"${filtered['revenue'].sum():,.2f}")
b.metric("Transactions", f"{filtered['transaction_id'].nunique():,}")
c.metric("Units sold", f"{filtered['quantity'].sum():,.0f}")

st.subheader("Revenue over time")
daily = filtered.groupby("date", as_index=False)["revenue"].sum().set_index("date")
st.line_chart(daily)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by store")
    by_store = filtered.groupby("store_id")["revenue"].sum().sort_values(ascending=False)
    st.bar_chart(by_store)
with right:
    st.subheader("Revenue by product")
    by_product = filtered.groupby("product")["revenue"].sum().sort_values(ascending=False)
    st.bar_chart(by_product)

st.subheader("Transactions")
st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True)

rejected_path = Path("outputs/rejected_sales.csv")
if rejected_path.exists():
    rejected = pd.read_csv(rejected_path)
    st.caption(f"Data quality: {len(rejected)} rejected transactions (duplicates are removed separately).")
