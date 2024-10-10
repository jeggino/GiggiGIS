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
    page_title="GiggiGIS Desktop",
    initial_sidebar_state="collapsed",
    page_icon="📝",
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

# --- DIMENSIONS ---
#innerWidth = streamlit_js_eval(js_expressions='screen.width',  want_output = True, key = 'width')
#innerHeight = streamlit_js_eval(js_expressions='window.screen.height', want_output = True, key = 'height')
OUTPUT_width = 1190
OUTPUT_height = 450

    
# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

def insert_json(key,waarnemer,datum,datum_2,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"datum_2":datum_2,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates,"project":project})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True,},
        position="topright",).add_to(m)
    Fullscreen(position="topleft").add_to(m)
    LocateControl(auto_start=False,position="topleft").add_to(m)
    

    
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
    
        sp = st.selectbox("Soort", BAT_NAMES)
        gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
        functie = st.selectbox("Functie", BAT_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
        aantal = st.number_input("Aantal", min_value=1)
        datum_2 = None
    
    elif soortgroup == 'Vogels':
    
        sp = st.selectbox("Soort", BIRD_NAMES)
        gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
        functie = st.selectbox("Functie", BIRD_FUNCTIE) 
        verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
        aantal = st.number_input("Aantal", min_value=1)
        datum_2 = None
    
    elif soortgroup == 'Vleermuiskast':
        functie = st.selectbox("Voorwaarde", VLEERMUISKAST_OPTIONS)
        bat_names = ["onbekend"] + BAT_NAMES
        sp = st.selectbox("Soort", bat_names) 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
        datum_2 = None
    
    elif soortgroup == 'Camera':
        functie = st.selectbox("Camera", CAMERA_OPTIONS)
        
        if functie in ["Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd"]:
          datum_2 = st.date_input("Datum camera verwijderd","today")
        else:
          datum_2 = None
            
        sp = None 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
    
    elif st.session_state.project['opdracht'] == 'Vangkooi':
    
        functie = st.selectbox("Rat vangkooi", RAT_VANGKOOI_OPTIONS)
    
        if functie in ['vangkooi verwijderd, rat gevangen','vangkooi verwijderd, geen rat gevangen']:
          datum_2 = st.date_input("Datum vangkooi verwijderd","today")
        else:
          datum_2 = None
          
        sp = None 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)

    elif st.session_state.project['opdracht'] == 'Rat val':
    
        functie = st.selectbox("Rat val", RAT_VAL_OPTIONS)
    
        if functie in ['Schietval verwijderd, geen rat gedood','Schietval verwijderd, rat gedood']:
          datum_2 = st.date_input("Datum rat val verwijderd","today")
        else:
          datum_2 = None
          
        sp = None 
        gedrag = None
        verblijf = None
        aantal = st.number_input("Aantal", min_value=1)
    
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    with st.expander("Upload een foto"):
        uploaded_file = st.file_uploader("")
    
    st.divider()
        
    submitted = st.button("**Gegevens opslaan**",use_container_width=True)
    
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
                    # drive.put(f"{key}.jpeg", data=bytes_data)      
                    drive.put(f"{key}", data=bytes_data)            
                    insert_json(key,waarnemer,str(datum),str(datum_2),str(time),soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project)
                
                else:
                    insert_json(key,waarnemer,str(datum),str(datum_2),str(time),soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project)

                st.success('Gegevens opgeslagen!', icon="✅")       
                st.rerun()

        except:
            st.stop()

        
        # st.switch_page("pages/✍️_Voeg_een_waarneming_in.py")


    

# --- APP ---  
try:
    IMAGE = "image/logo.png"
    IMAGE_2 ="image/menu.jpg"
    st.logo(IMAGE,  link=None, icon_image=IMAGE_2)

    waarnemer = st.session_state.login['name']
    
    
    
    deta = Deta(st.secrets[f"deta_key_other"])
    db = deta.Base("df_observations")
    drive = deta.Drive("df_pictures")    

        
    output_map = map()
    
    try:
        if len(output_map["features"]) != 0:
            input_data(output_map)
    except:
        st.stop()
    
except:
    st.switch_page("🗺️_Home.py")
