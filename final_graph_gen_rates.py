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

df_combined = pd.merge(df, df2[['cu_number', 'cu_name', 'statecode', 'peer_group']], on="cu_number", how="left")
    
# Sidebar with CU_NAME selection
selected_cu_name = st.sidebar.selectbox("Select CU Name", df_combined["cu_name"].unique())

# Function to calculate averages and generate plot for a given attribute


# Assume df_combined is preloaded with the appropriate data
# Attribute selection and CU selection are done via sidebar widgets

# Sidebar for quarter selection
quarters = sorted(df_combined['quarter'].unique())
quarter_1 = st.sidebar.selectbox("Select the first quarter", quarters, index=0)
quarter_2 = st.sidebar.selectbox("Select the second quarter", quarters, index=len(quarters)-1)

attributes = [col for col in df_combined.columns if df_combined[col].dtype in ['float64', 'int64']]  # Filter numeric columns
selected_attribute = st.sidebar.selectbox("Select Attribute", attributes)

def calculate_growth_rate(df, attribute, group, group_value, quarter_1, quarter_2):
    # Filter the data for the selected group in the given quarters
    filtered_df = df[(df[group] == group_value) & (df['quarter'].isin([quarter_1, quarter_2]))]
    
    # Get the attribute values for the two quarters
    value_1 = filtered_df[filtered_df['quarter'] == quarter_1][attribute].mean()
    value_2 = filtered_df[filtered_df['quarter'] == quarter_2][attribute].mean()

    # Calculate the growth rate and round it to 2 decimal places
    growth_rate = round(((value_2 - value_1) / value_1) * 100, 2) if value_1 != 0 else 0
    return growth_rate


def calculate_cu_growth_rate(df, attribute, cu_name, quarter_1, quarter_2):
    # Filter the data for the selected CU in the given quarters
    filtered_df = df[(df['cu_name'] == cu_name) & (df['quarter'].isin([quarter_1, quarter_2]))]

    # Ensure the data is correctly filtered and we have the values for both quarters
    if filtered_df['quarter'].nunique() == 2:
        # Get the attribute values for the two quarters
        value_1 = filtered_df[filtered_df['quarter'] == quarter_1][attribute].iloc[0]
        value_2 = filtered_df[filtered_df['quarter'] == quarter_2][attribute].iloc[0]

        # Calculate the growth rate and round it to 2 decimal places
        growth_rate = round(((value_2 - value_1) / value_1) * 100, 2) if value_1 != 0 else 0
    else:
        # If we don't have both values, we cannot calculate the growth rate
        growth_rate = None
    
    return growth_rate


# Get the selected CU's state code and peer group
selected_state_code = df_combined[df_combined['cu_name'] == selected_cu_name]['statecode'].iloc[0]
selected_peer_group = df_combined[df_combined['cu_name'] == selected_cu_name]['peer_group'].iloc[0]

# Calculate growth rates
cu_growth_rate = calculate_cu_growth_rate(df_combined, selected_attribute, selected_cu_name, quarter_1, quarter_2)

state_growth_rate = calculate_growth_rate(df_combined, selected_attribute, 'statecode', selected_state_code, quarter_1, quarter_2)
peer_group_growth_rate = calculate_growth_rate(df_combined, selected_attribute, 'peer_group', selected_peer_group, quarter_1, quarter_2)

# Data for plotting
growth_data = {
    'Category': ['CU', 'State', 'Peer Group'],
    'Growth Rate': [cu_growth_rate, state_growth_rate, peer_group_growth_rate]
}

growth_df = pd.DataFrame(growth_data)

# Plotting the bar chart
fig = px.bar(growth_df, x='Category', y='Growth Rate', 
             title=f"Growth Rate of {selected_attribute} from {quarter_1} to {quarter_2}",
             labels={'Growth Rate': 'Growth Rate (%)'},
             text=growth_df['Growth Rate'].apply(lambda x: f"{x:.2f}%"))

# Customize the layout with a specified figure size
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title='Category'),
    yaxis=dict(title='Growth Rate (%)'),
    title=dict(x=0.5),
    title_font=dict(size=22, color='darkblue', family="Arial, sans-serif"),
    font=dict(family="Arial, sans-serif", size=18, color="RebeccaPurple"),
    height=600,  # Set the height of the figure
    width=800,   # Set the width of the figure
)

# Customize bar colors
fig.update_traces(marker_color=['#19618A', '#005950', '#09B39C'])

st.plotly_chart(fig, use_container_width=True)
# Customize bar colors




# Extracting the state_code and peer_group for the selected CU
selected_state_code = df_combined[df_combined['cu_name'] == selected_cu_name]['statecode'].iloc[0]
selected_peer_group = df_combined[df_combined['cu_name'] == selected_cu_name]['peer_group'].iloc[0]

# plot_growth_rates(df_combined, selected_cu_name, selected_attribute, selected_state_code, selected_peer_group, 'quarter')

