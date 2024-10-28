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
gdf_areas
df_point = df_point[(df_point['project']==project)&(df_point['soortgroup']==opdracht)&(df_point['geometry_type']=="Point")]
df_point
option_1 = st.selectbox("Option 1",('zomerverblijfplaats','kraamverblijfplaats','paarverblijfplaats', 'winterverblijfplaats'))
option_1
df_point_option_1 = df_point.groupby(['gebied',option_1]).size()
df_point_option_1
