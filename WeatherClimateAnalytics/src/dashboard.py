import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import warnings

warnings.filterwarnings('ignore')

# Title
st.set_page_config(page_title="Weatho-Climatic Analytics", page_icon=":bar_chart:", layout="wide")

# Heading
st.title(":sun_behind_rain_cloud: Weather and Climate Forecasting, USA.")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# data = pd.read_csv('../dataset/upd_forecast_data.csv')
data = pd.read_csv('/mount/src/weatho-climatic/WeatherClimateAnalytics/dataset/upd_forecast_data.csv')
# st.dataframe(data)

# SideBar
st.sidebar.subheader('Apply Filters:')

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

# Main KPI's
total_precipitation = int(filtered_data1["TOT_PRECIPITATION_IN"].sum())
total_snowfall = int(filtered_data1["TOT_SNOWFALL_IN"].sum())
total_solar_radiation = int(filtered_data1["TOT_RADIATION_SOLAR_TOTAL_WPM2"].sum())

# page layout
left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader("***Total precipitation***")
    st.subheader(f":sun_behind_rain_cloud: {total_precipitation}")
with mid_col:
    st.subheader("***Total snowfall***")
    st.subheader(f":snow_cloud: {total_snowfall}")
with right_col:
    st.subheader("***Total solar radiation***")
    st.subheader(f":mostly_sunny: {total_solar_radiation}")

st.markdown("---")

# Line chart for Avg Temp. per Day

# Convert 'DATE_VALID_STD' column to datetime
filtered_data1['DATE_VALID_STD'] = pd.to_datetime(filtered_data1['DATE_VALID_STD'], format='%d-%m-%Y')
st.subheader('Air Temperature on a Daily Basis')

# Create a radio button
Options = ["AVG_TEMPERATURE_AIR_2M_F", "MIN_TEMPERATURE_AIR_2M_F", "MAX_TEMPERATURE_AIR_2M_F"]
selected_option = st.radio("***Temperatures***", Options)

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


# WindRose chart for Minimal and Maximum WindSpeed Variance By Region
st.subheader('WindSpeed Variance By Region')

# Create a radio button
options_mapping = ['Minimal WindSpeed', 'Maximum WindSpeed']
selected_ws = st.radio("***Wind Speeds***", options_mapping)
if selected_ws == "Minimal WindSpeed":
    wind_fig1 = go.Figure()

    wind_fig1.add_trace(go.Barpolar(
        r=filtered_data1['MIN_WIND_SPEED_10M_MPH'],
        name='10 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Yellow',
                    # opacity=0.8
                    ),
    ))
    wind_fig1.add_trace(go.Barpolar(
        r=filtered_data1['MIN_WIND_SPEED_80M_MPH'],
        name='80 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='red',
                    # opacity=0.5
                    ),
    ))
    wind_fig1.add_trace(go.Barpolar(
        r=filtered_data1['MIN_WIND_SPEED_100M_MPH'],
        name='100 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='blue',
                    opacity=0.5
                    ),
    ))

    wind_fig1.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    wind_fig1.update_layout(
        title='Wind Speed Distribution',
        # font_size=16,
        font=dict(family='Arial', size=14, color='orange'),
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=180,
        # width=200,
        # height=500,
        # paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        # color_discrete_sequence=px.colors.sequential.Plasma_r
        # template='plotly_dark'
    )
    st.plotly_chart(wind_fig1, use_container_width=True)
elif selected_ws == "Maximum WindSpeed":
    wind_fig2 = go.Figure()

    wind_fig2.add_trace(go.Barpolar(
        r=filtered_data1['MAX_WIND_SPEED_10M_MPH'],
        name='10 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Yellow',
                    # opacity=0.8
                    ),
    ))
    wind_fig2.add_trace(go.Barpolar(
        r=filtered_data1['MAX_WIND_SPEED_80M_MPH'],
        name='80 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='red',
                    # opacity=0.5
                    ),
    ))
    wind_fig2.add_trace(go.Barpolar(
        r=filtered_data1['MAX_WIND_SPEED_100M_MPH'],
        name='100 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='blue',
                    opacity=0.5
                    ),
    ))

    wind_fig2.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    wind_fig2.update_layout(
        title='Wind Speed Distribution',
        # font_size=16,
        font=dict(family='Arial', size=14, color='orange'),
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=180,
        # width=200,
        # height=500,
        # paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        # template='plotly_dark'
    )
    st.plotly_chart(wind_fig2, use_container_width=True)

# Bar chart for Pressure of Sea level Variance By State
st.subheader('Pressure of Sea level Variance By State')

# Create a radio button
options_mapping = ['Minimal Pressure', 'Maximum Pressure']
selected_ws = st.radio("***Pressure level***", options_mapping)

if selected_ws == 'Minimal Pressure':
    fig = px.bar(filtered_data1, x='State', y='MIN_PRESSURE_MEAN_SEA_LEVEL_MB', color="State",
                 title="Pressure Of Sea level by State",
                 hover_data=['State', 'MIN_PRESSURE_MEAN_SEA_LEVEL_MB'],
                 labels={'MIN_PRESSURE_MEAN_SEA_LEVEL_MB': 'Minimal Pressure of Sea level', 'Region': 'Region'},
                 height=600, width=1100, text='MIN_PRESSURE_MEAN_SEA_LEVEL_MB')
    st.plotly_chart(fig)

elif selected_ws == 'Maximum Pressure':
    fig = px.bar(filtered_data1, x='State', y='MAX_PRESSURE_MEAN_SEA_LEVEL_MB', color="State",
                 title="Pressure Of Sea level by State",
                 hover_data=['State', 'MAX_PRESSURE_MEAN_SEA_LEVEL_MB'],
                 labels={'MAX_PRESSURE_MEAN_SEA_LEVEL_MB': 'Maximum Pressure of Sea level', 'State': 'State'},
                 height=600, width=1100, text='MAX_PRESSURE_MEAN_SEA_LEVEL_MB')
    st.plotly_chart(fig)

# map by Precipitation
st.subheader('Localized Analysis for Precipitation, USA')

# Load the built-in GeoDataFrame of US states
us_states = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the GeoDataFrame with the DataFrame containing precipitation data
merged_data = pd.merge(us_states, filtered_data1, left_index=True, right_index=True, how='inner')

fig = px.choropleth(merged_data,
                    geojson=merged_data.geometry,
                    locations=merged_data.index,
                    color='TOT_PRECIPITATION_IN',
                    hover_data=['State', 'TOT_PRECIPITATION_IN'],
                    projection='miller',
                    title='USA State Map with Total Precipitation',
                    height=500,
                    width=1100
                   )
st.plotly_chart(fig)