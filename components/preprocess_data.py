import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def preprocess_data(df, class_col):
    with st.container(border = False):
        st.subheader("Pre-processing")
        
        with st.container(border = False):
            st.subheader(f"Selected class column: :blue[{class_col}]")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                use_label_encoder = st.checkbox(f"Label Encoder ({class_col})", value=False, key='label_encoder')
            with col2:
                drop_missing_values = st.checkbox("Drop Missing Values", value=False, key='missing_val')
            with col3:
                drop_duplicates = st.checkbox("Drop Duplicates", value=False, key='drop_dupes')
            with col4:
                use_one_hot_encoding = st.checkbox("One-Hot Encoding", value=False, key='one_hot_encoding')

            if st.button("Preprocess", key='run_processing'):
                if use_label_encoder:
                    le = LabelEncoder()
                    df[class_col] = le.fit_transform(df[class_col])
                    st.write(f"Applied Label Encoder to column: :blue[{class_col}]")

                if drop_missing_values:
                    df = df.dropna()
                    st.write("Dropped rows with missing values")

                if drop_duplicates:
                    df = df.drop_duplicates()
                    st.write("Dropped duplicate rows")
                
                if use_one_hot_encoding:
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                    if class_col in categorical_cols:
                        categorical_cols = categorical_cols.drop(class_col)
                    
                    if len(categorical_cols) > 0:
                        encoder = OneHotEncoder(sparse_output=False, drop='first')
                        encoded = encoder.fit_transform(df[categorical_cols])
                        encoded_cols = encoder.get_feature_names_out(categorical_cols)
                        encoded_df = pd.DataFrame(encoded, columns=encoded_cols, index=df.index)

                        df = df.drop(columns=categorical_cols)
                        df = pd.concat([df, encoded_df], axis=1)

                        st.write(f"One-Hot Encoded columns: :blue[{', '.join(categorical_cols)}]")
                    else:
                        st.write("No categorical columns present")

                st.success("Pre-processing completed")
                st.session_state.df = df
                st.rerun()

            st.markdown(f"""
            - **Number of rows:** {df.shape[0]}
            - **Number of columns:** {df.shape[1]}
            - **Missing values:** {df.isnull().sum().sum()}
            - **Duplicate rows:** {df.duplicated().sum()}
            """)

            show_all = st.checkbox("Show all rows", value=False)
            if show_all:
                st.dataframe(st.session_state.df)
            else:
                st.dataframe(st.session_state.df.head(6))