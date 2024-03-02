import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import date

from deta import Deta

import string
import random
from log_fun import *


st.set_page_config(
    page_title="GiggiGIS",
    page_icon="📝",
    layout="wide",
    
)

login()

if st.button("Logout"):
    st.cache_resource.clear()
    st.rerun()


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#GithubIcon {
  visibility: hidden;
}
</style> """, unsafe_allow_html=True)


# --- VARIABLES---

PASSWORD = "GiggiGIS"

GROUP = ["🪶 Vogels", "🦇 Vleermuizen", "🏠 Vleermuiskast"]

BAT_NAMES = ['Laatvlieger', 'Gewone dwergvleermuis', 'Watervleermuis',
       'Rosse vleermuis', 'Ruige dwergvleermuis', 'Meervleermuis',
       'Bosvleermuis', 'Franjestaart', 'Vleermuis onbekend',
       'Myotis spec.', 'Vale vleermuis', 'Gewone grootoorvleermuis',
       'Ingekorven vleermuis', 'Baardvleermuis', 'Brandts vleermuis',
       'Kleine dwergvleermuis', 'Grijze grootoorvleermuis',
       'Bechsteins vleermuis', 'Tweekleurige vleermuis',
       'Dwergvleermuis spec.', 'Plecotus spec.', 'Mopsvleermuis']

BIRD_NAMES = ['Gierzwaluw','Huismus']

BAT_BEHAVIOURS = ['foeragerend', 'roepend','verplaatsend (vliegroute)', 'sociale roep', 'uitvliegend','invliegend', 'overvliegend', 
           'nest-indicerend gedrag', 'zwermend', 'sporen', 'balts', 'verkeersslachtoffer','bezet nest']

BIRD_BEHAVIOURS = ['bezet nest', 'nest-indicerend gedrag', 'overvliegend',
       'foeragerend', 'ter plaatse', 'roepend', 'baltsend / zingend',
       'nestbouw', 'invliegend', 'uitvliegend', 'jagend',
       'roepend vanuit gebouw', 'baltsend / zingend op gebouw',
       'baltsend / zingend in vegetatie, struik of boom', 'sporen',
       'geen / onbekend', 'onbekend', 'vondst', 'paaiend',
       'verplaatsend (vliegroute)', 'copula']

BAT_FUNCTIE = ['geen / onbekend', 'zomerverblijfplaats in gebouw', 'paarverblijfplaats in gebouw','vliegroute', 'kraamverblijfplaats in gebouw',
           'vliegroute (bomen)', 'vliegroute (water)', 'zomerverblijfplaats in boom', 'paarverblijfplaats in boom', 
           'kraamverblijfplaats in boom', 'winterverblijfplaats in gebouw', 'massa winterverblijfplaats', 
           'essentieel foerageergebied (water)', 'winterverblijfplaats in bloei', 'essentieel foerageergebied (bomen)', 'vastgesteld territorium',
           'essentieel foerageergebied (grasland)']

BIRD_FUNCTIE = ['nestlocatie', 'geen / onbekend', 'vastgesteld territorium',
       'functioneel leefgebied', 'mogelijke nestlocatie',
       'voortplantingsbiotoop', 'winterverblijfplaats in boom',
       'zomerverblijfplaats']

BAT_VERBLIJF = ['geen / onbekend', 'dakgoot', 'spouwmuur', 'daklijst',
       'kantpan', 'regenpijp', 'holte', 'raamkozijn', 'luik', 'scheur',
       'schoorsteen', 'gevelbetimmering', 'nokpan', 'dakpan',
       'vleermuiskast', 'openingen in dak', 'dakkapel', 'schors']

VLEERMUISKAST_VERBLIJF = ["Op boom", "Op gebouw"]

BIRD_VERBLIJF = ['dakgoot', 'kantpan', 'zonnepaneel', 'nokpan', 'nestkast',
       'gevelbetimmering', 'openingen in dak', 'regenpijp',
       'geen / onbekend', 'dakpan', 'spouwmuur', 'onder dakrand',
       'raamkozijn', 'luik', 'schoorsteen', 'daklijst', 'dakkapel',
       'in struweel / struiken', 'holte', 'op / bij nest in boom',
       'scheur', 'vleermuiskast']



# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items

def insert_json(key,date,soortgroup,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key":key, "date":date,"soortgroup":soortgroup, "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"onbewoond":onbewoond})


def map():
    
    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    output = st_folium(m, returned_objects=["all_drawings"])
    
    return  output
    
def input_data(date,sp,gedrag,functie,verblijf,aantal,opmerking,uploaded_file,onbewoond):
    
    with st.container():
        output = map()
    
    with st.sidebar:
        submitted = st.button("Gegevens opslaan")
        if submitted:           

            try:

                json = output
                json["features"] = json.pop("all_drawings")
                geometry_type = json["features"][0]["geometry"]["type"]
                coordinates = json["features"][0]["geometry"]["coordinates"]                
                lng = coordinates[0]
                lat = coordinates[1]
                # key = password_generator(12)
                key = str(lng)+str(lat)

                if len(json["features"]) > 1:
                    st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                    st.stop()

                else:

                    if uploaded_file is not None:
                        bytes_data = uploaded_file.getvalue()
                        drive.put(f"{key}.jpeg", data=bytes_data)            
                        with st.spinner('Wait for it...'):
                            insert_json(key,str(date),soortgroup,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond)
                    else:
                        with st.spinner('Wait for it...'):
                            insert_json(key,str(date),soortgroup,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,onbewoond)

                    st.success('Gegevens opgeslagen!', icon="✅")

            except:
                st.info("Markeer een waarneming")
        

# --- APP ---
# horizontal menu
selected = option_menu(None, ['Data entry', 'Data visualization'], 
                       icons=["bi bi-pencil-square","bi bi-geo-alt-fill"],default_index=0, orientation="horizontal",menu_icon="cast",)


if selected == 'Data entry':
    
    with st.sidebar:
    
        soortgroup = st.selectbox("", GROUP)
        date = st.date_input("Date")        
    
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
    
    input_data(date,sp,gedrag,functie,verblijf,aantal,opmerking,uploaded_file,onbewoond)




elif selected == "Data visualization":  

    try:
        
        db_content = load_dataset()
        df_point = pd.DataFrame(db_content)
            
        
        df_2 = df_point

        icon = {"Gierzwaluw":"https://cdn-icons-png.flaticon.com/128/732/732126.png",
                "Huismus":"https://cdn-icons-png.flaticon.com/128/8531/8531874.png",
                "Bat": "https://cdn-icons-png.flaticon.com/128/2250/2250418.png",
                "Nest_bezet": "https://cdn-icons-png.flaticon.com/128/12085/12085929.png",
                "Nest_unbezet": "https://cdn-icons-png.flaticon.com/128/9468/9468770.png"}
        
        df_2["icon_data"] = df_2.apply(lambda x: icon[x["sp"]] if x["soortgroup"]=="🪶 Vogels" else (icon["Bat"] if x["soortgroup"]=="🦇 Vliermuizen"  else (icon["Nest_bezet"] if x["onbewoond"]=="Ja" else icon["Nest_unbezet"])), axis=1)
        
        map = folium.Map(zoom_start=8)
        fg = folium.FeatureGroup(name="Markers")
        LocateControl(auto_start=True).add_to(map)
        Fullscreen().add_to(map)        
        
        for i in range(len(df_2)):
            
            folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']], id=df_2.iloc[i]['key'],
                          popup=df_2.iloc[i]['key'],
                          icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=(30,30))).add_to(fg)

        output = st_folium(map,feature_group_to_add=fg)
        st.write(str(output["last_active_drawing"]['geometry']['coordinates'][0])+str(output["last_active_drawing"]['geometry']['coordinates'][1]))



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
                                password = st.text_input("", value="", type="password", label_visibility="collapsed")
                                if password == PASSWORD:
                                    db.delete(id)
                                    drive.delete(name)
                                    st.success('Gegevens verwijderd!', icon="✅")
                                elif password == "":
                                    st.info('Schrijf het wachtwoord op', icon="🕵️‍♀️")
                                else:
                                    st.warning('Het wachtwoord is niet correct!', icon="⚠️")
                                    

                    except:
                        st.warning('Geen foto opgeslagen voor deze waarneming!', icon="⚠️")
                        with st.form("entry_form", clear_on_submit=True):
                            submitted = st.form_submit_button("Verwijder data")
                            if submitted:
                                password = st.text_input("", value="", type="password", label_visibility="collapsed")
                                if password == PASSWORD:
                                    db.delete(id)
                                    st.success('Gegevens verwijderd!', icon="✅")
                                elif password == "":
                                    st.info('Schrijf het wachtwoord op', icon="🕵️‍♀️")
                                else:
                                    st.warning('Het wachtwoord is niet correct!', icon="⚠️")

            except:
                st.stop()

    except:
        st.stop()
