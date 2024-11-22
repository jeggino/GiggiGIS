import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast

from credentials import *


# ---LAYOUT---
st.set_page_config(
    page_title="Ratten Terschelling - Input App",
    initial_sidebar_state="collapsed",
    page_icon="🐀",
    layout="wide",
    
)


st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] svg {
        height: 0rem;
        width: 0rem;
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
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 0rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

from functions import *

#---DATASET---
ttl = 0
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="ratten-terschelling")

# --- APP ---
if "login" not in st.session_state:
    logIn()
    st.stop()

with st.sidebar:
    logOut()
    st.divider()

    

IMAGE = "icon/menu.jpg"
st.logo(IMAGE,  link="https://www.elskenecologie.nl/#:~:text=Elsken%20Ecologie%20is%20het%20onafhankelijke%20ecologisch%20advies-%20en", icon_image=IMAGE)

# try:
    
df_2 = df_point
df_2["datum"] = pd.to_datetime(df_2["datum"]).dt.date
    
st.sidebar.subheader("Filter op",divider=False)
d = st.sidebar.slider("Datum", min_value=df_2.datum.min(),max_value=df_2.datum.max(),value=(df_2.datum.min(), df_2.datum.max()),format="DD-MM-YYYY")

df_2 = df_2[(df_2['datum']>=d[0]) & (df_2['datum']<=d[1])]

st.sidebar.divider()

df_2["icon_data"] = df_2.apply(lambda x: icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen'] 
                               else icon_dictionary[x["soortgroup"]][x["functie"]], 
                               axis=1
                 )
map = folium.Map(location=(df_2["lat"].mean(), df_2["lng"].mean()),zoom_start=11,tiles=None)
LocateControl(auto_start=True).add_to(map)
Fullscreen().add_to(map)

functie_dictionary = {}
functie_len = df_2['functie'].unique()

for functie in functie_len:
    functie_dictionary[functie] = folium.FeatureGroup(name=functie)     

for feature_group in functie_dictionary.keys():
    map.add_child(functie_dictionary[feature_group])

folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Stratenkaart").add_to(map)
folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)
folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=False,name="Satellietkaart").add_to(map)
folium.LayerControl().add_to(map)    

groups={}

for group in choice_opdracht:
    groups[group] = list(df_2[df_2.soortgroup==group]["functie"].unique())
    feature = [functie_dictionary[i] for i in groups[group]]

    key_list = list(DICT_SORTGROUP.keys())
    val_list = list(DICT_SORTGROUP.values())
    position = val_list.index(group)
    
    groups[group] = feature

groups = dict(zip(soortgroup, list(groups.values())))
GroupedLayerControl(
    groups=groups,
    exclusive_groups=False,
    collapsed=True,
).add_to(map)

for i in range(len(df_2)):

    if df_2.iloc[i]['functie'] == "Waarneming rat doorgegeven, geen actie op ondernomen":
        ICON_SIZE_2 = ICON_SIZE_rat_maybe

    elif df_2.iloc[i]['functie'] == "Rat geschoten":
        ICON_SIZE_2 = ICON_SIZE_rat_maybe

    else:
        ICON_SIZE_2 = ICON_SIZE
        

    html = popup_html(i,df_2)
    popup = folium.Popup(folium.Html(html, script=True), max_width=300)
    fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]

    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                  popup=popup,
                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
                 ).add_to(fouctie_loop)
            

output = st_folium(map,
                   returned_objects=["last_object_clicked"],
                   width=OUTPUT_width, height=OUTPUT_height,feature_group_to_add=list(functie_dictionary.values()))
try:
    if len(output["last_object_clicked"]) != 0:
        coordinates = output["last_object_clicked"]
               
        lng = coordinates["lng"]
        lat = coordinates['lat']
        
        id = str(lng)+str(lat)
        with st.sidebar:
            if st.button("Waarneming bijwerken",use_container_width=True):
                update_item(id)
                st.switch_page("🗺️_Home.py")
            with st.form("entry_form", clear_on_submit=True,border=False):
                submitted = st.form_submit_button(":red[**Verwijder waarneming**]",use_container_width=True)
                if submitted:
                    df_filter = df_point[df_point["key"]==id]
                    df_drop = df_point[~df_point.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
                    conn.update(worksheet='ratten-terschelling',data=df_drop)
                    st.success('Waarneming verwijderd', icon="✅") 
                    st.page_link("🗺️_Home.py", label="Vernieuwen", icon="🔄",use_container_width=True)

except:
    pass
# except:
#     st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
#     st.stop()
