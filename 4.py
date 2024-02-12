import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Plots!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Credit Union Plots")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Database connection parameters
dbname = "postgres"
user = "postgres"
password = "Aiva@2024"
host = "192.168.1.9"
port = "5432"

@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def load_data_from_db():
    # Connect to your postgres DB
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Load data into DataFrames
    df = pd.read_sql("SELECT * FROM database10year", conn)
    df2 = pd.read_sql("SELECT * FROM branch", conn)

    # Close the connection
    conn.close()
    
    return df, df2

df, df2 = load_data_from_db()

# Merge DataFrames
df_combined = pd.merge(df, df2[['cu_number', 'cu_name', 'statecode', 'peer_group']], on="cu_number", how="left")
    
# Sidebar with CU_NAME selection
selected_cu_name = st.sidebar.selectbox("Select CU Name", df_combined["cu_name"].unique())
selected_data = df_combined[df_combined["cu_name"] == selected_cu_name]

# Display selected CU's information
st.title("Credit Union Information Comparison")
st.subheader(f"Selected CU: {selected_cu_name}")
st.write(selected_data)

# Extract the state name for the selected CU for labeling
selected_state_name = selected_data['statecode'].values[0]

# Calculations for State and Peer Group
state_avg_assets = df_combined[df_combined['statecode'] == selected_state_name]['TOTAL ASSETS'].mean()
peer_group_avg_assets = df_combined[df_combined['peer_group'] == selected_data['peer_group'].values[0]]['TOTAL ASSETS'].mean()

# Visualization for the selected CU, its State average, and Peer Group average
labels = [selected_cu_name, f"Average in {selected_state_name}", "Peer Group Average"]
values = [selected_data['TOTAL ASSETS'].values[0], state_avg_assets, peer_group_avg_assets]

fig = px.bar(x=labels, y=values, labels={'x': "Category", 'y': "Total Assets"}, title="Total Assets Comparison")
st.plotly_chart(fig)
