import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Credit Union Analysis", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Credit Union Analysis")
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

categories = {
    "Loans and Leases": [
        "Total number of loans and leases", 
        "Total amount of loans and leases", 
        "Number of Used Vehicle Loans", 
        "Amount of Used Vehicle Loans", 
        "Amount of new vehicle loans", 
        "Number of new Vehicle loans", 
        "TOTAL OTHER LOANS"
    ],
    "Share and Deposits": [
        "TOTAL AMOUNT OF SHARES AND DEPOSITS", 
        "Money Market (Amount)", 
        "Amount of Total Share Draft", 
        "Total Number of money market shares", 
        "TOTAL AMOUNT OF SHARES"
    ],
    "Delinquency": [
        "Deliquent Credit card loans (Amount) 0-180", 
        "Deliquent Credit card loans (Amount) 180+"
    ],
    "Membership and Financial Overview": [
        "NO OF MEMBERS", 
        "Number of Total Share Draft",
        "TOTAL ASSETS"
    ]
}



selected_category = st.sidebar.selectbox("Select Category", list(categories.keys()))

# Display the title of the selected category in h1 font size at the center of the page
st.markdown(f"<h1 style='text-align: center; color: black;'>{selected_category}</h1>", unsafe_allow_html=True)


def generate_comparison_plot(selected_cu_name, attribute, quarter, height=300, width=250):
    df_quarter = df_combined[df_combined['quarter'] == quarter]
    
    # Extract the data for the selected CU
    selected_data = df_quarter[df_quarter['cu_name'] == selected_cu_name]

    # Extract the state name and peer group for labeling
    selected_state_name = selected_data['statecode'].values[0]
    selected_peer_group = selected_data['peer_group'].values[0]

    # Calculations for State and Peer Group based on the filtered data
    state_avg = df_quarter[df_quarter['statecode'] == selected_state_name][attribute].mean()
    peer_group_avg = df_quarter[df_quarter['peer_group'] == selected_peer_group][attribute].mean()

    # Get value for the selected CU
    selected_cu_value = selected_data[attribute].values[0] if not selected_data.empty else 0

    # Visualization for the selected CU, its State average, and Peer Group average
    labels = [f"{selected_cu_name}", f"Average in {selected_state_name}", "Peer Group Average"]
    values = [selected_cu_value, state_avg, peer_group_avg]

    fig = px.bar(
        x=labels, 
        y=values, 
        labels={'x': "Category", 'y': attribute},
        text=values,
        color=labels,
        color_discrete_map={
            labels[0]: '#19618A', 
            labels[1]: '#005950', 
            labels[2]: '#09B39C'
        }
    )

    # Improve layout and add custom hover text
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title=attribute),
        showlegend=False,
        height=height,  # Use the height argument
        width=width,    # Use the width argument
        margin=dict(l=10, r=10, t=20, b=20)
    )
    
    fig.update_traces(
        texttemplate='%{x}: %{y:.2f}', 
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{y:.2f}'
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=False)




# Sidebar with attribute selection




def generate_multiple_plots(selected_cu_name, df, selected_category, selected_quarter):
    # Filter the DataFrame for the selected quarter
    columns_to_plot = categories[selected_category]

    # Create a grid layout with 4 columns
    num_columns = 3  # Number of columns in the grid

    # Create container columns for the layout
    cols = st.columns(num_columns)

    # Iterate over the columns to plot and create a plot for each one
    for index, attribute in enumerate(columns_to_plot):
        with cols[index % num_columns]:
            st.markdown(f"#### {attribute} Comparison for {selected_quarter}")
            generate_comparison_plot(selected_cu_name, attribute, selected_quarter, height=300, width=250)




# Call the function to generate multiple plots
# Ensure df_combined is filtered by the selected CU before passing it
selected_quarter = st.sidebar.selectbox("Select Quarter", sorted(df_combined['quarter'].unique()))
generate_multiple_plots(selected_cu_name, df_combined, selected_category, selected_quarter)


