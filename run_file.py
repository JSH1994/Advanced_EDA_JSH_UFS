# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport

st.set_page_config(page_title="EDA App", layout="wide")

st.title("Exploratory Data Analysis (EDA)")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",")

    st.success("File uploaded successfully!")

    # Preview
    st.subheader("Preview of Data")
    st.dataframe(df.head())

    # Info
    st.subheader("Dataset Info")
    st.write(f"Shape: {df.shape}")
    st.write("Data Types:")
    st.write(df.dtypes)

    # Missing values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Description
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe())

    # Profiling report
    st.subheader("Full EDA Report")

    with st.spinner("Generating report..."):
        profile = ProfileReport(df, title="EDA Report", explorative=True)
        st.components.v1.html(profile.to_html(), height=1200, scrolling=True)

else:
    st.info("Please upload a CSV file to begin.")
