# =========================================================
# PROFESSIONAL ARTHAPLAN DASHBOARD
# SIMPAN SEBAGAI: app.py
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
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    'dashboard/clean_arthaplan (1).csv'
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("ArthaPlan")

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2489/2489756.png",
    width=120
)

st.sidebar.header("Filter Data")

selected_category = st.sidebar.multiselect(
    "Pilih Kategori User",
    options=df['user_category'].unique(),
    default=df['user_category'].unique()
)

df = df[
    df['user_category'].isin(selected_category)
]

# =========================================================
# HEADER
# =========================================================

st.title("💰 ArthaPlan Financial Dashboard")

st.markdown("""
Dashboard analisis keuangan untuk monitoring pengeluaran,
budgeting, dan fraud detection.
""")

# =========================================================
# KPI SECTION
# =========================================================

total_spending = df['amount_rupiah'].sum()

avg_transaction = df['amount_rupiah'].mean()

total_users = df['client_id'].nunique()

fraud_count = df['is_fraud'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Pengeluaran",
        f"Rp {total_spending:,.0f}"
    )

with col2:
    st.metric(
        "Rata-rata Transaksi",
        f"Rp {avg_transaction:,.0f}"
    )

with col3:
    st.metric(
        "Total User",
        total_users
    )

with col4:
    st.metric(
        "Fraud Transaction",
        fraud_count
    )

# =========================================================
# CHART 1 - USER CATEGORY
# =========================================================

st.subheader("📊 Distribusi Kategori Pengguna")

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
    hole=0.5
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# EXPENSE CATEGORY CHART
# =====================================================

st.subheader("🛒 Expense Category")

expense = (
    df.groupby('expense_category')[
        'amount_rupiah'
    ]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    expense,
    x='expense_category',
    y='amount_rupiah',
    text_auto=True
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =========================================================
# CHART 2 - FRAUD DISTRIBUTION
# =========================================================

st.subheader("🚨 Distribusi Fraud")

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
    text_auto=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# CHART 3 - TOP SPENDING USER
# =========================================================

st.subheader("💸 Top Spending User")

top_user = (
    df.groupby('client_id')[
        'amount_rupiah'
    ]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_user,
    x='client_id',
    y='amount_rupiah',
    text_auto=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# CHART 4 - BUDGET USAGE
# =========================================================

st.subheader("📈 Budget Usage")

fig4 = px.histogram(
    df,
    x='budget_usage',
    nbins=30
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================================================
# EARLY WARNING SYSTEM
# =========================================================

st.subheader("⚠️ Budget Warning")

warning = df[
    df['budget_usage'] >= 90
]

st.dataframe(
    warning[
        [
            'client_id',
            'budget_usage',
            'warning'
        ]
    ],
    use_container_width=True
)

# =========================================================
# TRANSACTION TABLE
# =========================================================

st.subheader("🧾 Transaction Data")

st.dataframe(
    df.head(100),
    use_container_width=True
)

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

st.markdown(
    "Developed with ❤️ using Streamlit | ArthaPlan"
)
