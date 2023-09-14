from email.policy import default
from lib2to3.pgen2.pgen import DFAState
from logging import PlaceHolder
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px



st.set_page_config(layout="wide")
st.maxMessageSize = 300

db_path = "./data/data.db"
table_name = 'AIS_2023_May'


# Function to fetch a list of stock symbols from a file or API

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
    dayname_list_default = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayname_list = df.loc[:, "DayName"].tolist()
    dayname_list = sorted(dayname_list, key=dayname_list_default.index)
    conn.close()

    

    return dayname_list


def unique_hours_list():
    conn = sqlite3.connect(db_path)
    query = f"""select distinct "Hour" from {table_name}"""
    df = pd.read_sql(query, con=conn)
    hours_list = df.loc[:, "Hour"].tolist()
    hours_list.sort()
    conn.close()
    return hours_list


@st.cache_data
def selection_to_tuple(selection):
    if len(selection) == 1:
        selection_str = str(tuple(selection))[:-2]+")"
    else:
        selection_str = str(tuple(selection))
    return selection_str


@st.cache_data
def selected_vessels_df(selected_vessels, 
                        selected_ais_class, 
                        selected_riccardo_class, 
                        selected_movement,
                        selected_month,
                        selected_dayname,
                        selected_hours
                        ):
    conn = sqlite3.connect(db_path)
    
    # selections
    selected_vessels_str = selection_to_tuple(selected_vessels)
    selected_ais_class_str = selection_to_tuple(selected_ais_class)
    selected_riccardo_class_str = selection_to_tuple(selected_riccardo_class)
    selected_movement_str = selection_to_tuple(selected_movement)
    selected_month_str = selection_to_tuple(selected_month)
    selected_dayname_str = selection_to_tuple(selected_dayname)
    selected_hours_str = selection_to_tuple(selected_hours)
    
    # "Vessel Name", "IMO", "TYPE_NAME", "Riccardo Class", "Speed (knots)",
    # "LAT", "LON", "COURSE", "HEADING", "TIMESTAMP UTC", "JourneyID", "Movement_Type", 
    # "Speed in m/s", "Avg Speed per Time Increment",	"Avg Acceleration DV/DT",
    # "V/Vst", "tmp_Load_Pi_Pmax (V/Vst)^3", "Power Steady State (kW)",
    # "Accn DV/DT m/sec^2", "V*DV/DT", "Acceleration Power (kW)", "Aux Engine Power (kW)",
    # "Total Instantaneous Power (kW)", "Total Energy Consumption (kWh)", "Total Fuel Consumption (kG)",
    # "Total NOx Emission (kG)", "Total PM2.5 Emissions (kG)", "Total PM10 Emissions (kG)", "Total SO2 Emissions (kG)",
    # "Total CO2 Emissions (kG)", "Total CO2 Emissions (kG) from FC", "X_centre", "Y_centre", "Month", "DayName", "Hour"


    query = f"""select 
                "Vessel Name", "TYPE_NAME", "Riccardo Class", 
                "TIMESTAMP UTC", "Movement_Type", 
                "Total NOx Emission (kG)", "Total PM2.5 Emissions (kG)", "Total PM10 Emissions (kG)", "Total SO2 Emissions (kG)",
                "Total CO2 Emissions (kG)", "Total CO2 Emissions (kG) from FC", "Month", "DayName", "Hour"

                from {table_name} 
                where "Vessel Name" in {selected_vessels_str} 
                and "TYPE_NAME" in {selected_ais_class_str}
                and "Riccardo Class" in {selected_riccardo_class_str}
                and "Movement_Type" in {selected_movement_str}
                and "Month" in {selected_month_str}
                and "DayName" in {selected_dayname_str}
                and "Hour" in {selected_hours_str}
                """
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df


emissions_type_abbr = {"NOx": "Total NOx Emission (kG)",
                       "PM25": "Total PM2.5 Emissions (kG)",
                       "PM10": "Total PM10 Emissions (kG)",
                       "SO2": "Total SO2 Emissions (kG)",
                       "CO2": "Total CO2 Emissions (kG)",
                       "CO2 from FC": "Total CO2 Emissions (kG) from FC",
                       }

db_table_mapping = {
    "AIS 2023 May": "AIS_2023_May",
    "AIS 2022 Annual": "AIS_2022_Annual" 
}


# Streamlit app
# def main():

# st.title('DF')



# Set the layout to 'wide' to allow more space for the sidebar
with st.sidebar:
# Create a sidebar for the dropdowns
    # st.sidebar.title("Parameters")

    # Dataset Selection
    unique_tables = ("AIS 2023 May", "AIS 2022 Annual")
    selected_table = st.selectbox("Select Dataset:", unique_tables)
    table_name = db_table_mapping[selected_table]

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

    # Hour of Day
    unique_hours = unique_hours_list()
    selected_hours = st.multiselect("Select Hour of Day:",["All", "---",] + unique_hours, default=["All"])
    if "All" in selected_hours:
        selected_hours = unique_hours

    # Emission Type
    selected_emission_type = st.selectbox("Select Emission Type:",["NOx", "PM25", "PM10", "SO2", "CO2", "CO2 from FC"])





    fetch_button = st.button('Fetch Data')


# OUTPUTS
tab1, tab2, tab3, tab4 = st.tabs(["Graphs (Total)", "Graphs (Avg)", "Raw Data", "Selected Vessels' List"])
# with tab1:
#     st.title("Graphs")
# with tab2:
#     st.title("Raw Data")


# FETCH DATA
if fetch_button:
    # RAW DATA
    selected_vessels_df_ = selected_vessels_df(selected_vessels=selected_vessels,
                                               selected_ais_class=selected_ais_class,
                                               selected_riccardo_class=selected_riccardo_class,
                                               selected_movement=selected_movement,
                                               selected_month=selected_month,
                                               selected_dayname=selected_dayname,
                                               selected_hours=selected_hours)
    selected_vessels_df_['TIMESTAMP UTC'] = pd.to_datetime(selected_vessels_df_['TIMESTAMP UTC'])
    
    # GROUPING DFs
    # Day by Day
    grouped_month_df = selected_vessels_df_.groupby(selected_vessels_df_['Month'])[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    grouped_month_df.columns = ['Month', selected_emission_type]
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    all_months_df = pd.DataFrame({"Month": month_order})
    grouped_month_df = all_months_df.merge(grouped_month_df, on="Month", how='left').fillna(0)
    grouped_month_df['Month'] = pd.Categorical(grouped_month_df['Month'], categories=month_order, ordered=True)

    # Day by Day
    grouped_day_df = selected_vessels_df_.groupby(selected_vessels_df_['TIMESTAMP UTC'].dt.date)[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    start_date = selected_vessels_df_['TIMESTAMP UTC'].min().date()  # Start date from the data
    end_date = selected_vessels_df_['TIMESTAMP UTC'].max().date()    # End date from the data
    date_range = pd.date_range(start=start_date, end=end_date)
    grouped_day_df = grouped_day_df.set_index('TIMESTAMP UTC').reindex(date_range, fill_value=0).reset_index()
    grouped_day_df.columns = ['Date', selected_emission_type]

    # Days of Week
    grouped_days_week_df = selected_vessels_df_.groupby(selected_vessels_df_['DayName'])[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    grouped_days_week_df.columns = ['Day Name', selected_emission_type]
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_days_df = pd.DataFrame({"Day Name": day_order})
    grouped_days_week_df = all_days_df.merge(grouped_days_week_df, on="Day Name", how='left').fillna(0)
    grouped_days_week_df['Day Name'] = pd.Categorical(grouped_days_week_df['Day Name'], categories=day_order, ordered=True)
    # grouped_days_week_df = grouped_days_week_df.sort_values(by='Day Name').reset_index(drop=True)

    # Hours of Day
    grouped_hours_day_df = selected_vessels_df_.groupby(selected_vessels_df_['Hour'])[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    grouped_hours_day_df.columns = ['Hours', selected_emission_type]
    grouped_hours_day_df = grouped_hours_day_df.sort_values(by="Hours")

    grouped_hourly_sums = selected_vessels_df_.groupby([selected_vessels_df_['TIMESTAMP UTC'].dt.date, 'Hour'])[emissions_type_abbr[selected_emission_type]].sum().reset_index()
    # grouped_hours_day_daily_averages = grouped_hourly_sums.groupby('Hour')[emissions_type_abbr[selected_emission_type]].mean().reset_index()
    # grouped_hours_day_daily_averages.columns = ['Hours', selected_emission_type]
    # grouped_hours_day_daily_averages = grouped_hours_day_daily_averages.sort_values(by="Hours")

    # AIS Class Type
    grouped_AIS_Class_df = selected_vessels_df_.groupby(selected_vessels_df_['TYPE_NAME'])[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    grouped_AIS_Class_df.columns = ["AIS Class", selected_emission_type]
    grouped_AIS_Class_df.sort_values("AIS Class")

    # Riccardo Class Type
    grouped_Riccardo_Class_df = selected_vessels_df_.groupby(selected_vessels_df_['Riccardo Class'])[emissions_type_abbr[selected_emission_type]].sum().reset_index().round(2)
    grouped_Riccardo_Class_df.columns = ["Riccardo Class", selected_emission_type]
    grouped_Riccardo_Class_df.sort_values("Riccardo Class")

 
    # DASHBOARD LAYOUT
    with tab1:
        # Month by Month Container
        with st.container():
            st.subheader(f"Month by Month {selected_emission_type} (kG)")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.bar_chart(grouped_month_df,
                                x = 'Month',
                                y = [selected_emission_type],
                                # y = [f"{selected_emission_type} (Sum)"],
                            )  # Optional color = ['#FF0000', '#0000FF']
                # st.write("graph")
            with col2:
                st.write(grouped_month_df.set_index("Month"))

        # Days of Week Container
        with st.container():
            st.subheader(f"Days of Week {selected_emission_type} (kG)")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.bar_chart(grouped_days_week_df,
                                x = 'Day Name',
                                y = [selected_emission_type],
                            )  # Optional color = ['#FF0000', '#0000FF']
            with col2:
                st.write(grouped_days_week_df.set_index("Day Name"))

        # Day by Day Container
        with st.container():
            st.subheader(f"Day by Day {selected_emission_type} (kG)")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.bar_chart(grouped_day_df,
                                x = 'Date',
                                y = [selected_emission_type],
                                # y = [f"{selected_emission_type} (Sum)"],
                            )  # Optional color = ['#FF0000', '#0000FF']
            with col2:
                st.write(grouped_day_df.set_index("Date"))

        # Hours of Day Container
        with st.container():
            st.subheader(f"Hours of Day {selected_emission_type} (kG)")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.bar_chart(grouped_hours_day_df,
                                x = 'Hours',
                                y = [selected_emission_type],
                            )  # Optional color = ['#FF0000', '#0000FF']
                # st.bar_chart(rouped_hours_day_daily_averages,
                #                 x = 'Hours',
                #                 y = [selected_emission_type],
                #             )  # Optional color = ['#FF0000', '#0000FF']
            with col2:
                st.write(grouped_hours_day_df.set_index("Hours"))
                # st.write(grouped_hours_day_daily_averages)
        
        # AIS Pie Chart Container
        with st.container():
            st.subheader(f"Emissions Proportions by AIS Class")
            col1, col2 = st.columns([4, 1])
            with col1:
                # st.write("pie chart")
                fig = px.pie(grouped_AIS_Class_df, values=selected_emission_type, names='AIS Class') #title='AIS Class Division'
                # fig.show()
                st.plotly_chart(fig)
            
            with col2:
                st.write(grouped_AIS_Class_df.set_index("AIS Class"))

        # Riccardo Pie Chart Container
        with st.container():
            st.subheader(f"Emissions Proportions by Riccardo Class")
            col1, col2 = st.columns([4, 1])
            with col1:
                # st.write("pie chart")
                fig = px.pie(grouped_Riccardo_Class_df, values=selected_emission_type, names='Riccardo Class') #title='AIS Class Division'
                # fig.show()
                st.plotly_chart(fig)
            
            with col2:
                st.write(grouped_Riccardo_Class_df.set_index("Riccardo Class"))


    with tab2:
        # Day by Day Container
        st.write("Daily Averages can be added here if needed...")
        # with st.container():
        #     st.subheader(f"Day by Day {selected_emission_type} (kG)")
        #     col1, col2 = st.columns([4, 1])
        #     with col1:
        #         st.bar_chart(grouped_day_df,
        #                         x = 'Date',
        #                         y = [selected_emission_type],
        #                         # y = [f"{selected_emission_type} (Sum)"],
        #                     )  # Optional color = ['#FF0000', '#0000FF']
        #     with col2:
        #         st.write(grouped_day_df)

        # # Days of Week Container
        # with st.container():
        #     st.subheader(f"Days of Week {selected_emission_type} (kG)")
        #     col1, col2 = st.columns([4, 1])
        #     with col1:
        #         st.bar_chart(grouped_days_week_df,
        #                         x = 'Day Name',
        #                         y = [selected_emission_type],
        #                     )  # Optional color = ['#FF0000', '#0000FF']
        #     with col2:
        #         st.write(grouped_days_week_df)

        # # Hours of Day Container
        # with st.container():
        #     st.subheader(f"Hours of Day {selected_emission_type} (kG)")
        #     col1, col2 = st.columns([4, 1])
        #     with col1:
        #         st.bar_chart(grouped_hours_day_df,
        #                         x = 'Hours',
        #                         y = [selected_emission_type],
        #                     )  # Optional color = ['#FF0000', '#0000FF']
        #         st.bar_chart(grouped_hours_day_daily_averages,
        #                         x = 'Hours',
        #                         y = [selected_emission_type],
        #                     )  # Optional color = ['#FF0000', '#0000FF']
        #     with col2:
        #         st.write(grouped_hours_day_df)
        #         st.write(grouped_hours_day_daily_averages)



        

    with tab3:
        # st.write(selected_vessels_df_)
        st.write("Raw Data can be added here if needed")

    with tab4:
        st.write(pd.DataFrame(selected_vessels_df_["Vessel Name"].unique().tolist(), columns=["Vessels"]))





# df = read_git_db()
# st.write(df)

# if __name__ == '__main__':
#     main()
