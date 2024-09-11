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
    div.block-container {padding-top: 0rem; padding-bottom: 2rem; padding-left: 0rem; padding-right: 0rem; margin-top: 1em; margin-bottom: 2em;}
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")


# --- DIMENSIONS ---
OUTPUT_height = 610
OUTPUT_width = 350
CONTAINER_height = 640
ICON_SIZE = (21,21)
ICON_SIZE_huismus = (25,25)

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items    



def popup_html(row):
    
    i = row
     
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    soortgroup=df_2['soortgroup'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soortgroup</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(soortgroup) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html

IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, icon_image=None)

try:
    
    db_content = load_dataset()
    df_point = pd.DataFrame(db_content)
    
       
    df_2 = df_point
    
    df_2["icon_data"] = df_2.apply(lambda x: icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen'] 
                                   else icon_dictionary[x["soortgroup"]][x["functie"]], 
                                   axis=1
                     )
    
    map = folium.Map()
    LocateControl(auto_start=True).add_to(map)
    Fullscreen().add_to(map)
    
    fg = folium.FeatureGroup(name="Vleermuiskast")
    fg_2 = folium.FeatureGroup(name="Huismussen")
    fg_4 = folium.FeatureGroup(name="Gierzwaluwen")
    fg_3 = folium.FeatureGroup(name="Vleermuizen")
    fg_5 = folium.FeatureGroup(name="Camera")
    fg_6 = folium.FeatureGroup(name="Rat val")
    
    map.add_child(fg)
    map.add_child(fg_2)
    map.add_child(fg_4)
    map.add_child(fg_3)
    map.add_child(fg_5)
    map.add_child(fg_6)
    
    folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False).add_to(map)
    folium.LayerControl().add_to(map)
   

    
    
    for i in range(len(df_2)):

        if df_2.iloc[i]['geometry_type'] == "Point":

            html = popup_html(i)
            popup = folium.Popup(folium.Html(html, script=True), max_width=300)

            if df_2.iloc[i]['soortgroup'] == "Vleermuiskast":
                folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                              popup=popup,
                              icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg)

            elif df_2.iloc[i]['soortgroup'] == "Vogels":
                if df_2.iloc[i]['sp'] == "Huismus":
                    
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_huismus)).add_to(fg_2)
                    
                elif df_2.iloc[i]['sp'] == "Gierzwaluw":
                    
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_4)

            elif df_2.iloc[i]['soortgroup'] == "Vleermuizen":
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_3)

            elif df_2.iloc[i]['soortgroup'] == "Camera":
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_5)

            elif df_2.iloc[i]['soortgroup'] == "Rat val":
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_6)

                

        elif df_2.iloc[i]['geometry_type'] == "LineString":

            folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(fg)

    with st.container(height=CONTAINER_height, border=True):
        output_2 = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,feature_group_to_add=[fg,fg_2,fg_3,fg_4])
        
    try:
        
        id = str(output_2["last_active_drawing"]['geometry']['coordinates'][0])+str(output_2["last_active_drawing"]['geometry']['coordinates'][1])
        name = f"{id}.jpeg"

        with st.sidebar:

            

            try:

                res = drive.get(name).read()
                with st.expander("Zie foto"):
                    st.image(res)
                    
                with st.form("entry_form", clear_on_submit=True):
                    submitted = st.form_submit_button("Verwijder data")
                    if submitted:
                        # if waarnemer ==  df_point.set_index("key").loc[id,"waarnemer"]:
                            db.delete(id)
                            drive.delete(name)
                            st.success('Gegevens verwijderd!', icon="✅")
                            st.page_link("🗺️_Home.py", label="vernieuwen", icon="🔄")
                        # else:
                        #     st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")
                            

            except:
                st.info('Geen foto opgeslagen voor deze waarneming!')
                with st.form("entry_form", clear_on_submit=True):
                    submitted = st.form_submit_button("Verwijder data")
                    if submitted:
                        # if waarnemer == df_point.set_index("key").loc[id,"waarnemer"]:
                            db.delete(id)
                            st.success('Gegevens verwijderd!', icon="✅")
                            st.page_link("🗺️_Home.py", label="vernieuwen", icon="🔄")
                        # else:
                        #     st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")

    except:
        st.stop()

except:
    st.warning('problem')
    st.stop()
