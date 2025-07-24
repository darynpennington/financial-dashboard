import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Company Financial Dashboard")

uploaded_file = st.file_uploader("Upload your financial spreadsheet (Excel or CSV)", type=["xlsx", "xls", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    date_cols = df.select_dtypes(include=['datetime', 'object']).columns.tolist()

    if numeric_cols:
        st.subheader("📈 Graph Generator")
        y_col = st.selectbox("Select a numeric column to plot (Y-axis):", numeric_cols)
        x_col = st.selectbox("Select a column for X-axis:", date_cols)

        try:
            df[x_col] = pd.to_datetime(df[x_col], errors='coerce')
            df = df.dropna(subset=[x_col])
            df = df.sort_values(x_col)

            fig, ax = plt.subplots()
            ax.plot(df[x_col], df[y_col], marker='o')
            ax.set_title(f"{y_col} Over Time")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.grid(True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error in plotting: {e}")
    else:
        st.warning("No numeric columns found for plotting.")
