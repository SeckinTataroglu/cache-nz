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

def unique_months_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "Month" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    month_list = df.loc[:, "Month"].tolist()
    conn.close()
    return month_list

def unique_dayname_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "DayName" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    dayname_list = df.loc[:, "DayName"].tolist()
    conn.close()
    return dayname_list


def selection_to_tuple(selection):
    if len(selection) == 1:
        selection_str = str(tuple(selection))[:-2]+")"
    else:
        selection_str = str(tuple(selection))
    return selection_str



def selected_vessels_df(selected_vessels, 
                        selected_ais_class, 
                        selected_riccardo_class, 
                        selected_movement,
                        selected_month,
                        selected_dayname
                        ):
    conn = sqlite3.connect(db_path)
    
    # selections
    selected_vessels_str = selection_to_tuple(selected_vessels)
    selected_ais_class_str = selection_to_tuple(selected_ais_class)
    selected_riccardo_class_str = selection_to_tuple(selected_riccardo_class)
    selected_movement_str = selection_to_tuple(selected_movement)
    selected_month_str = selection_to_tuple(selected_month)
    selected_dayname_str = selection_to_tuple(selected_dayname)
    
    query = f"""select * from {table_name} 
                where "Vessel Name" in {selected_vessels_str} 
                and "TYPE_NAME" in {selected_ais_class_str}
                and "Riccardo Class" in {selected_riccardo_class_str}
                and "Movement_Type" in {selected_movement_str}
                and "Month" in {selected_month_str}
                and "DayName" in {selected_dayname_str}
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
    selected_vessels = st.multiselect("Select Vessels:",["All", "---"] + unique_vessels, default=["All"])
    if "All" in selected_vessels:
        selected_vessels = unique_vessels

    # AIS Class
    unique_ais_class = unique_ais_class_list()
    selected_ais_class = st.multiselect("Select AIS Class (TYPE_NAME):",["All", "---"] + unique_ais_class, default=["All"])
    if "All" in selected_ais_class:
        selected_ais_class = unique_ais_class
    
    # Riccardo Class
    unique_riccardo_class = unique_riccardo_class_list()
    selected_riccardo_class = st.multiselect("Select Riccardo Class:",["All", "---"] + unique_riccardo_class, default=["All"])
    if "All" in selected_riccardo_class:
        selected_riccardo_class = unique_riccardo_class

    # Inbound Berth Outbound
    selected_movement = st.multiselect("Select Movement:",["All", "---", "Inbound", "Berth", "Outbound"], default=["All"])
    if "All" in selected_movement:
        selected_movement = ["Inbound", "Berth", "Outbound"]

    # Month
    unique_months = unique_months_list()
    selected_month = st.multiselect("Select Months:",["All", "---",] + unique_months, default=["All"])
    if "All" in selected_month:
        selected_month = unique_months

    # Day of Week
    unique_dayname = unique_dayname_list()
    selected_dayname = st.multiselect("Select Days of Week:",["All", "---",] + unique_dayname, default=["All"])
    if "All" in selected_dayname:
        selected_dayname = unique_dayname

    
    



    fetch_button = st.button('Fetch Data')

if fetch_button:
    # st.write(selected_vessels)
    selected_vessels_df_ = selected_vessels_df(selected_vessels=selected_vessels,
                                               selected_ais_class=selected_ais_class,
                                               selected_riccardo_class=selected_riccardo_class,
                                               selected_movement=selected_movement,
                                               selected_month=selected_month,
                                               selected_dayname=selected_dayname)
    st.write(selected_vessels_df_)





# df = read_git_db()
# st.write(df)

# if __name__ == '__main__':
#     main()
