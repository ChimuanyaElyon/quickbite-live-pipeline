import streamlit as st
import pandas as pd
import pyodbc
import time

SERVER   = "DESKTOP-DCENTG8"
DATABASE = "quickbite"

CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

st.set_page_config(page_title="QuickBite Live Dashboard", layout="wide")
st.title("🍔 QuickBite — Live Orders Dashboard")

placeholder = st.empty()

while True:
    conn = pyodbc.connect(CONN_STR)
    df = pd.read_sql("SELECT * FROM orders ORDER BY order_id DESC", conn)
    conn.close()

    with placeholder.container():

        # ── KPI CARDS ───────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Orders",    len(df))
        col2.metric("Total Revenue",   f"₦{df['total_price'].sum():,.0f}")
        col3.metric("Avg Order Value", f"₦{df['total_price'].mean():,.0f}")
        col4.metric("Branches Active", df['branch'].nunique())

        st.markdown("---")

        # ── ROW 2: CHARTS ────────────────────────────────────
        col5, col6 = st.columns(2)

        with col5:
            st.subheader("Revenue by Branch")
            branch_rev = df.groupby("branch")["total_price"].sum().sort_values()
            st.bar_chart(branch_rev)

        with col6:
            st.subheader("Orders by Payment Method")
            payment_counts = df["payment"].value_counts()
            st.bar_chart(payment_counts)

        st.markdown("---")

        # ── ROW 3: MORE CHARTS ───────────────────────────────
        col7, col8 = st.columns(2)

        with col7:
            st.subheader("Top Selling Items")
            top_items = df.groupby("item")["quantity"].sum().sort_values(ascending=False).head(5)
            st.bar_chart(top_items)

        with col8:
            st.subheader("Revenue Over Time")
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            rev_time = df.set_index("timestamp")["total_price"].resample("1min").sum()
            st.line_chart(rev_time)

        st.markdown("---")

        # ── LIVE ORDERS TABLE ────────────────────────────────
        st.subheader("🟢 Live Orders Feed")
        st.dataframe(df.head(20), use_container_width=True)

    time.sleep(15)