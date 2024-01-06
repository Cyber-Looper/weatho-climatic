import streamlit as st
import plotly.express as px
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Title
st.set_page_config(page_title="Weatho-Climatic Analytics", page_icon=":bar_chart:", layout="wide")

# Heading
st.title(":sun_behind_rain_cloud: Weather and Climate Forecasting, USA.")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Upload a dataset
file = st.file_uploader(":file_folder: Upload a dataset", type=(["csv", "txt", "xlsx", "xls"]))
if file is not None:
    filename = file.name
    data = pd.read_csv(filename)
    st.write(data)
else:
    data = pd.read_csv("/mount/src/weatho-climatic/WeatherClimateAnalytics/dataset/upd_forecast_data.csv")
    st.write(data)

# Sidebar
st.sidebar.header("Apply your filter: ")

# Choose Region
region = st.sidebar.multiselect("Choose your region", data["Region"].unique())
if not region:
    data2 = data.copy()
else:
    data2 = data[data["Region"].isin(region)]

# Choose State
state = st.sidebar.multiselect("Choose your state", data2["State"].unique())
if not state:
    data3 = data2.copy()
else:
    data3 = data2[data2["State"].isin(state)]

# Choose City
city = st.sidebar.multiselect("Choose your city", data3["City"].unique())

# Filter the data based on Region, State and City
if not region and not state and not city:
    filtered_data = data
elif not state and not city:
    filtered_data = data[data["Region"].isin(region)]
elif not region and not city:
    filtered_data = data[data["State"].isin(state)]
elif state and city:
    filtered_data = data3[data["State"].isin(state) & data3["City"].isin(city)]
elif region and city:
    filtered_data = data3[data["Region"].isin(region) & data3["City"].isin(city)]
elif region and state:
    filtered_data = data3[data["Region"].isin(region) & data3["State"].isin(state)]
elif city:
    filtered_data = data3[data3["City"].isin(city)]
else:
    filtered_data = data3[data3["Region"].isin(region) & data3["State"].isin(state) & data3["City"].isin(city)]

filtered_data1 = filtered_data.copy()

# Line chart with Avg Temp. per Day

# Convert 'DATE_VALID_STD' column to datetime
filtered_data1['DATE_VALID_STD'] = pd.to_datetime(filtered_data1['DATE_VALID_STD'], format='%d-%m-%Y')
# filtered_data["DATE_VALID_STD"] = filtered_data["DATE_VALID_STD"].dt.to_period("M")
st.subheader('Air Temperature on a Daily Basis')
# Create a radio button
Options = ["AVG_TEMPERATURE_AIR_2M_F", "MIN_TEMPERATURE_AIR_2M_F", "MAX_TEMPERATURE_AIR_2M_F"]
selected_option = st.radio("**Temperature**", Options)

if selected_option == "AVG_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_data1.groupby(filtered_data1["DATE_VALID_STD"].dt.strftime("%Y %b %d"))[
                                 "AVG_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Average Temperature for Air", "DATE_VALID_STD": "Days"}, height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "MAX_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_data1.groupby(filtered_data1["DATE_VALID_STD"].dt.strftime("%Y %b %d"))[
                                 "MAX_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Maximum Temperature for Air", "DATE_VALID_STD": "Days"}, height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "MIN_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_data1.groupby(filtered_data1["DATE_VALID_STD"].dt.strftime("%Y %b %d"))[
                                 "MIN_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Minimum Temperature for Air", "DATE_VALID_STD": "Days"}, height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)

# Monthly Precipitation based on state

# st.subheader("Category wise Sales")
#     fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
#                  template = "seaborn")
#     st.plotly_chart(fig,use_container_width=True, height = 200)