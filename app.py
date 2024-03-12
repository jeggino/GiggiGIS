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
        Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
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



"---"
from dataclasses import dataclass
from typing import Dict, List, Optional

import folium
import requests
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(layout="wide")


@st.cache_resource
def get_data() -> List[Dict]:
    api_key = st.secrets["api_key"]
    url = f"https://developer.nps.gov/api/v1/parks?api_key={api_key}&limit=500"
    resp = requests.get(url)
    data = resp.json()["data"]
    parks = [park for park in data if park["designation"] == "National Park"]

    for park in parks:
        park["_point"] = Point.from_dict(park)

    return parks


@dataclass
class Point:
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: Dict) -> "Point":
        if "lat" in data:
            return cls(float(data["lat"]), float(data["lng"]))
        elif "latitude" in data:
            return cls(float(data["latitude"]), float(data["longitude"]))
        else:
            raise NotImplementedError(data.keys())

    def is_close_to(self, other: "Point") -> bool:
        close_lat = self.lat - 0.0001 <= other.lat <= self.lat + 0.0001
        close_lon = self.lon - 0.0001 <= other.lon <= self.lon + 0.0001
        return close_lat and close_lon


@dataclass
class Bounds:
    south_west: Point
    north_east: Point

    def contains_point(self, point: Point) -> bool:
        in_lon = self.south_west.lon <= point.lon <= self.north_east.lon
        in_lat = self.south_west.lat <= point.lat <= self.north_east.lat

        return in_lon and in_lat

    @classmethod
    def from_dict(cls, data: Dict) -> "Bounds":
        return cls(
            Point.from_dict(data["_southWest"]), Point.from_dict(data["_northEast"])
        )


#############################
# Streamlit app
#############################

"## National Parks in the United States"

"""
The National Parks Service provides an
[API](https://www.nps.gov/subjects/digital/nps-data-api.htm) to programmatically explore
NPS data.

We can take data about each park and display it on the map _conditionally_ based on
whether it is in the viewport.

---
"""

# define layout
c1, c2 = st.columns(2)

# get and cache data from API
parks = get_data()

# layout map
with c1:
    """(_Click on a pin to bring up more information_)"""
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=4)

    for park in parks:
        popup = folium.Popup(
            
            ,
            max_width=250,
        )
        folium.Marker([park["latitude"], park["longitude"]], popup=popup).add_to(m)

    map_data = st_folium(m, key="fig1", width=700, height=700)

# get data from map for further processing
map_bounds = Bounds.from_dict(map_data["bounds"])

# when a point is clicked, display additional information about the park
try:
    point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])

    if point_clicked is not None:
        with st.spinner(text="loading image..."):
            for park in parks:
                if park["_point"].is_close_to(point_clicked):
                    with c2:
                        f"""### _{park["fullName"]}_"""
                        park["description"]
                        st.image(
                            park["images"][0]["url"],
                            caption=park["images"][0]["caption"],
                        )
                        st.expander("Show park full details").write(park)
except TypeError:
    point_clicked = None

# even though there is a c1 reference above, we can do it again
# output will get appended after original content
with c1:
    parks_in_view: List[Dict] = []
    for park in parks:
        if map_bounds.contains_point(park["_point"]):
            parks_in_view.append(park)

    "Parks visible:", len(parks_in_view)
    "Bounding box:", map_bounds
