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
gdf_areas = gpd.read_file(geometry_file)
gdf_areas.geometry = gdf_areas.geometry.apply(lambda x: Polygon(x.coords)) 
gdf_areas
df_point[df_point['project']==st.session_state["project"]['project_name']]
