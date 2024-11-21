import streamlit as st
import pandas as pd
import numpy as np

from components import load_dataframe

if "show_controls" not in st.session_state:
    st.session_state.show_controls = False

st.title("Dataset Treater")

df = load_dataframe()

if df is not None:
    st.data_editor(df)
else:
    st.session_state.show_controls = False