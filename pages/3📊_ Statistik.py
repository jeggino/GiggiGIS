import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import geopandas as gpd
from shapely.geometry import Polygon

import pydeck as pdk
import datetime
from datetime import datetime, timedelta, date
import random


#---DATASET---
ttl = 0
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="df_observations")

# --- APP ---
project = st.session_state["project"]['project_name']
opdracht = st.session_state["project"]['opdracht']
gdf_areas = gpd.read_file(f"geometries/{project}.geojson")
gdf_areas.geometry = gdf_areas.geometry.apply(lambda x: Polygon(x.coords)) 
df_point = df_point[(df_point['project']==project)&(df_point['soortgroup']==opdracht)&(df_point['geometry_type']=="Point")].reset_index(drop=True)
option_1 = st.selectbox("Option 1",('zomerverblijfplaats','kraamverblijfplaats','paarverblijfplaats', 'winterverblijfplaats'))
df_point_option_1 = df_point[df_point['functie']==option_1]
df_point_option_1 = df_point_option_1.groupby(['gebied'],as_index=False).size()
df_merge_option_1 = gdf_areas.rename(columns={'Wijk':'gebied'}).merge(df_point_option_1, on='gebied',how='left').fillna(0)
INITIAL_VIEW_STATE = pdk.ViewState(latitude=49.254, longitude=-123.13, zoom=11, max_zoom=16, pitch=45, bearing=0)

geojson = pdk.Layer(
    "GeoJsonLayer",
    df_merge_option_1,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="size / 20",
    get_fill_color="[255, 255, size * 255]",
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[polygon, geojson], initial_view_state=INITIAL_VIEW_STATE)
