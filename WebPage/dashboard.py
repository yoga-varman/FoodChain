import sys
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from Config.db import get_conn,DATABASE_URL

st.title("📊 FoodChain Dashboard")

# Database connection

engine = create_engine(DATABASE_URL)

# Get number of users
query = "SELECT COUNT(*) AS user_count FROM foodchain.users"

df = pd.read_sql(query, engine)

user_count = int(df["user_count"].iloc[0])

# Display user count
st.metric(
    label="👥 Total Users",
    value=user_count
)