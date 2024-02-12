import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Plots!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Credit Union Plots")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\nihar.patel\OneDrive - AIVA Partners Pvt. Ltd\Desktop\Work\8QuarterDatabase.csv")
    df = pd.read_csv("8QuarterDatabase.csv", encoding = "ISO-8859-1")


selected_cu_number = st.sidebar.selectbox("Select CU_NUMBER", df["CU_NUMBER"])

# Filter data based on selected CU_NUMBER
selected_data = df[df["CU_NUMBER"] == selected_cu_number]

# Display selected CU_NUMBER's information
st.title("Credit Union Information Comparison")
st.subheader(f"CU_NUMBER: {selected_cu_number}")
st.write(selected_data)

# Visualization - Total Assets
st.title("Total Assets Comparison")
st.bar_chart(selected_data.groupby("CU_NUMBER")["TOTAL ASSETS"].sum())

# Visualization - Other attributes (add more visualizations as needed)
# Example: Total Amount of Shares and Deposits
st.title("Total Amount of Shares and Deposits Comparison")
st.bar_chart(selected_data.groupby("CU_NUMBER")["TOTAL AMOUNT OF SHARES AND DEPOSITS"].sum())