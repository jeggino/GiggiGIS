import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
from streamlit_gsheets import GSheetsConnection

import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from credentials import *



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
OUTPUT_width = 1190
OUTPUT_height = 450


    
# --- FUNCTIONS ---
def insert_json(key,waarnemer,datum,datum_2,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates,project):
    
    data = [{"key":key, "waarnemer":waarnemer,"datum":datum,"datum_2":datum_2,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates,"project":project}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="df_observations",data=df_updated)      
  
def map():
    
    m = folium.Map()
    if st.session_state.project['opdracht'] == 'Vleermuizen':
        Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True},
            position="topright",).add_to(m)

    else:
        Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False},
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

    geometry_type = output["features"][0]["geometry"]["type"]
    
    st.divider()
    
    if soortgroup == 'Vleermuizen':
    
        sp = st.selectbox("Soort", BAT_NAMES)
         
        
        if geometry_type == 'Polygon':
            gedrag = None
            functie = st.selectbox("Functie", ["Foerageergebied","Paringsgebied"])
            verblijf = None

        elif geometry_type == 'LineString':
            gedrag = None
            functie = st.selectbox("Functie", ["linea della minchia","linea de lo strafogo"])
            verblijf = None

        else:
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

    elif soortgroup == 'Vogels-Overig':
    
        sp = st.selectbox("Soort", BIRD_NAMES_ANDER)
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

    # with st.expander("Upload een foto"):
    #     uploaded_file = st.file_uploader("")
    
    st.divider()
        
    submitted = st.button("**Gegevens opslaan**",use_container_width=True)
    
    if submitted:           

        try:

            # geometry_type = output["features"][0]["geometry"]["type"]
            coordinates = output["features"][0]["geometry"]["coordinates"] 
            
            if geometry_type in ["LineString",'Polygon']:

                lng = coordinates[0][0][0]
                lat = coordinates[0][0][1]
                key = str(lng)+str(lat)
            
            else: 
                
                lng = coordinates[0]
                lat = coordinates[1]
                coordinates = None
                
                key = str(lng)+str(lat)

            if len(output["features"]) > 1:
                st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                st.stop()

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
    
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_old = conn.read(ttl=0,worksheet="df_observations")

        
    output_map = map()
    
    try:
        if len(output_map["features"]) != 0:
            input_data(output_map)
    except:
        st.stop()
    
except:
    st.switch_page("🗺️_Home.py")
