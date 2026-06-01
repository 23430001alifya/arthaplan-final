import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="ArthaPlan Dashboard",
    page_icon="💰",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data_final.csv")

df = load_data()

# =========================
# TITLE
# =========================

st.title("💰 ArthaPlan Dashboard")
st.markdown(
    "Analisis Perilaku Pengeluaran Pengguna"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Filter")

kategori = st.sidebar.multiselect(
    "Kategori",
    options=df["kategori"].unique(),
    default=df["kategori"].unique()
)

df = df[
    df["kategori"].isin(kategori)
]

# =========================
# KPI
# =========================

total_user = df["client_id"].nunique()

avg_spending = (
    df["total_spending"].mean()
)

avg_transaction = (
    df["transaction_count"].mean()
)

overbudget_count = (
    df["overbudget"].sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total User",
    f"{total_user:,}"
)

col2.metric(
    "Avg Spending",
    f"Rp {avg_spending:,.0f}"
)

col3.metric(
    "Avg Transaction",
    f"{avg_transaction:,.0f}"
)

col4.metric(
    "Overbudget User",
    f"{overbudget_count:,}"
)

st.divider()

# =========================
# DISTRIBUSI SPENDING
# =========================

st.subheader(
    "Distribusi Total Spending"
)

fig1 = px.histogram(
    df,
    x="total_spending",
    nbins=30
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================
# KATEGORI USER
# =========================

st.subheader(
    "Distribusi Kategori Pengguna"
)

kategori_count = (
    df["kategori"]
    .value_counts()
    .reset_index()
)

kategori_count.columns = [
    "Kategori",
    "Jumlah"
]

fig2 = px.pie(
    kategori_count,
    names="Kategori",
    values="Jumlah",
    hole=0.4
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# OVERBUDGET
# =========================

st.subheader(
    "Status Overbudget"
)

overbudget_count = (
    df["overbudget"]
    .value_counts()
    .reset_index()
)

overbudget_count.columns = [
    "Status",
    "Jumlah"
]

fig3 = px.bar(
    overbudget_count,
    x="Status",
    y="Jumlah"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================
# TOP 10 USER
# =========================

st.subheader(
    "Top 10 Pengguna dengan Spending Tertinggi"
)

top10 = (
    df.sort_values(
        by="total_spending",
        ascending=False
    )
    .head(10)
)

fig4 = px.bar(
    top10,
    x="client_id",
    y="total_spending"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================
# SCATTER
# =========================

st.subheader(
    "Transaction Count vs Spending"
)

fig5 = px.scatter(
    df,
    x="transaction_count",
    y="total_spending",
    color="kategori"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =========================
# RAW DATA
# =========================

with st.expander("Lihat Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
