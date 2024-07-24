import streamlit as st
from urllib.request import urlopen
import pandas as pd
import app

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"
url = "https://seekingalpha.com/symbol/UBER/growth"

sample = app.ttm_revenue
print(sample)