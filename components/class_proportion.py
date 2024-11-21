import streamlit as st
import pandas as pd
import plotly.express as px

def class_proportion(df, class_col):
    class_counts = df[class_col].value_counts().reset_index()
    class_counts.columns = [class_col, 'count']
    fig = px.pie(class_counts, names=class_col, values='count', title='Class Proportion')
    st.plotly_chart(fig)
 