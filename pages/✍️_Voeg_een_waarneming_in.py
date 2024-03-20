import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import date
import random

from deta import Deta

from credencials import *

import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="GigGIS",
    page_icon="📝",
    layout="wide",
    
)


reduce_header_height_style = """
<style>
    div.block-container {padding-top:0rem; padding-bottom: 0em; padding-left: 0rem; padding-right: 0rem; margin-top: 1em; margin-bottom: 2em;}
</style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.markdown("""
<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
""",
unsafe_allow_html=True)


# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

try:
    waarnemer = st.session_state["name"]
    
except:
    st.switch_page("🗺️_Home.py")

# --- DIMENSIONS ---
OUTPUT_height = 630
OUTPUT_width = 350
CONTAINER_height = 660
# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

def insert_json(key,waarnemer,datum,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"onbewoond":onbewoond,"coordinates":coordinates})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    
    return  output


def input_data():

    with st.container(height=CONTAINER_height, border=True):
        
        output = map()
    
    with st.sidebar:
        
        submitted = st.button("Gegevens opslaan")
        
        if submitted:           

            try:

                output["features"] = output.pop("all_drawings")
                geometry_type = output["features"][0]["geometry"]["type"]
                coordinates = output["features"][0]["geometry"]["coordinates"] 
                
                if geometry_type == "LineString":
                    
                    lng = None
                    lat = None
                    key = None
                
                else: 
                    
                    lng = coordinates[0]
                    lat = coordinates[1]
                    coordinates = None
                    
                    key = str(lng)+str(lat)

                if len(output["features"]) > 1:
                    st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                    st.stop()

                else:

                    if uploaded_file is not None:
                        bytes_data = uploaded_file.getvalue()
                        drive.put(f"{key}.jpeg", data=bytes_data)            
                        with st.spinner('Wait for it...'):
                            insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)
                    
                    else:
                        with st.spinner('Wait for it...'):
                            insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)

                    st.success('Gegevens opgeslagen!', icon="✅")
                    
                    
                    

            except:
                st.info("Markeer een waarneming")

            st.switch_page("🗺️_Home.py")

    

# --- APP ---    
with st.sidebar:

    soortgroup = st.selectbox("", GROUP)
    datum = st.date_input("Datum")        

    if soortgroup == '🦇 Vleermuizen':
    
        sp = st.selectbox("Soort", BAT_NAMES)
        gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
        functie = st.selectbox("Functie", BAT_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
        onbewoond = None
    
    elif soortgroup == '🪶 Vogels':
    
        sp = st.selectbox("Soort", BIRD_NAMES)
        gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
        functie = st.selectbox("Functie", BIRD_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
        onbewoond = None
    
    elif soortgroup == '🏠 Vleermuiskast':
        onbewoond = st.selectbox("Bewoond", ["Ja","Nee"])
        BAT_NAMES = ["onbekend"] + BAT_NAMES
        sp = st.selectbox("Soort", BAT_NAMES) 
        gedrag = None
        functie = None
        verblijf = None
        
    
    aantal = st.number_input("Aantal", min_value=0)
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    with st.expander("Upload een foto"):
        uploaded_file = st.camera_input("")

input_data()
