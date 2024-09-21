import streamlit as st
from streamlit_js_eval import streamlit_js_eval

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from deta import Deta

from credencials import *



# ---LAYOUT---
st.set_page_config(
    page_title="GigGIS",
    initial_sidebar_state="collapsed",
    page_icon="📝",
    layout="wide",
    
)

# .viewerBadge_text__1JaDK{ display: none; }

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,  footer { visibility: hidden; } 
    </style>
    """,
    unsafe_allow_html=True)

reduce_header_height_style = """
<style>
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem;}  header { visibility: hidden; padding-bottom: 1rem; }
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)



# --- COSTANTS ---
IMAGE = "image/logo.png"
WIDTH_SCREEN = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
HEIGHT_SCREEN = streamlit_js_eval(js_expressions='screen.height', key = 'SCR1')
OUTPUT_height = int(HEIGHT_SCREEN) * 0.75
OUTPUT_width = WIDTH_SCREEN 

# --- DATASET ---
deta = Deta(st.secrets[f"deta_key_other"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures") 
    
# --- FUNCTIONS ---
def insert_json(key,waarnemer,datum,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates,"project":project})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False,}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    

    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    output["features"] = output.pop("all_drawings")
    
    return  output

        
@st.dialog(" ")
def input_data(output):

    waarnemer = st.session_state.login['name']
    project = st.session_state.project['project_name']
    soortgroup = st.session_state.project['opdracht']
    
    
    datum = st.date_input("Datum","today")       
    nine_hours_from_now = datetime.now() + timedelta(hours=2)
    time = st.time_input("Tijd", nine_hours_from_now)
    
    st.divider()
    
    if soortgroup == 'Vleermuizen':
    
        sp = st.selectbox("Soort", BIRD_NAMES)
        sp = st.selectbox("Soort", BAT_NAMES)
        gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
        functie = st.selectbox("Functie", BAT_FUNCTIE, help=HELP_FUNCTIE ) 
        verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
        aantal = st.number_input("Aantal", min_value=1)
    
    elif soortgroup == 'Vogels':
    
        sp = st.selectbox("Soort", BIRD_NAMES)
        gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
        functie = st.selectbox("Functie", BIRD_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
        aantal = st.number_input("Aantal", min_value=1)
    
    elif soortgroup == 'Vleermuiskast':
        functie = st.selectbox("Voorwaarde", VLEERMUISKAST_OPTIONS)
        bat_name = ["onbekend"] + BAT_NAMES
        sp = st.selectbox("Soort", bat_name) 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
    
    elif soortgroup == 'Camera':
        functie = st.selectbox("Camera", CAMERA_OPTIONS)
        sp = None 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
    
    elif soortgroup == 'Rat val':
        functie = st.selectbox("Rat val", RAT_VAL_OPTIONS)
        sp = None 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
    
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    with st.expander("Upload een foto"):
        uploaded_file = st.camera_input("")
    
    st.divider()
        
    submitted = st.button("Gegevens opslaan")
    
    if submitted:           

        try:

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
                    insert_json(key,waarnemer,str(datum),str(time),soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project)
                
                else:
                    insert_json(key,waarnemer,str(datum),str(time),soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project)

                st.success('Gegevens opgeslagen!', icon="✅")
                
                
                

        except:
            st.stop()

        st.switch_page("🗺️_Home.py")

    

# --- APP ---  
try:
    st.logo(IMAGE,  link=None, icon_image=None)    
     
    output_map = map()
    
    try:
        if len(output_map["features"]) != 0:
            input_data(output_map)
    except:
        st.stop()
    
except:
    st.switch_page("🗺️_Home.py")
    
