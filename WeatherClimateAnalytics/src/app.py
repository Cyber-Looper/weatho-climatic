import pandas as pd
import requests
from io import StringIO
import streamlit as st
import snowflake.connector as sf
import plotly.express as px
import plotly.graph_objects as go
import numpy

# Authentication with Snowflake credentials
conn = sf.connect(user='sudharchanan', password='Sudharcha$434', role='ACCOUNTADMIN',
                  account='rw21158.central-india.azure',
                  warehouse='COMPUTE_WH', database='global_weather__climate_data_for_bi')
# Create a cursor object
cur = conn.cursor()
st.session_state['snow_conn'] = cur


# # Store the session returned data
@st.cache_data
def get_weather():
    fore_data = pd.read_csv('forecast_data.csv')
    src_data = pd.DataFrame(fore_data)
    return src_data


tle = 'Global Weather Analytics'
st.markdown(f'<h2 style="text-align:center;background-color:#ffffff;color:green;">{tle}</h2>',
            unsafe_allow_html=True)

wc_data = get_weather()

st.write(wc_data)


# Replace meaningful country name instead code
def cntry_code_to_name(code):
    if code == 'US':
        return 'US of America'
    elif code == 'AU':
        return 'Australia'
    elif code == 'BR':
        return 'Brazil'
    elif code == 'GB':
        return 'United Kingdom'
    elif code == 'DE':
        return 'Germany'
    else:
        return code


# Apply the function to the specified column
wc_data['COUNTRY'] = wc_data['COUNTRY'].apply(cntry_code_to_name)

# Convert the 'wc_date' DATE_VALID_STD column to datetime format
wc_data['DATE_VALID_STD'] = pd.to_datetime(wc_data['DATE_VALID_STD'], format="%d-%m-%Y")

# Extracting year, month, and day from the datetime column
wc_data['year'] = wc_data['DATE_VALID_STD'].dt.year
wc_data['month'] = wc_data['DATE_VALID_STD'].dt.month
wc_data['day'] = wc_data['DATE_VALID_STD'].dt.day

wc_data['TOT_PRECIPITATION_IN'] = wc_data['TOT_PRECIPITATION_IN'].sum()
wc_data['TOT_PRECIPITATION_IN'] = wc_data['TOT_PRECIPITATION_IN'].round(2)
report_tle = 'Weather Report'
st.markdown(f'<h4 style="color:cyan;">{report_tle}</h4>', unsafe_allow_html=True)
# st.write(wc_data['year'], wc_data['month'], wc_data['day'])

# Bar chart to know total precipitation regarding snow/rain
fig = px.bar(wc_data, x='COUNTRY', y='TOT_PRECIPITATION_IN', color="COUNTRY", title="Precipitations based on Country",
             hover_data=['COUNTRY', 'TOT_PRECIPITATION_IN'], labels={'TOT_PRECIPITATION_IN': 'Total Precipitations',
                                                                     'COUNTRY': 'Country'}, height=500,
             text='TOT_PRECIPITATION_IN')
st.plotly_chart(fig)

# Wind speed based on direction
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=wc_data['MAX_WIND_SPEED_10M_MPH'],
    name='10 m/h',
    # text=wc_data['COUNTRY'],
    theta=wc_data['COUNTRY'],
    hoverinfo='r+theta+name',
    marker=dict(color='Yellow',
                # opacity=0.8
                ),
))
fig.add_trace(go.Barpolar(
    r=wc_data['MAX_WIND_SPEED_80M_MPH'],
    name='80 m/h',
    # text=wc_data['COUNTRY'],
    theta=wc_data['COUNTRY'],
    hoverinfo='r+theta+name',
    marker=dict(color='red',
                # opacity=0.5
                ),
))
fig.add_trace(go.Barpolar(
    r=wc_data['MAX_WIND_SPEED_100M_MPH'],
    name='100 m/h',
    # text=wc_data['COUNTRY'],
    theta=wc_data['COUNTRY'],
    hoverinfo='r+theta+name',
    marker=dict(color='blue',
                opacity=0.5
                ),
))

fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
fig.update_layout(
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
st.plotly_chart(fig)

# Daily solar radiation levels across different geographical regions.
# wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'] = wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'].sum()
# wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'] = wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'].round(2)

# fig, ax = plt.subplots()
# im = ax.imshow(wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'])
#
# # Show all ticks and label them with the respective list entries
# ax.set_xticks((wc_data['COUNTRY']), labels='COUNTRY')
# ax.set_yticks((wc_data['month']), labels='Solar Radiation by Month')
st.write(wc_data.shape)
# fig = px.imshow(wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'],
#                 x=wc_data['COUNTRY'],
#                 y=wc_data['month'],
#                 labels=dict(x='Country', y='Solar Radiation by Month'),
#                 title='Daily solar radiation levels across different geographical regions',
#                 color_continuous_scale='viridis',
#                 width=600,
#                 height=400,
#                 facet_col=3
#                 )
# # Customizing layout properties
# fig.update_layout(
#     xaxis=dict(title='Category Axis'),
#     yaxis=dict(title='Values Axis'),
#     margin=dict(l=50, r=50, b=50, t=50),
#     font=dict(family='Arial', size=12, color='black'),
#     title_font=dict(size=16, family='Arial'),
#     # coloraxis_colorbar=dict(title='Colorbar Title'),
#     plot_bgcolor='white',
#     paper_bgcolor='lightgray',
# )

# st.write(wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'].sum())
# wc_data['year'] = wc_data['year'].unique()
# wc_data['COUNTRY'] = wc_data.drop_duplicates(subset="COUNTRY")
# uniqueValues = (wc_data['year'].append(wc_data['year'])).unique()
# st.write(uniqueValues)
# st.write(wc_data['COUNTRY'])
# agg_weather_data = wc_data.groupby(['COUNTRY', 'month'])
# wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'] = wc_data['TOT_RADIATION_SOLAR_TOTAL_WPM2'].sum()
# fig = px.imshow(wc_data, x='COUNTRY', y='year', color_continuous_scale='viridis')

# st.plotly_chart(fig)

# # Create a horizontal line chart using Plotly
# fig = go.Figure(data=[
#     go.Scatter(x=wc_data['year'], y=wc_data["AVG_TEMPERATURE_AIR_2M_F"], mode='lines', orientation='h',
#                fillcolor='blue')])
# #
# # # Set chart layout
# fig.update_layout(title='Average Temparature for Past Years', xaxis_title='Years', yaxis_title=' Avg.Temperature')
#
# # # Display the Plotly chart in the Streamlit app
# st.plotly_chart(fig)
#
# # Altair Line Charts
#
# alt.Chart(wc_data).mark_line().encode(
#     x=wc_data['year'],
#     y=wc_data["AVG_TEMPERATURE_AIR_2M_F"]
# )
