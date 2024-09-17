import streamlit as st
from deta import Deta
import pandas as pd
import folium
from folium.plugins import  Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

import geopandas as gpd
import datetime
from datetime import date
import random

from costants import *
from functions import *


st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')



deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_authentication")
drive = deta.Drive("df_pictures")
db_content = db.fetch().items 
df_references = pd.DataFrame(db_content)
df_references
