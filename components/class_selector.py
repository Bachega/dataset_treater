import streamlit as st

def find_class(dataframe):
    columns_with_two_unique_values = [col for col in dataframe.columns if dataframe[col].nunique() == 2]
    if len(columns_with_two_unique_values) == 1:
        return columns_with_two_unique_values[0]
    return columns_with_two_unique_values

def class_selector(df):
    class_list = find_class(df)
    
    synonyms = ['class', 'target']
    index = 0
    for _class in class_list:
        if _class.lower() in synonyms:
            index = class_list.index(_class)

    selected_class = st.selectbox("Select the column that represents the class", class_list, index=index)
    return selected_class