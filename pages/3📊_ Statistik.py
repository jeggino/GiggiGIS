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
df_point[(df_point['project']==project)&(df_point['soortgroup']==opdracht)&(df_point['geometry_type']=="Point")]

import streamlit as st

tab1 = st.tabs(["Cat"])
tab2 = st.tabs(["Dog"]) 
tab3 = st.tabs(["Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
