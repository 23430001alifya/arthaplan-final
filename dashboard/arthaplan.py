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

st.sidebar.title("💰 ArthaPlan")

kategori = st.sidebar.multiselect(
    "Kategori User",
    options=df["kategori_user"].unique(),
    default=df["kategori_user"].unique()
)

credit_min = st.sidebar.slider(
    "Minimum Credit Score",
    int(df["credit_score"].min()),
    int(df["credit_score"].max()),
    int(df["credit_score"].min())
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

df = df[
    (df["kategori_user"].isin(kategori))
    &
    (df["credit_score"] >= credit_min)
    &
    (df["gender"].isin(gender))
]

# ==================================================
# HEADER
# ==================================================

st.title("💰 ArthaPlan Dashboard")
st.markdown("### Financial Planning & User Profiling")

# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total User",
        f"{df['id'].nunique():,}"
    )

with col2:
    st.metric(
        "💵 Avg Income",
        f"Rp {df['yearly_income_rupiah'].mean():,.0f}"
    )

with col3:
    st.metric(
        "💳 Avg Credit Score",
        f"{df['credit_score'].mean():.0f}"
    )

with col4:
    st.metric(
        "🏦 Avg Debt",
        f"Rp {df['total_debt_rupiah'].mean():,.0f}"
    )

st.divider()

# ==================================================
# CHARTS BARIS 1
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
# CHARTS BARIS 2
# ==================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("💰 Distribusi Pendapatan")

    fig, ax = plt.subplots()

    ax.hist(
        df["yearly_income_rupiah"],
        bins=20
    )

    st.pyplot(fig)

with col2:

    st.subheader("🏦 Distribusi Hutang")

    fig, ax = plt.subplots()

    ax.hist(
        df["total_debt_rupiah"],
        bins=20
    )

    st.pyplot(fig)

# ==================================================
# CHARTS BARIS 3
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

    st.subheader("👨‍💼 Gender")

    fig, ax = plt.subplots()

    df["gender"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

# ==================================================
# TOP USER INCOME
# ==================================================

st.subheader("🏆 Top 10 Pendapatan Tertinggi")

top_income = (
    df.sort_values(
        "yearly_income_rupiah",
        ascending=False
    )
    .head(10)
)

st.bar_chart(
    top_income.set_index("id")[
        "yearly_income_rupiah"
    ]
)

# ==================================================
# DATA TABLE
# ==================================================

st.subheader("📋 Data Pengguna")

st.dataframe(
    df,
    use_container_width=True
)

# ==================================================
# DOWNLOAD
# ==================================================

csv = df.to_csv(index=False)

st.download_button(
    "⬇️ Download Data",
    csv,
    "arthaplan_filtered.csv",
    "text/csv"
)
