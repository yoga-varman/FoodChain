import streamlit as st
import plotly.express as px
import pandas as pd

st.title("📊 FoodChain Dashboard")

data = pd.DataFrame({
    "Category": [
        "Vegetables",
        "Fruits",
        "Grains",
        "Dairy",
        "Meat"
    ],
    "Products": [
        35,
        25,
        20,
        12,
        8
    ]
})

fig = px.pie(
    data,
    names="Category",
    values="Products",
    hole=0.45,
    title="Food Category Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)