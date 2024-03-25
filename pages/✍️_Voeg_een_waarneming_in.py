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
OUTPUT_height = 610
OUTPUT_width = 350
CONTAINER_height = 640
    
# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

def insert_json(key,waarnemer,datum,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"onbewoond":onbewoond,"coordinates":coordinates})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False,}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    
    return  output


def input_data():

    with st.container(height=CONTAINER_height, border=True):
        
        output = map()
    
        
    submitted = popover.button("Gegevens opslaan")
    
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
                popover.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                popover.stop()

            else:

                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    drive.put(f"{key}.jpeg", data=bytes_data)            
                    insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)
                
                else:
                    insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)

                popover.success('Gegevens opgeslagen!', icon="✅")
                
                
                

        except:
            popover.info("Markeer een waarneming")
            st.stop()

        st.switch_page("🗺️_Home.py")

    

# --- APP ---    
popover = st.popover("🗒️")

popover.page_link("🗺️_Home.py", label="Annuleren", icon="❌")
soortgroup = popover.selectbox("", GROUP)
datum = popover.date_input("Datum")        

if soortgroup == '🦇 Vleermuizen':

    sp = popover.selectbox("Soort", BAT_NAMES)
    gedrag = popover.selectbox("Gedrag", BAT_BEHAVIOURS) 
    functie = popover.selectbox("Functie", BAT_FUNCTIE) 
    verblijf = popover.selectbox("Verblijf", BAT_VERBLIJF) 
    onbewoond = None

elif soortgroup == '🪶 Vogels':

    sp = popover.selectbox("Soort", BIRD_NAMES)
    gedrag = popover.selectbox("Gedrag", BIRD_BEHAVIOURS) 
    functie = popover.selectbox("Functie", BIRD_FUNCTIE) 
    verblijf = popover.selectbox("Verblijf", BIRD_VERBLIJF) 
    onbewoond = None

elif soortgroup == '🏠 Vleermuiskast':
    onbewoond = popover.selectbox("Bewoond", ["Ja","Nee"])
    BAT_NAMES = ["onbekend"] + BAT_NAMES
    sp = popover.selectbox("Soort", BAT_NAMES) 
    gedrag = None
    functie = None
    verblijf = None
    

aantal = popover.number_input("Aantal", min_value=0)
opmerking = popover.text_input("", placeholder="Vul hier een opmerking in ...")

with popover.expander("Upload een foto"):
    uploaded_file = st.camera_input("")

input_data()

