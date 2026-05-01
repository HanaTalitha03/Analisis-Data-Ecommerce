import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")


all_df = pd.read_csv("main_data.csv")


with st.sidebar:
    st.header("Filter Data")

    state_list = all_df["customer_state"].unique()

    selected_state = st.multiselect(
        "Pilih State",
        options=state_list,
        default=state_list
    )


main_df = all_df[all_df["customer_state"].isin(selected_state)]


st.header("Dashboard Analisis E-Commerce")


col1, col2 = st.columns(2)

with col1:
    total_orders = main_df["order_id"].nunique()
    st.metric("Total Orders", total_orders)

with col2:
    total_revenue = main_df["price"].sum()
    st.metric("Total Revenue", f"{total_revenue:,.2f}")


st.subheader("State dengan Revenue Tertinggi")

state_df = main_df.groupby("customer_state").agg({
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

state_df.rename(columns={
    "order_id": "total_orders",
    "price": "revenue"
}, inplace=True)

state_df = state_df.sort_values(by="revenue", ascending=False)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=state_df.head(10), x="revenue", y="customer_state", ax=ax)
st.pyplot(fig)


st.subheader("Kategori dengan Revenue Tertinggi")

category_df = main_df.groupby("product_category_name_english").agg({
    "price": "sum",
    "review_score": "mean"
}).reset_index()

category_df.rename(columns={
    "price": "revenue",
    "review_score": "avg_review"
}, inplace=True)

category_df = category_df.sort_values(by="revenue", ascending=False)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=category_df.head(10), x="revenue", y="product_category_name_english", ax=ax)
st.pyplot(fig)


st.subheader("Hubungan Review Score dan Revenue")

fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(
    data=category_df,
    x="avg_review",
    y="revenue",
    ax=ax
)

st.pyplot(fig)


st.subheader("Data Sample")
st.dataframe(main_df.head())