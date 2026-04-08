# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport

st.set_page_config(page_title="EDA App", layout="wide")

st.title("Exploratory Data Analysis (EDA)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully")

    # Preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Basic info
    st.subheader("Dataset Information")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write("Data Types:")
    st.write(df.dtypes)

    # Missing values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    # Profiling report
    st.subheader("Full EDA Report")

    with st.spinner("Generating report..."):
        profile = ProfileReport(df, explorative=True)
        st.components.v1.html(profile.to_html(), height=1000, scrolling=True)

else:
    st.info("Please upload a CSV file to begin.")
