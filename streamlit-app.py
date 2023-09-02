import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

db_path = "./data/data.db"
table_name = 'raw_data_20230815'


# Function to fetch a list of stock symbols from a file or API
def read_git_db():
    conn = sqlite3.connect(db_path)
    # Check if the table already exists in the database
    query = f"""select distinct "Vessel Name" from {table_name}"""
    
    df = pd.read_sql(query, con=conn)

    conn.close()
    return df

def unique_vessels_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "Vessel Name" from {table_name}"""
    
    df = pd.read_sql(query, con=conn)
    vessels_list = df.loc[:, "Vessel Name"].tolist()
    conn.close()
    return vessels_list


def selected_vessels_df(selected_vessels):
    conn = sqlite3.connect(db_path)
    if len(selected_vessels) == 1:
        selected_vessels_str = str(tuple(selected_vessels))[:-2]+")"
    else:
        selected_vessels_str = str(tuple(selected_vessels))
    query = f"""select * from {table_name} where "Vessel Name" in {selected_vessels_str} limit 10000"""
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df




# Streamlit app
# def main():

st.title('DF')



# Set the layout to 'wide' to allow more space for the sidebar
with st.sidebar:
# Create a sidebar for the dropdowns
    st.sidebar.title("Parameters")

    # container = st.container()
    unique_vessels = unique_vessels_list()
    # all = st.checkbox("Select all", value=True)

    # if all:
    #     selected_options = container.multiselect("Select Vessels:", unique_vessels, unique_vessels)
    # else:
    #     selected_options =  container.multiselect("Select Vessels:", unique_vessels)


    selected_vessels = st.multiselect("Select one or more options:",["All"] + ["---"] + unique_vessels)

    if "All" in selected_vessels:
        selected_vessels = unique_vessels
    
    



    fetch_button = st.button('Fetch Data')

if fetch_button:
    st.write(selected_vessels)
    selected_vessels_df_ = selected_vessels_df(selected_vessels=selected_vessels)
    st.write(selected_vessels_df_)





df = read_git_db()
st.write(df)

# if __name__ == '__main__':
#     main()
