import streamlit as st
import pandas as pd

df = pd.read_csv(
    'dashboard/clean_arthaplan.csv'
)
st.title(
    'ArthaPlan Dashboard'
)

# total pengeluaran
st.metric(
    'Total Pengeluaran',
    f"Rp {df['amount_rupiah'].sum():,.0f}"
)

# fraud
st.subheader(
    'Fraud Transaction'
)

st.bar_chart(
    df['is_fraud']
    .value_counts()
)

# kategori user
st.subheader(
    'Kategori Pengguna'
)

st.bar_chart(
    df['user_category']
    .value_counts()
)

# warning budget
st.subheader(
    'Budget Warning'
)

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
    ]
)
