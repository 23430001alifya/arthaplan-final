import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="ArthaPlan Dashboard",
    page_icon="💰",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
     return pd.read_csv("dashboard/main_data (4).csv")

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2489/2489756.png",
    width=100
)

st.sidebar.title("💰 ArthaPlan")

st.sidebar.markdown("---")

kategori = st.sidebar.multiselect(
    "Kategori User",
    options=df["kategori_user"].dropna().unique(),
    default=df["kategori_user"].dropna().unique()
)

credit = st.sidebar.slider(
    "Minimum Credit Score",
    int(df["credit_score"].min()),
    int(df["credit_score"].max()),
    int(df["credit_score"].min())
)

df = df[
    (df["kategori_user"].isin(kategori))
    &
    (df["credit_score"] >= credit)
]

# ==================================================
# HEADER
# ==================================================

st.title("💰 ArthaPlan Interactive Dashboard")

st.markdown(
"""
Dashboard Monitoring Financial Planning & User Spending
"""
)

# ==================================================
# KPI
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total User",
        f"{df['client_id'].nunique():,}"
    )

with col2:
    st.metric(
        "💸 Total Spending",
        f"Rp {df['amount_rupiah'].sum():,.0f}"
    )

with col3:
    st.metric(
        "💳 Avg Credit Score",
        f"{df['credit_score'].mean():.0f}"
    )

with col4:
    st.metric(
        "⚠️ Overbudget User",
        f"{df['overbudget'].sum():,}"
    )

st.divider()

# ==================================================
# CHART 1
# ==================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Kategori User")

    fig, ax = plt.subplots()

    df["kategori_user"].value_counts().plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("💳 Credit Category")

    fig, ax = plt.subplots()

    df["credit_category"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

# ==================================================
# CHART 2
# ==================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Distribusi Credit Score")

    fig, ax = plt.subplots()

    ax.hist(
        df["credit_score"],
        bins=20
    )

    st.pyplot(fig)

with col2:

    st.subheader("💰 Distribusi Pendapatan")

    fig, ax = plt.subplots()

    ax.hist(
        df["yearly_income_rupiah"],
        bins=20
    )

    st.pyplot(fig)

# ==================================================
# TOP SPENDING USER
# ==================================================

st.subheader("🏆 Top 10 Spending User")

top_user = (
    df.groupby("client_id")["total_spending"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_user)

# ==================================================
# OVERBUDGET
# ==================================================

st.subheader("⚠️ Overbudget Monitoring")

overbudget = (
    df["overbudget"]
    .value_counts()
)

st.bar_chart(overbudget)

# ==================================================
# DATA TABLE
# ==================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)

# ==================================================
# DOWNLOAD
# ==================================================

csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="arthaplan_filtered.csv",
    mime="text/csv"
)
