import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from deta import Deta

from credencials import *

import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="GigGIS",
    page_icon="📝",
    initial_sidebar_state="collapsed",
    layout="wide",
    
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)

reduce_header_height_style = """
<style>
    .appview-container .main .block-container {padding-top: 0em; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; margin-top: 0em; margin-bottom: 2em;}
</style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)









# --- DIMENSIONS ---
OUTPUT_height = 610
OUTPUT_width = 350
CONTAINER_height = 640
    
# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

def insert_json(key,waarnemer,datum,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"time":time,"soortgroup":soortgroup, "aantal":aantal,
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
                st.stop()

            else:

                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    drive.put(f"{key}.jpeg", data=bytes_data)            
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)
                
                else:
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)

                popover.success('Gegevens opgeslagen!', icon="✅")
                
                
                

        except:
            popover.info("Markeer een waarneming")
            st.stop()

        st.switch_page("🗺️_Home.py")

    

# --- APP ---  
popover = st.sidebar

deta = Deta(st.secrets[f"deta_key_other"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

waarnemer = popover.selectbox("Waarnemer", WAARNEMERS, key="waarnemer",index=None, label_visibility= 'collapsed', placeholder = "Wie ben je ...") 
"---"
datum = popover.date_input("Datum","today")       
nine_hours_from_now = datetime.now() + timedelta(hours=2)
time = popover.time_input("Tijd", nine_hours_from_now)
soortgroup = popover.selectbox("", GROUP)
"---"



if soortgroup == '🦇 Vleermuizen':

    sp = popover.selectbox("Soort", BAT_NAMES,key="Soort")
    gedrag = popover.selectbox("Gedrag", BAT_BEHAVIOURS) 
    functie = popover.selectbox("Functie", BAT_FUNCTIE, help=HELP_FUNCTIE ) 
    verblijf = popover.selectbox("Verblijf", BAT_VERBLIJF) 
    onbewoond = None
    aantal = popover.number_input("Aantal", min_value=1)

elif soortgroup == '🪶 Vogels':

    sp = popover.selectbox("Soort", BIRD_NAMES)
    gedrag = popover.selectbox("Gedrag", BIRD_BEHAVIOURS) 
    functie = popover.selectbox("Functie", BIRD_FUNCTIE) 
    verblijf = popover.selectbox("Verblijf", BIRD_VERBLIJF) 
    onbewoond = None
    aantal = popover.number_input("Aantal", min_value=1)

elif soortgroup == '🏠 Vleermuiskast':
    onbewoond = popover.selectbox("Bewoond", VLEERMUISKAST_OPTIONS)
    BAT_NAMES = ["onbekend"] + BAT_NAMES
    sp = popover.selectbox("Soort", BAT_NAMES) 
    gedrag = None
    functie = None
    verblijf = None
    aantal = popover.number_input("Aantal", min_value=1)

elif soortgroup == '📷 Camera':
    functie = popover.selectbox("Camera", CAMERA_OPTIONS)
    BAT_NAMES = None
    sp = None 
    gedrag = None
    onbewoond = None
    verblijf = None
    aantal = None

elif soortgroup == '🐀 Rat val':
    functie = popover.selectbox("Rat val", RAT_VAL_OPTIONS)
    BAT_NAMES = None
    sp = None 
    gedrag = None
    onbewoond = None
    verblijf = None
    aantal = None

opmerking = popover.text_input("", placeholder="Vul hier een opmerking in ...")

with popover.expander("Upload een foto"):
    uploaded_file = st.camera_input("")

    
input_data()

