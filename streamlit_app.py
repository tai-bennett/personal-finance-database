import streamlit as st

# Define the pages
home_page = st.Page("ui/pages/home.py", title="Home")
trends_page = st.Page("ui/pages/trends.py", title="Trends")
db_page = st.Page("ui/pages/database.py", title="Database")
about_page = st.Page("ui/pages/about.py", title="About")

# Set up navigation
pg = st.navigation([home_page, trends_page, db_page, about_page])

# Run the selected page
pg.run()
