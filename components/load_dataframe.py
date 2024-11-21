import streamlit as st
import pandas as pd
from scipy.io import arff
from io import StringIO

from utils import arff_to_csv

def load_dataframe():
    file = st.file_uploader("Upload a CSV/ARFF")

    df = None
    if file is not None:
        if file.name.endswith('.arff'):
            df = arff_to_csv(file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
    return df