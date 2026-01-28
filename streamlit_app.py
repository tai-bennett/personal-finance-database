import streamlit as st

# Define the pages
home_page = st.Page("ui/pages/home.py", title="Home")
test_page = st.Page("ui/pages/test.py", title="Test Page")

# Set up navigation
pg = st.navigation([home_page, test_page])

# Run the selected page
pg.run()
