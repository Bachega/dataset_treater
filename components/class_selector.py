import streamlit as st

from utils import find_class

def class_selector(df):
    class_list = find_class(df)
    selected_class = st.selectbox("Select a class", class_list)
    return selected_class