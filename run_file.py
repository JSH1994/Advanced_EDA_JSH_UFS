import streamlit as st
import pandas as pd
import sweetviz as sv
import tempfile
from pathlib import Path
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report

st.set_page_config(page_title="EDA App", layout="wide")
st.title("Exploratory Data Analysis")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully")

    st.subheader("Data preview")
    st.dataframe(df.head())

    st.subheader("Dataset information")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")
    st.write("Data types:")
    st.dataframe(df.dtypes.astype(str).rename("dtype"))

    st.subheader("Missing values")
    st.dataframe(df.isnull().sum().rename("missing_values"))

    st.subheader("Summary statistics")
    st.dataframe(df.describe(include="all"))

    report_choice = st.radio(
        "Choose report type",
        ["Sweetviz", "YData Profiling", "Both"],
        index=0
    )

    if report_choice in ["Sweetviz", "Both"]:
        st.subheader("Sweetviz report")
        with st.spinner("Generating Sweetviz report..."):
            with tempfile.TemporaryDirectory() as tmp_dir:
                report_path = Path(tmp_dir) / "sweetviz_report.html"
                report = sv.analyze(df)
                report.show_html(filepath=str(report_path), open_browser=False)
                html = report_path.read_text(encoding="utf-8")

            st.components.v1.html(html, height=1200, scrolling=True)

    if report_choice in ["YData Profiling", "Both"]:
        st.subheader("YData Profiling report")
        with st.spinner("Generating YData report..."):
            profile = ProfileReport(df, explorative=True)
            st_profile_report(profile)

else:
    st.info("Please upload a CSV file to begin.")
