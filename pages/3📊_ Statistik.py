import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import geopandas as gpd
from shapely.geometry import Polygon

import pydeck as pdk
import altair as alt

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
df_dagverslag = conn.read(ttl=ttl,worksheet="df_ekomaps_dagverslagen")


# --- APP ---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE,  link=None, icon_image=IMAGE_2)

project = st.session_state["project"]['project_name']
opdracht = st.session_state["project"]['opdracht']
gdf_areas = gpd.read_file(f"geometries/{project}.geojson")
gdf_areas.geometry = gdf_areas.geometry.apply(lambda x: Polygon(x.coords)) 
df_point = df_point[(df_point['project']==project)&(df_point['soortgroup']==opdracht)&(df_point['geometry_type']=="Point")].reset_index(drop=True)

col_1,col_2 = st.columns([1,2])
option_1 = col_1.selectbox("Option 1",('zomerverblijfplaats','kraamverblijfplaats','paarverblijfplaats', 'winterverblijfplaats'))
df_point_option_1 = df_point[df_point['functie']==option_1]
df_point_option_1 = df_point_option_1.groupby(['gebied'],as_index=False).size()
df_merge_option_1 = gdf_areas.rename(columns={'Wijk':'gebied'}).merge(df_point_option_1, on='gebied',how='left').fillna(0)

# st.bar_chart(df_merge_option_1, x="size", y="gebied", horizontal=False)
col_1.bar_chart(data=df_merge_option_1, x="size", y="gebied", x_label='aantal', y_label='Gebied', color=None, 
horizontal=False, stack=False, width=None, height=400, use_container_width=True)

INITIAL_VIEW_STATE = pdk.ViewState(latitude=gdf_areas.dissolve().centroid.y[0], longitude=gdf_areas.dissolve().centroid.x[0], zoom=11, max_zoom=16, pitch=45, bearing=0)

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

tooltip = {
    "html": "<b>{gebied}</b> <br /><b>Aantal: {size}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE,tooltip=tooltip)

col_2.pydeck_chart(pydeck_obj=r,use_container_width=True, width=None, height=400, selection_mode="single-object", on_select="ignore", key=None)

"---"
option_2 = st.selectbox("Option 2",gdf_areas['Wijk'].unique())
df_dagverslag_option_2 = df_dagverslag[df_dagverslag['gebied_id']==option_2]
df_dagverslag_option_2['datum'] = pd.to_datetime(df_dagverslag_option_2['datum'])
df_dagverslag_option_2['year'] = df_dagverslag_option_2['datum'].dt.year

year_min = df_dagverslag_option_2['year'].min()
year_max = df_dagverslag_option_2['year'].max() + 1

chart = alt.Chart(df_dagverslag_option_2).mark_point(size=60).encode(
    alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
          scale=alt.Scale(domain=[str(year_min),str(year_max)])),
    alt.Y('gebied_id:N',
          axis=alt.Axis(grid=False,domain=False,ticks=True,),
          sort=alt.EncodingSortField(field="gebied",  order='ascending'),
          title=""),
    stroke=alt.Color('doel'),
    fill=alt.Color('doel',legend=alt.Legend(orient="bottom",direction='vertical',titleAnchor='middle')).title("Doel"),
    tooltip=[alt.Tooltip("waarnemer:N",title = "Waarnemer"),
             alt.Tooltip("extra_velfwerker:N",title ="Extra veldwerkers"),
             alt.Tooltip("doel:N",title ="Doel"),
             alt.Tooltip("datum:T",title ="Datum"),
             alt.Tooltip("start_time:N",title ="Begin tijd"),
             alt.Tooltip("eind_time:N",title ="Eind tijd"),
             alt.Tooltip("temperatuur:N",title ="Temperatuur"),
             alt.Tooltip("bewolking:N",title ="Bewolking"),
             alt.Tooltip("neerslag:N",title ="Neerslag"),
             alt.Tooltip("windkrcht:N",title ="Windkrcht"),
             alt.Tooltip("windrichting:N",title ="Windrichting"),
             alt.Tooltip("opmerking:N",title ="Opmerking"),
            ],
).properties(
    height=230,
    title=alt.Title(
        text="",
        subtitle="",
        anchor='start'
    )
).configure_view(stroke=None)

st.altair_chart(chart, theme=None, use_container_width=True)
