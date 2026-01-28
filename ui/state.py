import streamlit as st
from src.DashboardService import DashboardService
from src.config import *

# @st.cache_resource
def get_backend(conn):
    # config, _ = get_config_from_json("configs/config_test.json")
    return DashboardService(conn)
