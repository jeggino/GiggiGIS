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
from functions import *


# ---LAYOUT---
st.set_page_config(
    page_title="GigGIS",
    initial_sidebar_state="collapsed",
    page_icon="📝",
    layout="wide",
    
)

 

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_ } 
    </style>
    """,
    unsafe_allow_html=True)

reduce_header_height_style = """
<style>
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem;}  header { visibility: hidden; padding-top: 0rem}
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)



# --- COSTANTS ---
IMAGE = "image/logo.png"


# # --- DATASET ---
# deta = Deta(st.secrets[f"deta_key_other"])
# db = deta.Base("df_observations")
# drive = deta.Drive("df_pictures") 
    


    

# --- APP ---  
try:
    st.logo(IMAGE,  link=None, icon_image=None)    

    waarnemer = st.session_state.login['name']
     
    output_map = map()
    
    try:
        if len(output_map["features"]) != 0:
            input_data(output_map)
    except:
        st.stop()
    
except:
    st.switch_page("🗺️_Home.py")
    
