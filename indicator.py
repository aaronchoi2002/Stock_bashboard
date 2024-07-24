import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

url = "https://seekingalpha.com/symbol/UBER/growth"


r_qoq_change = 5.0
pe = 20
def display_indicator(r_qoq_change, pe):
    cols = st.columns(2)
    with cols[0]:
        color = "green" if r_qoq_change > 0 else "red"
        st.markdown(f'<div ; padding: 10px;">Quarter Revenue growth > 0 </div>', unsafe_allow_html=True)
        # Display the stock health indicators
        st.markdown(
            f'<div style="background-color: {color}; color: white; padding: 10px;">Revenue growth: {r_qoq_change:.2f}%</div>',
            unsafe_allow_html=True)

    with cols[1]:
        color = "green" if pe < 25 else "red"
        st.markdown(f'<div ; padding: 10px;">PE Ratio < 25 </div>', unsafe_allow_html=True)
        # Display the stock health indicators
        st.markdown(f'<div style="background-color: {color}; color: white; padding: 10px;">PE Ratio: {pe}</div>',
                unsafe_allow_html=True)