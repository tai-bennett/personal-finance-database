import streamlit as st
import sqlite3
from ui.state import get_backend

db_path = "db/test.db"
conn = sqlite3.connect(db_path)
# cur = conn.cursor()
backend = get_backend(conn)

# Main page content
st.markdown("# Welcome to the Home Page")
st.sidebar.markdown("# Home")

df = backend.get_test_df()
df.columns = ["Date", "Description", "Category", "Amount"]

st.table(df)
conn.close()
