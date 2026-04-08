# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport

st.set_page_config(page_title="EDA Report App", layout="wide")

st.title("Exploratory Data Analysis App")
st.write("Upload a CSV file or use the bundled sample file to generate a quick EDA report.")

DEFAULT_FILE = "Morphological_yield_components.csv"

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

file_to_read = None
file_name = None

if uploaded_file is not None:
    file_to_read = uploaded_file
    file_name = uploaded_file.name
elif os.path.exists(DEFAULT_FILE):
    file_to_read = DEFAULT_FILE
    file_name = DEFAULT_FILE

if file_to_read is None:
    st.info(
        "No file found yet. Upload a CSV file, or add "
        f"`{DEFAULT_FILE}` to the same folder as `app.py` in your GitHub repo."
    )
    st.stop()

try:
    df = pd.read_csv(file_to_read, sep=",")
except Exception as e:
    st.error(f"Could not read the CSV file: {e}")
    st.stop()

st.success(f"Loaded file: {file_name}")

with st.expander("Preview data", expanded=True):
    st.dataframe(df.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dataset shape")
    st.write({"rows": df.shape[0], "columns": df.shape[1]})

    st.subheader("Data types")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "column", 0: "dtype"}))

with col2:
    st.subheader("Missing values")
    st.dataframe(
        df.isnull().sum().reset_index().rename(columns={"index": "column", 0: "missing_values"})
    )

st.subheader("Descriptive statistics")
st.dataframe(df.describe(include="all").transpose())

st.subheader("Profiling report")
with st.spinner("Generating the profiling report..."):
    profile = ProfileReport(df, title="EDA Report", explorative=True)
    profile_html = profile.to_html()

st.components.v1.html(profile_html, height=1200, scrolling=True)
