import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import requests
import json
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# CARICAMENTO DATI E PREPROCESSING
DATA_URL = (
    r"C:\Users\kevin\Desktop\Università\DataScience\2 year\Lab on Smart Cities\Data\full_data\drive-download-20230504T163914Z-002\Motor_Vehicle_Collisions_-_Crashes.csv"
)
speeds_url = 'https://data.cityofnewyork.us/resource/i4gi-tjb9.json?$limit=3000'   # 3000 numero di righe 
crashes_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=100000'

    # read data using usecols
data = pd.read_csv(DATA_URL, usecols = ['LATITUDE', 'LONGITUDE', 'CRASH DATE', 'CRASH TIME', 'ON STREET NAME',  'NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED', 'CONTRIBUTING FACTOR VEHICLE 1'])
        #r = requests.get(crashes_url)
        #data = r.json()
        # create a dataframe with the data
        #data = pd.DataFrame(data)
lowerCase = lambda x: str(x).replace(' ', '_').lower()
data.rename(lowerCase, axis='columns', inplace=True)
  # change dtypes
data['latitude'] = data['latitude'].astype('float64')
data['longitude'] = data['longitude'].astype('float64')
        # dropna for number_of_persons_injured
data = data.dropna(axis = 0, subset=['latitude', 'longitude', 'number_of_persons_injured', 'number_of_persons_killed', 'number_of_pedestrians_injured', 'number_of_pedestrians_killed', 'number_of_cyclist_injured', 'number_of_cyclist_killed', 'number_of_motorist_injured', 'number_of_motorist_killed', 'contributing_factor_vehicle_1'])
data['number_of_persons_injured'] = data['number_of_persons_injured'].astype('int64')
data['number_of_persons_killed'] = data['number_of_persons_killed'].astype('int64')
data['number_of_pedestrians_injured'] = data['number_of_pedestrians_injured'].astype('int64')
data['number_of_pedestrians_killed'] = data['number_of_pedestrians_killed'].astype('int64')
data['number_of_cyclist_injured'] = data['number_of_cyclist_injured'].astype('int64')
data['number_of_cyclist_killed'] = data['number_of_cyclist_killed'].astype('int64')
data['number_of_motorist_injured'] = data['number_of_motorist_injured'].astype('int64')

data['number_of_motorist_killed'] = data['number_of_motorist_killed'].astype('int64')
data['crash_date_crash_time'] = pd.to_datetime(data['crash_date'] + ' ' + data['crash_time'])
data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
data['contributing_factor_vehicle_1'] = data['contributing_factor_vehicle_1'].astype('category')


# filer out some data with wrong coordinates
data = data[data['latitude'] > 40]
data = data[data['longitude'] < -70]
data = data[data['latitude'] < 42]
data = data[data['longitude'] > -75]



if __name__ == '__main__':    
    # set page width
    st.set_page_config(layout="wide")
    st.title("       Near Real-Time Analysis of Motor Vehicle Collisions in NYC ")
    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")

    


    # CHECKBOX PER VISUALIZZARE TUTTI DATI RAW
    st.subheader("Click the checkbox to see the raw data loaded from the NYC Open Data API")
    if st.button("Show raw data", False):
        st.write(data.head(8))

    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")

    


# GRAFICO 3D SUL NUMERO DI COLLISIONI IN BASE ALL'ORA
    st.header("How many accidents occur during the day and which subjects are involved?")
    # multiple select
    multi = st.selectbox('Select the type of collisions you are interested in', ['All', 'Pedestrians', 'Cyclists', 'Motorists'])

    # select the time period- last week , last month, overall
    time_period = st.selectbox('Select the time period you are interested in', ['Last week', 'Last month', 'Overall'])
    if multi == 'All':
        data2 = data
    elif multi == 'Pedestrians':
        data2 = data[data['number_of_pedestrians_injured'] + data['number_of_pedestrians_killed'] > 0]
    elif multi == 'Cyclists':
        data2 = data[data['number_of_cyclist_injured'] + data['number_of_cyclist_killed'] > 0]
    elif multi == 'Motorists':
        data2 = data[data['number_of_motorist_injured'] + data['number_of_motorist_killed'] > 0]


    if time_period == 'Overall':
        data2 = data2
    elif time_period == 'Last week':
        data2 = data2[data2['date/time'] >= pd.to_datetime(datetime.datetime.now() - datetime.timedelta(days=100))]
    elif time_period == 'Last month':
        data2 = data2[data2['date/time'] >= pd.to_datetime(datetime.datetime.now() - datetime.timedelta(days=120))]

    hour = st.slider("Hour to look at", 0, 23)
    data2 = data2[data2['date/time'].dt.hour == hour]

    st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    midpoint = (np.average(data2['latitude']), np.average(data2['longitude']))
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state = {
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50
        },
        layers = [
            pdk.Layer(
                "HexagonLayer",
                data = data2[['date/time', 'latitude', 'longitude']],
                get_position=['longitude', 'latitude'],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    ))

    st.markdown("   ")
    st.markdown("   ")




# GRAFICO A BARRE SUL NUMERO DI COLLISIONI IN BASE AL MINUTO
    st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    filtered = data[
        (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
    ]
    hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
    fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
    st.write(fig)

    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")





# GRAFICO A DISPERSIONE SUL NUMERO DI PERSONE INFORTUNATE
    st.header("Where are the most people injured/killed in accidents in New York City?")
    multi = st.selectbox("Select the type of people's involvement in the accident", ['Injured', 'Killed'])
    # select the time period- last week , last month, overall
    time_period2 = st.selectbox('Select the time period you are interested in ', ['Last week', 'Last month', 'Overall'])
    injured_people = st.slider("Number of people involved in vehicle collisions", 0, 19)

    if multi == 'Injured':
        query = "number_of_persons_injured >= @injured_people"
    elif multi == 'Killed':
        query = "number_of_persons_killed >= @injured_people"

    if time_period == 'Overall':
        data2 = data
    elif time_period == 'Last week':
        data2 = data[data['date/time'] >= pd.to_datetime(datetime.datetime.now() - datetime.timedelta(days=70))]
    elif time_period == 'Last month':
        data2 = data[data['date/time'] >= pd.to_datetime(datetime.datetime.now() - datetime.timedelta(days=85))]

    st.map(data2.query(query)[["latitude", "longitude"]].dropna(how="any"))
    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")

   

    


# LISTA DELLE STRADE PIU' PERICOLOSE IN BASE AL TIPO DI PERSONA INFORTUNATA (PEDESTRIAN, CYCLIST, MOTORIST)
    st.header("Top 5 dangerous streets by types of affected people")
    select = st.selectbox('Affected categories', ['Pedestrians', 'Cyclists', 'Motorists'])

    if select == 'Pedestrians':
        st.write(data.query("number_of_pedestrians_injured >= 1")[["on_street_name", "number_of_pedestrians_injured",  "number_of_pedestrians_killed"   ]].sort_values(by=['number_of_pedestrians_injured'], ascending=False).dropna(how='any')[:5])

    elif select == 'Cyclists':
        st.write(data.query("number_of_cyclist_injured >= 1")[["on_street_name", "number_of_cyclist_injured", "number_of_cyclist_killed"]].sort_values(by=['number_of_cyclist_injured'], ascending=False).dropna(how='any')[:5])

    else:
        st.write(data.query("number_of_motorist_injured >= 1")[["on_street_name", "number_of_motorist_injured", "number_of_motorist_killed"]].sort_values(by=['number_of_motorist_injured'], ascending=False).dropna(how='any')[:5])




