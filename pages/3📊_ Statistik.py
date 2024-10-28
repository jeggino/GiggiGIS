import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import geopandas as gpd
from shapely.geometry import Polygon

import pydeck as pdk
import datetime
from datetime import datetime, timedelta, date
import random




# ---LAYOUT---
st.set_page_config(
    page_title="🦇🪶 SMPs",
    initial_sidebar_state="collapsed",
    page_icon="🦇🪶",
    layout="wide",
)


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


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

INITIAL_VIEW_STATE = pdk.ViewState(latitude=gdf_areas.dissolve().centroid.x[0], longitude=gdf_areas.dissolve().centroid.y[0], zoom=11, max_zoom=16, pitch=45, bearing=0)

geojson = pdk.Layer(
    "GeoJsonLayer",
    df_merge_option_1,
    opacity=0.8,
    stroked=False,
    filled=True,
    pickable=True,
    extruded=True,
    wireframe=True,
    get_elevation="size * 200",
    get_fill_color="[255, 255, size * 255]",
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE)

st.pydeck_chart(pydeck_obj=r,use_container_width=True, width=None, height=None, selection_mode="single-object", on_select="ignore", key=None)
