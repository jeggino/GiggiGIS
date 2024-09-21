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



# ---LAYOUT---
st.set_page_config(
    page_title="GigGIS",
    initial_sidebar_state="collapsed",
    page_icon="📝",
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
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; margin-top: 1em; margin-bottom: 2em;}
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #FFFFFF;">
  <a class="navbar-brand" target="_blank">   </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
</nav>
""", unsafe_allow_html=True)


# --- DIMENSIONS ---
from streamlit_js_eval import streamlit_js_eval

WIDTH_SCREEN = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
HEIGHT_SCREEN = streamlit_js_eval(js_expressions='screen.height', key = 'SCR1')
st.write(f"Screen width is {WIDTH_SCREEN}")
st.write(f"Screen height is {HEIGHT_SCREEN}")
OUTPUT_height = streamlit_js_eval(WIDTH_SCREEN)
OUTPUT_width = streamlit_js_eval(HEIGHT_SCREEN)
CONTAINER_height = streamlit_js_eval(WIDTH_SCREEN)
    
# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

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

            # output["features"] = output.pop("all_drawings")
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
    IMAGE = "image/logo.png"
    st.logo(IMAGE,  link=None, icon_image=None)    

    
    
    deta = Deta(st.secrets[f"deta_key_other"])
    db = deta.Base("df_observations")
    drive = deta.Drive("df_pictures")    

    with st.container(height=CONTAINER_height, border=True):
        
        output_map = map()
    
    try:
        if len(output_map["features"]) != 0:
            input_data(output_map)
    except:
        st.stop()
    
except:
    st.switch_page("🗺️_Home.py")
    
