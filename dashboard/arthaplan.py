import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIG PAGE
# ==================================================

st.set_page_config(
    page_title="ArthaPlan Dashboard",
    page_icon="💰",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#f8faf8;
}

[data-testid="stSidebar"]{
    background-color:#14532d;
}

[data-testid="stSidebar"] *{
    color:white;
}

.kpi-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    border-left:6px solid #22c55e;
}

h1,h2,h3{
    color:#14532d;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data_final.csv")

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("💰 ArthaPlan")

st.sidebar.markdown("---")

st.sidebar.subheader("Filter")

kategori_filter = st.sidebar.multiselect(
    "Kategori",
    options=df["kategori"].unique(),
    default=df["kategori"].unique()
)

card_filter = st.sidebar.multiselect(
    "Card Type",
    options=df["card_type"].unique(),
    default=df["card_type"].unique()
)

overbudget_filter = st.sidebar.multiselect(
    "Overbudget",
    options=df["overbudget"].unique(),
    default=df["overbudget"].unique()
)

df = df[
    (df["kategori"].isin(kategori_filter))
    &
    (df["card_type"].isin(card_filter))
    &
    (df["overbudget"].isin(overbudget_filter))
]

# ==================================================
# HEADER
# ==================================================

st.title("💰 ArthaPlan Analytics")

st.markdown("""
Dashboard Analisis Pengeluaran Pengguna, Segmentasi Perilaku Keuangan,
dan Identifikasi Risiko Overbudget.
""")

# ==================================================
# KPI
# ==================================================

total_user = df["client_id"].nunique()

total_spending = df["total_spending"].sum()

avg_spending = df["total_spending"].mean()

overbudget_user = df["overbudget"].sum()

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h4>Total User</h4>
        <h2>{total_user:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <h4>Total Spending</h4>
        <h2>Rp {total_spending:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <h4>Avg Spending</h4>
        <h2>Rp {avg_spending:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <h4>Overbudget User</h4>
        <h2>{overbudget_user:,}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# INSIGHT
# ==================================================

st.success(
    f"""
    📌 Insight Utama

    • Total pengguna yang dianalisis: {total_user:,}

    • Total pengeluaran: Rp {total_spending:,.0f}

    • Rata-rata pengeluaran pengguna: Rp {avg_spending:,.0f}

    • Jumlah pengguna overbudget: {overbudget_user:,}

    • Mayoritas pengguna berada pada kategori: {df['kategori'].mode()[0]}
    """
)

# ==================================================
# ROW 1
# ==================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("Distribusi Total Spending")

    fig1 = px.histogram(
        df,
        x="total_spending",
        nbins=30,
        color_discrete_sequence=["#16a34a"]
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    st.subheader("Distribusi Kategori Pengguna")

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
        hole=0.5,
        color_discrete_sequence=[
            "#14532d",
            "#16a34a",
            "#4ade80"
        ]
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# ROW 2
# ==================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("Overbudget Analysis")

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
        y="Jumlah",
        color="Jumlah",
        color_continuous_scale="greens"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:

    st.subheader("Transaction Count vs Spending")

    fig4 = px.scatter(
        df,
        x="transaction_count",
        y="total_spending",
        color="kategori",
        color_discrete_sequence=[
            "#14532d",
            "#16a34a",
            "#4ade80"
        ]
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==================================================
# TOP USER
# ==================================================

st.subheader("Top 10 Pengguna dengan Spending Tertinggi")

top10 = (
    df
    .sort_values(
        by="total_spending",
        ascending=False
    )
    .head(10)
)

fig5 = px.bar(
    top10,
    x="client_id",
    y="total_spending",
    color="total_spending",
    color_continuous_scale="greens"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==================================================
# RAW DATA
# ==================================================

with st.expander("Lihat Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
