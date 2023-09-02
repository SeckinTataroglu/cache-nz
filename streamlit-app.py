import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

db_path = "./data/data.db"
table_name = 'raw_data_20230815'


# Function to fetch a list of stock symbols from a file or API
# def read_git_db():
#     conn = sqlite3.connect(db_path)
#     # Check if the table already exists in the database
#     query = f"""select distinct "Vessel Name" from {table_name}"""
    
#     df = pd.read_sql(query, con=conn)

#     conn.close()
#     return df

def unique_vessels_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "Vessel Name" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    vessels_list = df.loc[:, "Vessel Name"].tolist()
    conn.close()
    return vessels_list

def unique_ais_class_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "TYPE_NAME" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    ais_class_list = df.loc[:, "TYPE_NAME"].tolist()
    conn.close()
    return ais_class_list

def unique_riccardo_class_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "Riccardo Class" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    category_list = df.loc[:, "Riccardo Class"].tolist()
    conn.close()
    return category_list


def selected_vessels_df(selected_vessels, 
                        selected_ais_class, 
                        selected_riccardo_class, 
                        selected_movement):
    conn = sqlite3.connect(db_path)
    # selected vessels
    if len(selected_vessels) == 1:
        selected_vessels_str = str(tuple(selected_vessels))[:-2]+")"
    else:
        selected_vessels_str = str(tuple(selected_vessels))

    # selected riccardo class
    if len(selected_ais_class) == 1:
        selected_ais_class_str = str(tuple(selected_ais_class))[:-2]+")"
    else:
        selected_ais_class_str = str(tuple(selected_ais_class))

    # selected riccardo class
    if len(selected_riccardo_class) == 1:
        selected_riccardo_class_str = str(tuple(selected_riccardo_class))[:-2]+")"
    else:
        selected_riccardo_class_str = str(tuple(selected_riccardo_class))
    
    # selected movements
    if len(selected_movement) == 1:
        selected_movement_str = str(tuple(selected_movement))[:-2]+")"
    else:
        selected_movement_str = str(tuple(selected_movement))
    
    query = f"""select * from {table_name} 
                where "Vessel Name" in {selected_vessels_str} 
                and "TYPE_NAME" in {selected_ais_class_str}
                and "Riccardo Class" in {selected_riccardo_class_str}
                and "Movement_Type" in {selected_movement_str}
                limit 10000"""
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df




# Streamlit app
# def main():

# st.title('DF')



# Set the layout to 'wide' to allow more space for the sidebar
with st.sidebar:
# Create a sidebar for the dropdowns
    st.sidebar.title("Parameters")

    # Vessels List
    unique_vessels = unique_vessels_list()
    selected_vessels = st.multiselect("Select Vessels:",["All"] + ["---"] + unique_vessels, default=["All"])
    if "All" in selected_vessels:
        selected_vessels = unique_vessels

    # AIS Class
    unique_ais_class = unique_ais_class_list()
    selected_ais_class = st.multiselect("Select AIS Class (TYPE_NAME):",["All"] + ["---"] + unique_ais_class, default=["All"])
    if "All" in selected_ais_class:
        selected_ais_class = unique_ais_class
    
    # Riccardo Class
    unique_riccardo_class = unique_riccardo_class_list()
    selected_riccardo_class = st.multiselect("Select Riccardo Class:",["All"] + ["---"] + unique_riccardo_class, default=["All"])
    if "All" in selected_riccardo_class:
        selected_riccardo_class = unique_riccardo_class

    # Inbound Berth Outbound
    selected_movement = st.multiselect("Select Movement:",["All", "---", "Inbound", "Berth", "Outbound"], default=["All"])
    if "All" in selected_movement:
        selected_movement = ["Inbound", "Berth", "Outbound"]

    
    



    fetch_button = st.button('Fetch Data')

if fetch_button:
    # st.write(selected_vessels)
    selected_vessels_df_ = selected_vessels_df(selected_vessels=selected_vessels,
                                               selected_ais_class=selected_ais_class,
                                               selected_riccardo_class=selected_riccardo_class,
                                               selected_movement=selected_movement)
    st.write(selected_vessels_df_)





# df = read_git_db()
# st.write(df)

# if __name__ == '__main__':
#     main()
