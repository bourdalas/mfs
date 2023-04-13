from dataclasses import dataclass
from random import randint, random
from typing import List, Optional

import geocoder
import geopandas as gpd
import pandas as pd
import plotly.express as px
import pycountry
import pydeck as pdk
import requests
import streamlit as st
from geopy.geocoders import Nominatim


@dataclass
class User: # type: ignore
    lon: float
    lat: float
    country: Optional[str] = None
    city: Optional[str]= None
    iso_a3: Optional[str]= None
    points: Optional[list] = None


def cities_3d(users: List[User]):


    # Load world map data
    world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # Create user dataframe
    user_df = pd.DataFrame([u.__dict__ for u in users])

    # Merge user dataframe with world map dataframe
    merged = world_map.merge(user_df, on='iso_a3')

    # Create PyDeck chart
    view_state = pdk.ViewState(latitude=user_df["lat"].mean(), longitude=user_df["lon"].mean(), zoom=5, pitch=45)
    # scatter = pdk.Layer('ScatterplotLayer',
    #                     data=user_df,
    #                     get_position='[lon, lat]',
    #                     get_color='[255, 0, 0]',
    #                     get_radius=100000,
    #                     pickable=True,
    #                     auto_highlight=True,
    #                     tooltip='country\ncity'
    #                     )
    
    
    user_markers = pdk.Layer(
    'ScatterplotLayer',
    data=user_df,
    get_position=['lon', 'lat'],
    get_fill_color=[255, 0, 0, 255], # red color    
    get_radius=8000,
    # get_elevation = "elevation",
    elevation_scale=20,
    elevation_range=[0,500],
    extruded=True,
    opacity=0.3,
    pickable=True,
    auto_highlight=True,
    coverage = 1,    
    # on_hover=["country", "city"],
        )


    polygon = pdk.Layer(
        "PolygonLayer",
        users[0].points,
        stroked=True,
        # processes the data as a flat longitude-latitude pair
        get_polygon="-",
        get_fill_color=[0, 255, 0],

    )

    r = pdk.Deck(layers=[ user_markers], initial_view_state=view_state, map_style='mapbox://styles/mapbox/dark-v10', 
                     tooltip={
        'html': '<b>{city}</b>',
        'style': {
            'color': 'white'
        }}
)

    # @st.cache(allow_output_mutation=True)
    # def display_user_details(user_idx):
    #     user = users[user_idx]
    #     st.write(f"Country: {user.country}")
    #     st.write(f"City: {user.city}")
    #     st.write(f"Latitude: {user.lat}")
    #     st.write(f"Longitude: {user.lon}")

    # Render Pydeck map in Streamlit app
    # picked = r.selected_data
    # if picked:
    #     display_user_details(picked[0]["index"])

    st.pydeck_chart(r)


def get_iso_a3(country_code):
    try:
        return pycountry.countries.lookup(country_code).alpha_3
    except LookupError:
        return None

def create_user_given_ip() -> User:
    # ip_address = requests.get('https://api.ipify.org').text
    # url = f'http://ip-api.com/json/{ip_address}'
    # data = requests.get(url).json()
    data = {"lat": 34.34, "lon": 53.21}
    lat, lon = data['lat'] * 0.2* randint(-1,2), data['lon'] * 0.1* randint(-1,1)

    # geolocator = Nominatim(user_agent='my_app')
    # location = geolocator.reverse(f'{lat}, {lon}', exactly_one=True)
    location = None
    if not location:
        return User(lon=lon, lat=lat)
    points = None
    if "boundingbox" in location.raw:
        min_lon, max_lon, min_lat, max_lat = location.raw["boundingbox"]
        points = [[min_lat, max_lon], [min_lat,min_lon], [max_lat,max_lon], [max_lat,min_lon]]
 
    
    city = location.raw['address'].get('city', None)
    country = location.raw['address'].get('country', None)
    
    iso_a3 = None
    if "country_code" in location.raw['address']: 
        country_code = location.raw['address']['country_code']
        iso_a3 = get_iso_a3(country_code)
    return User(country=country, city=city, lon=lon, lat=lat, iso_a3=iso_a3, points=points)





users = [create_user_given_ip() for _ in range(100)]

# st.write("Your location: ", location)
cities_3d(users)