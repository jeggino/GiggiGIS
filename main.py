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
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")
db_content = db.fetch().items 
df_point = pd.DataFrame(db_content)
SOORTGROUP = df_point.soortgroup.unique()


# ___APP___



if "login" not in st.session_state:
    st.write("LogIn please")
    logIn()
    st.stop()

if st.session_state.login['password'] != st.secrets['password']:
    f"Sorry {st.session_state.login['name']} your password is not correct"
    logIn()
    st.stop()

if 'project' not in st.session_state:  
    st.write("Chose a project")
    project()
    st.stop()

with st.sidebar:
    f"Hello {st.session_state.login['name']} you will work at the {st.session_state.project['project_name']} project. GOOD LUCK!!!"
    logOut_project()
    logOut()
    st.divider()


df_point
st.divider()

waarnemer = st.sidebar.selectbox("Chose an operator",WAARNEMERS)
df_point_2 = df_point[df_point['soortgroup']==st.session_state.project['project_name']]
df_point_2[df_point_2['waarnemer']==waarnemer]


"---"
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


 
   
    

