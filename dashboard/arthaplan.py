# =========================================================
# PREMIUM ARTHAPLAN DASHBOARD
# MODERN UI - DARK MODE
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ArthaPlan Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3, h4, h5, h6 {
    color: white;
}

label, p, div {
    color: #d1d5db;
}

.metric-card {
    background: linear-gradient(
        135deg,
        #1e293b,
        #111827
    );
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #312e81;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.chart-card {
    background: #111827;
    padding: 20px;
    border-radius: 20px;
    margin-top: 10px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    'dashboard/clean_arthaplan (1).csv'
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💰 ArthaPlan")

st.sidebar.markdown("""
Financial Planning Dashboard
""")

# FILTER CATEGORY
selected_category = st.sidebar.multiselect(
    "Kategori Pengguna",
    options=df['user_category'].unique(),
    default=df['user_category'].unique()
)

df = df[
    df['user_category'].isin(
        selected_category
    )
]

# FILTER CATEGORY EXPENSE
selected_expense = st.sidebar.multiselect(
    "Expense Category",
    options=df['expense_category'].unique(),
    default=df['expense_category'].unique()
)

df = df[
    df['expense_category'].isin(
        selected_expense
    )
]

# =========================================================
# HEADER
# =========================================================

st.markdown("""
# 💰 ArthaPlan Financial Dashboard

Analisis pengeluaran, budgeting,
dan fraud detection pengguna.
""")

# =========================================================
# KPI SECTION
# =========================================================

total_spending = df[
    'amount_rupiah'
].sum()

avg_transaction = df[
    'amount_rupiah'
].mean()

total_users = df[
    'client_id'
].nunique()

fraud_count = df[
    'is_fraud'
].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h5>Total Pengeluaran</h5>
        <h2>Rp {:,.0f}</h2>
    </div>
    """.format(total_spending),
    unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h5>Rata-rata Transaksi</h5>
        <h2>Rp {:,.0f}</h2>
    </div>
    """.format(avg_transaction),
    unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h5>Total User</h5>
        <h2>{}</h2>
    </div>
    """.format(total_users),
    unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h5>Fraud Transaction</h5>
        <h2>{}</h2>
    </div>
    """.format(fraud_count),
    unsafe_allow_html=True)

# =========================================================
# CHART ROW 1
# =========================================================

col5, col6 = st.columns(2)

# =========================================================
# USER CATEGORY
# =========================================================

with col5:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    st.subheader("📊 Kategori Pengguna")

    category_count = (
        df['user_category']
        .value_counts()
        .reset_index()
    )

    category_count.columns = [
        'Kategori',
        'Jumlah'
    ]

    fig1 = px.pie(
        category_count,
        names='Kategori',
        values='Jumlah',
        hole=0.6,
        template='plotly_dark'
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================================
# FRAUD DISTRIBUTION
# =========================================================

with col6:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    st.subheader("🚨 Fraud Distribution")

    fraud_dist = (
        df['is_fraud']
        .value_counts()
        .reset_index()
    )

    fraud_dist.columns = [
        'Fraud',
        'Jumlah'
    ]

    fig2 = px.bar(
        fraud_dist,
        x='Fraud',
        y='Jumlah',
        text_auto=True,
        template='plotly_dark'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================================
# CHART ROW 2
# =========================================================

col7, col8 = st.columns(2)

# =========================================================
# EXPENSE CATEGORY
# =========================================================

with col7:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    st.subheader("🛒 Expense Category")

    expense = (
        df.groupby('expense_category')[
            'amount_rupiah'
        ]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        expense,
        x='expense_category',
        y='amount_rupiah',
        text_auto=True,
        template='plotly_dark'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================================
# BUDGET USAGE
# =========================================================

with col8:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    st.subheader("📈 Budget Usage")

    fig4 = px.histogram(
        df,
        x='budget_usage',
        nbins=30,
        template='plotly_dark'
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================================
# WARNING TABLE
# =========================================================

st.markdown("""
<div class="chart-card">
""", unsafe_allow_html=True)

st.subheader("⚠️ Budget Warning")

warning = df[
    df['budget_usage'] >= 90
]

st.dataframe(
    warning[
        [
            'client_id',
            'expense_category',
            'budget_usage',
            'warning'
        ]
    ],
    use_container_width=True
)

st.markdown("</div>",
unsafe_allow_html=True)

# =========================================================
# RAW DATA
# =========================================================

st.markdown("""
<div class="chart-card">
""", unsafe_allow_html=True)

st.subheader("🧾 Transaction Data")

st.dataframe(
    df.head(100),
    use_container_width=True
)

st.markdown("</div>",
unsafe_allow_html=True)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name='arthaplan.csv',
    mime='text/csv'
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<center>
ArthaPlan Dashboard • Built with Streamlit
</center>
""", unsafe_allow_html=True)
