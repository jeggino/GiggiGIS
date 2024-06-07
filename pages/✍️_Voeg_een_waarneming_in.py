import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import date

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
    .appview-container .main .block-container {padding-top: 0em; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; margin-top: -3em; margin-bottom: 2em;}
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

def insert_json(key,waarnemer,datum,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates,project):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"onbewoond":onbewoond,"coordinates":coordinates,"project":project})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False,}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    

    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    
    return  output



def input_data(output):

    # with st.container(height=CONTAINER_height, border=True):
        
    #     output = map()

    output = output
    
        
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
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates,project)
                
                else:
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates,project)

                st.success('Gegevens opgeslagen!', icon="✅")
                
                
                

        except:
            st.info("Markeer een waarneming")
            st.stop()

        st.switch_page("🗺️_Home.py")

    

# --- APP ---  
# popover = st.popover("🗒️")
@st.experimental_dialog("Cast your vote")
def vote():
    try:
        waarnemer = st.session_state["name"]
        
        if waarnemer == 'Luigi Giugliano':
            deta = Deta(st.secrets[f"deta_key_jobert"])
            db = deta.Base("df_observations")
            drive = deta.Drive("df_pictures")
    
        else:
            deta = Deta(st.secrets[f"deta_key_other"])
            db = deta.Base("df_observations")
            drive = deta.Drive("df_pictures")
            
        
    except:
        st.switch_page("🗺️_Home.py")
    
    
        
    st.page_link("🗺️_Home.py", label="Annuleren", icon="❌")
    if waarnemer == 'Luigi Giugliano':
        project = st.selectbox("Project", ["Zaandam","Badhoevedorp"],key="project")
    else:
        project = None
        
    soortgroup = st.selectbox("", GROUP)
    datum = st.date_input("Datum","today")       
    time = st.time_input("Tijd", "now")
    
    if soortgroup == '🦇 Vleermuizen':
    
        sp = st.selectbox("Soort", BAT_NAMES,key="Soort")
        gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
        functie = st.selectbox("Functie", BAT_FUNCTIE, help=HELP_FUNCTIE ) 
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
        sp = popover.selectbox("Soort", BAT_NAMES) 
        gedrag = None
        functie = None
        verblijf = None
        
    
    aantal = st.number_input("Aantal", min_value=0)
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    with st.expander("Upload een foto"):
        uploaded_file = st.camera_input("")

    ####
    input_data(output)
    ###
    

if st.button("jhkal"):
    vote(output)
    
with st.container(height=CONTAINER_height, border=True):
    
    output = map()


    
# input_data(output)

