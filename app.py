import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
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

import time


st.set_page_config(
    page_title="GigGIS",
    page_icon="📝",
    layout="wide",
    
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    
    waarnemer = st.session_state["name"]
    
    
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    #GithubIcon {
      visibility: hidden;
    }
    </style> """, unsafe_allow_html=True)

    padding = 0
    st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: {padding}rem;
            padding-right: {padding}rem;
            padding-left: {padding}rem;
            padding-bottom: {padding}rem;
        }} </style> """, unsafe_allow_html=True)
    
    
    
    # --- CONNECT TO DETA ---
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("df_observations")
    drive = deta.Drive("df_pictures")
    
    # --- FUNCTIONS ---
    
    def load_dataset():
        return db.fetch().items
    
    def insert_json(key,waarnemer,datum,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates):
        
        return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"soortgroup":soortgroup, "aantal":aantal,
                       "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                       "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"onbewoond":onbewoond,"coordinates":coordinates})
    
    
    def map():
        
        m = folium.Map()
        Draw(export=True,draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
        Fullscreen().add_to(m)
        LocateControl(auto_start=True).add_to(m)
        output = st_folium(m, returned_objects=["all_drawings"])
        
        return  output
    
    
    def input_data():
        
        with st.container():
            output = map()
        
        with st.sidebar:
            
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
                            with st.spinner('Wait for it...'):
                                insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)
                        else:
                            with st.spinner('Wait for it...'):
                                insert_json(key,waarnemer,str(datum),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond,coordinates)
    
                        st.success('Gegevens opgeslagen!', icon="✅")
    
                except:
                    st.info("Markeer een waarneming")
    
    
    def popup_html(row):
        
        i = row
         
        datum=df_2['datum'].iloc[i] 
        soortgroup=df_2['soortgroup'].iloc[i]
        sp = df_2['sp'].iloc[i] 
        functie=df_2['functie'].iloc[i]
        gedrag=df_2['gedrag'].iloc[i]
        verblijf=df_2['verblijf'].iloc[i]
        bewoond=df_2['onbewoond'].iloc[i] 
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
        <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Bewoond</span></td>
        <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(bewoond) + """
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
            
    
    # --- APP ---
    # horizontal menu
    selected = option_menu(None, ['Datavisualisatie','Voeg een waarneming in'], 
                           icons=["bi bi-geo-alt-fill","bi bi-pencil-square"],
                           default_index=0,
                           orientation="horizontal")


    if selected == 'Voeg een waarneming in':
        
        with st.sidebar:
        
            soortgroup = st.selectbox("", GROUP)
            datum = st.date_input("Datum")        
        
            if soortgroup == '🦇 Vleermuizen':
        
                sp = st.selectbox("Soort", BAT_NAMES)
                gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
                functie = st.selectbox("Functie", BAT_FUNCTIE) 
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
                sp = st.selectbox("Soort", BAT_NAMES) 
                gedrag = None
                functie = None
                verblijf = None
                
        
            aantal = st.number_input("Aantal", min_value=0)
            opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
            
            with st.expander("Upload een foto"):
                uploaded_file = st.camera_input("")
        
        input_data()
    
    elif selected == "Datavisualisatie":  
    
        try:
            
            db_content = load_dataset()
            df_point = pd.DataFrame(db_content)
                
            
            df_2 = df_point
            
            df_2["icon_data"] = df_2.apply(lambda x: ICON[x["sp"]] if x["soortgroup"]=="Vogels" 
                                           else (ICON["Bat"] if x["soortgroup"]=="Vleermuizen"  
                                                 else (ICON["Nest_bezet"] if x["onbewoond"]=="Ja" 
                                                       else ICON["Nest_unbezet"])), axis=1)
            
            map = folium.Map(zoom_start=8)
            fg = folium.FeatureGroup(name="Markers")
            LocateControl(auto_start=True).add_to(map)
            Fullscreen().add_to(map)        
            
            for i in range(len(df_2)):

                if df_2.iloc[i]['geometry_type'] == "Point":
    
                    html = popup_html(i)
                    popup = folium.Popup(folium.Html(html, script=True), max_width=300)
                    
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']], id=df_2.iloc[i]['key'],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=(30,30))).add_to(map)

                elif df_2.iloc[i]['geometry_type'] == "LineString":

                    folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(fg)
    
            output = st_folium(map)
            output["features"] = output.pop("all_drawings")
            geometry_type = output["features"][0]["geometry"]["type"]
            coordinates = output["features"][0]["geometry"]["coordinates"] 
    
            with st.sidebar:
    
                try:
                    
                    id = str(output["last_active_drawing"]['geometry']['coordinates'][0])+str(output["last_active_drawing"]['geometry']['coordinates'][1])
                    name = f"{id}.jpeg"
            
                    with st.sidebar:
    
                        try:
    
                            res = drive.get(name).read()
                            with st.expander("Zie foto"):
                                st.image(res)
                                
                            with st.form("entry_form", clear_on_submit=True):
                                submitted = st.form_submit_button("Verwijder data")
                                if submitted:
                                    if waarnemer ==  df_point.set_index("key").loc[id,"waarnemer"]:
                                        db.delete(id)
                                        drive.delete(name)
                                        st.success('Gegevens verwijderd!', icon="✅")
                                    else:
                                        st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")
                                        
    
                        except:
                            st.warning('Geen foto opgeslagen voor deze waarneming!', icon="⚠️")
                            with st.form("entry_form", clear_on_submit=True):
                                submitted = st.form_submit_button("Verwijder data")
                                if submitted:
                                    if waarnemer == df_point.set_index("key").loc[id,"waarnemer"]:
                                        db.delete(id)
                                        st.success('Gegevens verwijderd!', icon="✅")
                                    else:
                                        st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")
    
                except:
                    st.stop()
    
        except:
            st.stop()
