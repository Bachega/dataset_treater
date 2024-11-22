import streamlit as st
import pandas as pd
from scipy.io import arff
from io import StringIO

from utils import arff_to_csv

def load_dataframe():
    file = st.file_uploader("Upload a CSV/ARFF")

    # df = None
    if file is not None:
        if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != file.name:
            if file.name.endswith('.arff'):
                st.session_state.df = arff_to_csv(file)
            elif file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(file)

            st.session_state.df_og = st.session_state.df.copy(deep=True)
                        
            st.session_state.uploaded_file = file.name
    else:
        st.session_state.df = None
        st.session_state.df_og = None
        st.session_state.uploaded_file = None
    # return df