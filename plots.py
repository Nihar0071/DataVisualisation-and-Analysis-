import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Plots!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Credit Union Plots")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)

    # Check file type and read accordingly
    if filename.endswith(".csv"):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith((".txt", ".xls", ".xlsx")):
        df = pd.read_csv(fl, delimiter='\t', encoding="ISO-8859-1")
    else:
        st.error("Unsupported file format. Please upload a CSV, TXT, XLS, or XLSX file.")
        st.stop()
else:
    # os.chdir(r"C:\Users\nihar.patel\OneDrive - AIVA Partners Pvt. Ltd\Desktop\Work\8QuarterDatabase.csv")
    print("Hello")


fl2 = st.file_uploader(":file_folder: Upload the second text file", type=["txt"])
import streamlit as st
import pandas as pd
import plotly.express as px

# Assuming df is your primary dataframe from the first file upload (8QuarterDatabase or equivalent)
# and df2 is from the second file upload (FOICUC or equivalent)

# Merge dataframes on CU_NUMBER after both files are uploaded
if fl is not None and fl2 is not None:  # Ensure both files are uploaded
    df2 = pd.read_csv(fl2, delimiter=',', quotechar='"', encoding="ISO-8859-1")
    # Merge on CU_NUMBER to include CU_NAME in the main dataframe
    df_combined = pd.merge(df, df2[['CU_NUMBER', 'CU_NAME', 'STATE', 'Peer_Group']], on="CU_NUMBER", how="left")
    
    # Sidebar with CU_NAME selection
    selected_cu_name = st.sidebar.selectbox("Select CU Name", df_combined["CU_NAME"].unique())
    selected_data = df_combined[df_combined["CU_NAME"] == selected_cu_name]

    # Display selected CU's information
    st.title("Credit Union Information Comparison")
    st.subheader(f"Selected CU: {selected_cu_name}")
    st.write(selected_data)

    # Extract the state name for the selected CU for labeling
    selected_state_name = selected_data['STATE'].values[0]

    # Calculations for State and Peer Group
    state_avg_assets = df_combined[df_combined['STATE'] == selected_state_name]['TOTAL ASSETS'].mean()
    peer_group_avg_assets = df_combined[df_combined['Peer_Group'] == selected_data['Peer_Group'].values[0]]['TOTAL ASSETS'].mean()

    # Visualization for the selected CU, its State average, and Peer Group average
    # Update labels to include the name of the CU and the name of the State
    labels = [selected_cu_name, f"Average in {selected_state_name}", "Peer Group Average"]
    values = [selected_data['TOTAL ASSETS'].values[0], state_avg_assets, peer_group_avg_assets]

    fig = px.bar(
        x=labels,
        y=values,
        labels={'x': "Category", 'y': "Total Assets"},
        title="Total Assets Comparison"
    )
    st.plotly_chart(fig)
    
    # Additional visualizations can be added here using a similar approach
else:
    st.warning("Please upload both files to proceed.")
