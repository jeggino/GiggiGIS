import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd

import pydeck as pdk
import datetime
from datetime import datetime, timedelta, date
import random


st.session_state["project"]['gdf']
geometry_file = f"geometries/{st.session_state["project"]['project_name']}.geojson" 
gdf_areas = gpd.read_file(geometry_file)
gdf_areas.geometry = gdf_areas.geometry.apply(lambda x: Polygon(x.coords)) 
gdf_areas
