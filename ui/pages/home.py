import streamlit as st
import sqlite3
import pandas as pd
from ui.state import get_backend
pd.options.display.float_format = '{:.2f}'.format

db_path = "db/test.db"
conn = sqlite3.connect(db_path)
# cur = conn.cursor()
backend = get_backend(conn)

# Main page content
st.markdown("# Welcome to the Home Page")
st.sidebar.markdown("# Home")

st.markdown("## Transactions this Month")
df = backend.get_test_df()
df.columns = ["Date", "Description", "Category", "Amount"]

# st.table(df, border='horizontal')
st.dataframe(df)

st.markdown("## Total per Category")
df_cat = backend.get_aggregate()
df_cat.columns = ["Category", "Amount"]
st.table(df_cat, border='horizontal')
conn.close()
