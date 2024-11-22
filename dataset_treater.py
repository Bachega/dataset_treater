import streamlit as st
import pandas as pd
import numpy as np

from components import load_dataframe, class_selector, class_proportion, test_mfe, test_scorer, preprocess_data
from math import ceil

if "show_controls" not in st.session_state:
    st.session_state.show_controls = False

if "df" not in st.session_state:
    st.session_state.df = None

if "df_og" not in st.session_state:
    st.session_state.df_og = None

if "class_col" not in st.session_state:
    st.session_state.class_col = None

if "treatments" not in st.session_state:
    st.session_state.treatments = {}

if "tests_run" not in st.session_state:
    st.session_state.tests_run = []

st.set_page_config(page_title="Dataset Treater")
st.title("Dataset Treater")

def class_selector_and_prevalence():
    df = st.session_state.df
    
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

        preprocess_data(st.session_state.df, class_col)
        
    return class_col

def review(class_col):
    st.title("Review")
    st.subheader(f"Class: :blue[{class_col}]")
    if 'show_original' not in st.session_state:
        st.session_state.show_original = False

    st.session_state.show_original = st.checkbox("Show Original Dataset", value=st.session_state.show_original)

    st.subheader("Treated dataset")
    st.dataframe(st.session_state.df)

    if st.session_state.show_original:
        st.subheader("Original dataset")
        st.dataframe(st.session_state.df_og)

    df = st.session_state.df.copy(deep=True)
    if class_col != 'class':
        df['class'] = df[class_col]
        df = df.drop(columns=[class_col])
        class_col = 'class'
        # csv = st.session_state.df.to_csv(index=False)
    csv = df.to_csv(index=False)
    file_name = st.session_state.uploaded_file.split('.')[0]+'.csv'
    st.download_button(label="Save and Download",
                    data=csv,
                    file_name=file_name,
                    mime="text/csv")

def undo_changes():
    if st.button("Undo Changes"):
        st.session_state.df = st.session_state.df_og.copy(deep=True)
        st.rerun()

def menu():
    # col1, col2 = st.columns(2)
    undo_changes()
    class_col = class_selector_and_prevalence()
    # preprocess_data(st.session_state.df, class_col)
    test_mfe(st.session_state.df, class_col)
    test_scorer(st.session_state.df, class_col)
    review(class_col)

load_dataframe()
if st.session_state.df is not None:
    # st.write(st.session_state.df)
    # st.write(st.session_state.df.drop_duplicates())
    menu()
else:
    st.session_state.show_controls = False