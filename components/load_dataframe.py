import streamlit as st
import pandas as pd

def load_dataframe():
    file = st.file_uploader("Upload a CSV")
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = None
    return df