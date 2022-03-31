import streamlit as st
from  predict_page import show_predict_page
from plot_page import show_plot_page


# SIDEBAR
page = st.sidebar.selectbox("Other Details you can Check ",("Prediction", "Plot"))

if page=="Prediction":
    show_predict_page()
else:
    show_plot_page()
