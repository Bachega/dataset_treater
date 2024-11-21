import streamlit as st
import pandas as pd
import numpy as np

from components import load_dataframe, class_selector, class_proportion, test_mfe, test_scorer, preprocess_data
from math import ceil

if "show_controls" not in st.session_state:
    st.session_state.show_controls = False

if "df" not in st.session_state:
    st.session_state.df = None

if "class_col" not in st.session_state:
    st.session_state.class_col = None

st.set_page_config(page_title="Dataset Treater")
st.title("Dataset Treater")

def class_selector_and_prevalence(df):
    with st.container(border=True):
        class_col = class_selector(df)
        class_proportion(df, class_col)

        with st.container():
            dataset_size = len(df)

            class_list = sorted(df[class_col].unique().tolist())

            pos_prop = len(df[df[class_col] == class_list[1]]) / dataset_size
            neg_prop = len(df[df[class_col] == class_list[0]]) / dataset_size
            
            col1, col2 = st.columns(2)
            with col1:
                sample_size = st.number_input("Sample size", min_value=0, max_value=1000, value=100)
            with col2:
                test_size = st.number_input("Test size", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
            
            pos_number_sample_test = ceil(pos_prop * dataset_size * test_size)
            neg_number_sample_test = ceil(neg_prop * dataset_size * test_size)

            if pos_number_sample_test > sample_size:
                st.write(f":green[Positive samples for test: {pos_number_sample_test}]")
            else:
                st.write(f":red[Positive samples for test: {pos_number_sample_test}]")
            
            if neg_number_sample_test > sample_size:
                st.write(f":green[Negative samples for test: {neg_number_sample_test}]")
            else:
                st.write(f":red[Negative samples for test: {neg_number_sample_test}]")
    return class_col

def edit_dataset():
    st.title("Edit dataset")
    st.write("Edit freely the dataset below")
    with st.container(border=True):
        edited_df = st.data_editor(df)
        csv = edited_df.to_csv(index=False)
        st.download_button(label="Save and Download",
                        data=csv,
                        file_name='edited_dataframe.csv',
                        mime="text/csv")

def menu(df):
    # col1, col2 = st.columns(2)
    class_col = class_selector_and_prevalence(df)
    df = preprocess_data(df, class_col)
    test_mfe(st.session_state.df, class_col)
    test_scorer(st.session_state.df, class_col)
    edit_dataset()

df = load_dataframe()
if df is not None:
    menu(df)
else:
    st.session_state.show_controls = False