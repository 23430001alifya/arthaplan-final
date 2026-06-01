import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ArthaPlan Dashboard",
    page_icon="💰",
    layout="wide"
)

pio.templates.default = "plotly_white"

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.main{
    background:#f8faf8;
}

[data-testid="stSidebar"]{
    background:#14532d;
}

[data-testid="stSidebar"] *{
    color:white;
}

.kpi-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
    border-left:6px solid #22c55e;
}

.kpi-title{
    color:#6b7280;
    font-size:14px;
}

.kpi-value{
    color:#14532d;
    font-size:28px;
    font-weight:bold;
}

.insight-box{
    background:#dcfce7;
    padding:18px;
    border-radius:12px;
    border-left:6px solid #16a34a;
}

h1,h2,h3{
    color:#14532d;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data_final.csv")

df = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("💰 ArthaPlan")

st.sidebar.markdown("---")

st.sidebar.subheader("Filter Dashboard")

kategori = st.sidebar.multiselect(
    "Kategori",
    df["kategori"].unique(),
    default=df["kategori"].unique()
)

card_type = st.sidebar.multiselect(
    "Card Type",
    df["card_type"].unique(),
    default=df["card_type"].unique()
)

overbudget = st.sidebar.multiselect(
    "Overbudget",
    df["overbudget"].unique(),
    default=df["overbudget"].unique()
)

df = df[
    (df["kategori"].isin(kategori))
    &
    (df["card_type"].isin(card_type))
    &
    (df["overbudget"].isin(overbudget))
]

# =====================================
# HEADER
# =====================================

st.title("💰 ArthaPlan Analytics")

st.caption(
    "Smart Financial Planning Dashboard"
)

# =====================================
# KPI
# =====================================

total_user = df["client_id"].nunique()

total_spending = df["total_spending"].sum()

avg_spending = df["total_spending"].mean()

overbudget_user = df["overbudget"].sum()

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>TOTAL USER</div>
        <div class='kpi-value'>{total_user:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>TOTAL SPENDING</div>
        <div class='kpi-value'>
        Rp {total_spending:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>AVG SPENDING</div>
        <div class='kpi-value'>
        Rp {avg_spending:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>OVERBUDGET USER</div>
        <div class='kpi-value'>
        {overbudget_user:,}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# INSIGHT
# =====================================

st.markdown(f"""
<div class="insight-box">

<b>📌 Insight Utama</b>

<br><br>

• Total pengguna: {total_user:,}

<br>

• Total spending: Rp {total_spending:,.0f}

<br>

• Average spending: Rp {avg_spending:,.0f}

<br>

• User overbudget: {overbudget_user:,}

<br>

• Mayoritas kategori:
<b>{df['kategori'].mode()[0]}</b>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# ROW 1
# =====================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("Distribusi Total Spending")

    fig1 = px.histogram(
        df,
        x="total_spending",
        nbins=30,
        color_discrete_sequence=["#16a34a"]
    )

    fig1.update_layout(
        height=400
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    st.subheader("Kategori Pengguna")

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
        hole=0.55,
        color_discrete_sequence=[
            "#14532d",
            "#16a34a",
            "#4ade80"
        ]
    )

    fig2.update_layout(
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================
# ROW 2
# =====================================

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
        color="Status",
        color_discrete_sequence=[
            "#14532d",
            "#22c55e"
        ]
    )

    fig3.update_layout(
        showlegend=False,
        height=400
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:

    st.subheader("Transaction vs Spending")

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

    fig4.update_layout(
        height=400
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================
# TOP 10 USER
# =====================================

st.subheader(
    "Top 10 Pengguna dengan Spending Tertinggi"
)

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
    color_discrete_sequence=["#16a34a"]
)

fig5.update_layout(
    height=500
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =====================================
# RAW DATA
# =====================================

with st.expander("📄 Lihat Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
