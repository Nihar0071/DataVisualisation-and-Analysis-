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

def generate_comparison_plot(selected_cu_name, attribute, height=300, width=250):
    selected_data = df_combined[df_combined['cu_name'] == selected_cu_name]

    # Extract the state name and peer group for labeling
    selected_state_name = selected_data['statecode'].values[0]
    selected_peer_group = selected_data['peer_group'].values[0]

    # Calculations for State and Peer Group
    state_avg = df_combined[df_combined['statecode'] == selected_state_name][attribute].mean()
    peer_group_avg = df_combined[df_combined['peer_group'] == selected_peer_group][attribute].mean()

    # Get value for the selected CU
    selected_cu_value = selected_data[attribute].values[0] if not selected_data.empty else 0

    # Visualization for the selected CU, its State average, and Peer Group average
    labels = [f"{selected_cu_name}", f"Average in {selected_state_name}", "Peer Group Average"]
    values = [selected_cu_value, state_avg, peer_group_avg]

    fig = px.bar(
        x=labels, 
        y=values, 
        labels={'x': "Category", 'y': attribute}, 
        # title=f"{attribute} Comparison",
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
        showlegend=False,  # Remove the legend
        height=height, width=width,  # Set height and width
        margin=dict(l=10, r=10, t=20, b=20)  # Tighter margins
    )
    
    fig.update_traces(
        texttemplate='%{x}: %{y:.2f}', 
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{y:.2f}'
    )

    # Show the plot with a fixed width
    st.plotly_chart(fig, use_container_width=False)



# Sidebar with attribute selection




def generate_multiple_plots(selected_cu_name, df):
    # Filter numeric columns
    # plot_height = 250  # Reduced height for a better aspect ratio
    # plot_width = 250
    numeric_attributes = [col for col in df.columns[1:] if df[col].dtype in ['float64', 'int64']]

    # Create a grid layout with 4 columns
    num_columns = 3  # Number of columns in the grid
    
    # Calculate the number of rows needed
    num_rows = len(numeric_attributes) // num_columns + (1 if len(numeric_attributes) % num_columns else 0)
    
    # Adjust the size of each plot to fit in the layout
    plot_height = max(300, 800 // num_rows)  # Adjust the height dynamically based on the number of rows
    plot_width = 250  # Adjust the width to fit 4 plots in a row

    # Iterate over the numeric attributes and create a plot for each
    for index, attribute in enumerate(numeric_attributes):
        if index % num_columns == 0:
            cols = st.columns(num_columns)
        with cols[index % num_columns]:
            st.markdown(f"#### {attribute} Comparison")
            generate_comparison_plot(selected_cu_name, attribute, plot_height, plot_width)

# Call the function to generate multiple plots
generate_multiple_plots(selected_cu_name, df_combined)




