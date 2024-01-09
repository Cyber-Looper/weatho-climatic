import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# Title
st.set_page_config(page_title="Weatho-Climatic Analytics", page_icon=":bar_chart:", layout="wide")

with open('/mount/src/weatho-climatic/WeatherClimateAnalytics/src/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Heading
st.title(":sun_behind_rain_cloud: Weather and Climate Forecasting, USA.")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Introduction
st.write(':snowflake: **Weather** and **Climate** play a pivotal role in shaping the daily lives of people across '
         'the United States. The'
         'period from 2021 to 2022 witnessed significant climatic events, impacting various regions, states, '
         'and cities. This dashboard provides a overview of key weather parameters, including ***air temperature, '
         'wind speed, sea-level pressure, solar radiation, precipitation, and snowfall***.')

# Dataset
# data = pd.read_csv('../dataset/upd_forecast_data.csv')
data = pd.read_csv('/mount/src/weatho-climatic/WeatherClimateAnalytics/dataset/upd_forecast_data.csv')
# st.dataframe(data)

# SideBar
st.sidebar.subheader('Apply Filters:')

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

# Map chart for Localized Analysis for Precipitation, USA
st.subheader(':thunder_cloud_and_rain: Localized Analysis for Precipitation, USA')
st.write(':pushpin: The USA witnessed diverse precipitation patterns across its states from 2021 to 2022. Some '
         'regions faced'
         'prolonged droughts, impacting water resources and agriculture, while others grappled with heavy rainfall '
         'and storms, leading to flooding and infrastructure challenges. Precise state-specific precipitation '
         'forecasting proved vital for managing water resources, mitigating the impact of extreme weather events, '
         'and supporting informed decision-making in various sectors.')

# Round the column values to 6 decimal places
filtered_data1['Longitude'] = filtered_data1['Longitude'].astype(float).round(6)
filtered_data1['Latitude'] = filtered_data1['Latitude'].astype(float).round(6)

custom_scale = ["#FF6A3D", "#A288A6", "#1A2238"]
fig = px.scatter_mapbox(filtered_data1, lat="Latitude", lon="Longitude", hover_name="State",
                        hover_data=["State", "TOT_PRECIPITATION_IN", "DATE_VALID_STD"],
                        color_discrete_sequence=custom_scale, zoom=3, height=300,
                        title="USA State Map with Total Precipitation",
                        labels={"State": "State", "TOT_PRECIPITATION_IN": "Total precipitations"})
fig.update_layout(

    mapbox_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)
st.plotly_chart(fig)

# Line chart for Avg Temp. per Day

# Convert 'DATE_VALID_STD' column to datetime
filtered_data1['DATE_VALID_STD'] = pd.to_datetime(filtered_data1['DATE_VALID_STD'], format='%d-%m-%Y')
st.subheader(':fog: Air Temperature on a Daily Basis')
st.write(':pushpin: Throughout 2021-2022, the USA experienced dynamic fluctuations in Monthly air temperatures. '
         'Record-breaking heatwaves and unseasonable cold spells marked the extremes, with minimum temperatures '
         'plunging and maximum'
         'temperatures soaring. Climatologists closely monitored these shifts, providing valuable insights into the '
         'average monthly temperature trends across regions, states, and cities.')
# Create a radio button
Options = ["AVG_TEMPERATURE_AIR_2M_F", "MIN_TEMPERATURE_AIR_2M_F", "MAX_TEMPERATURE_AIR_2M_F"]
selected_option = st.radio("***Temperatures***", Options)

# Choose
# Sort Date value as ascending order
filtered_data['DATE_VALID_STD'] = pd.to_datetime(filtered_data['DATE_VALID_STD'], format='%d-%m-%Y')
filtered_data = filtered_data.sort_values(by='DATE_VALID_STD', ascending=True)

# Page layouts for minimum and maximum dates
filtered_data_date = filtered_data.copy()

# Timeline to filter Air Temperature
st.subheader('Apply Timeline')
col1, col2 = st.columns(2)
filtered_data_date["DATE_VALID_STD"] = pd.to_datetime(filtered_data_date["DATE_VALID_STD"])

# customize date_input field
st.markdown(
    """
    <style>
        div[data-baseweb="input"] {
            width: 300px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Getting the min and max date
startDate = pd.to_datetime('2021-12-29')
# startDate = pd.to_datetime(filtered_data_date["DATE_VALID_STD"]).min()
endDate = pd.to_datetime(filtered_data_date["DATE_VALID_STD"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("***Start Date***", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("***End Date***", endDate))

filtered_date = filtered_data_date[
    (filtered_data_date["DATE_VALID_STD"] >= date1) & (filtered_data_date["DATE_VALID_STD"] <= date2)].copy()
# st.write(filtered_date)

if selected_option == "AVG_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_date.groupby(filtered_date["DATE_VALID_STD"].dt.strftime("%Y %b"))[
                                 "AVG_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Average Temperature for Air", "DATE_VALID_STD": "Month of Year"},
                  height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "MAX_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_date.groupby(filtered_date["DATE_VALID_STD"].dt.strftime("%Y %b"))[
                                 "MAX_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Maximum Temperature for Air", "DATE_VALID_STD": "Month of Year"},
                  height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "MIN_TEMPERATURE_AIR_2M_F":
    linechart = pd.DataFrame(filtered_date.groupby(filtered_date["DATE_VALID_STD"].dt.strftime("%Y %b"))[
                                 "MIN_TEMPERATURE_AIR_2M_F"].sum()).reset_index()
    fig = px.line(linechart, x="DATE_VALID_STD", y=selected_option,
                  labels={selected_option: "Minimum Temperature for Air", "DATE_VALID_STD": "Month of Year"},
                  height=500,
                  width=1000, template="gridon")
    st.plotly_chart(fig, use_container_width=True)

# WindRose chart for Minimal and Maximum WindSpeed Variance By Region
st.subheader(':tornado_cloud: WindSpeed Variance By Region')
st.write(':pushpin: The USA experienced notable wind speed variances across different regions from 2021 to 2022. '
         'Coastal areas,'
         'particularly in the East and West, encountered significant wind events influencing maritime activities and '
         'local climates. Varied wind patterns in the South and Central regions had implications for industries such '
         'as agriculture, transportation, and renewable energy. Precise regional wind speed forecasting played a '
         'crucial role in preparing for and adapting to changing atmospheric conditions.')
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
        marker=dict(color='Purple',
                    # opacity=0.8
                    ),
    ))
    wind_fig1.add_trace(go.Barpolar(
        r=filtered_data1['MIN_WIND_SPEED_80M_MPH'],
        name='80 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Blue',
                    # opacity=0.5
                    ),
    ))
    wind_fig1.add_trace(go.Barpolar(
        r=filtered_data1['MIN_WIND_SPEED_100M_MPH'],
        name='100 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Green',
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
        marker=dict(color='Purple',
                    # opacity=0.8
                    ),
    ))
    wind_fig2.add_trace(go.Barpolar(
        r=filtered_data1['MAX_WIND_SPEED_80M_MPH'],
        name='80 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Blue',
                    # opacity=0.5
                    ),
    ))
    wind_fig2.add_trace(go.Barpolar(
        r=filtered_data1['MAX_WIND_SPEED_100M_MPH'],
        name='100 m/h',
        theta=filtered_data1['Region'],
        hoverinfo='r+theta+name',
        marker=dict(color='Green',
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
st.subheader(':ocean: Pressure of Sea level Variance By State')
st.write(':pushpin: The sea-level pressure dynamics exhibited regional variations across USA states from 2021 to '
         '2022. Changes in sea-level pressure played a crucial role in influencing weather patterns, '
         'storm developments, and oceanic currents. Monitoring state-specific sea-level pressure variations was '
         'essential for accurate weather forecasting, aiding in the anticipation and preparation for extreme weather '
         'events in different coastal areas.')
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


# Footer content
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(
        """
        <div class="cust_footer">
            <p>logo</p>
            <p>Weather and Climate Forecasting for USA</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with foot2:
    st.markdown(
        """
        <div class="cust_footer">
            <p>Resources</p>
            <p>Data Source: [Your Data Source]</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with foot2:
    st.markdown(
        """
        <div class="cust_footer">
            <p>Contact Us</p>
            <p>Email</p>
            <p>Phone</p>
            <br><br><br>
            <p>Powered by: Climato-Weather</p>
        </div>
        """,
        unsafe_allow_html=True
    )