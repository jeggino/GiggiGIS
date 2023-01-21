import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime

from deta import Deta

import string
import random

from streamlit_elements import elements, mui, html


st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🍕",
    layout="wide",
    
)

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


# --- VARIABLES---

GROUP = ["Vogels", "Vliermuizen"]

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

BIRD_VERBLIJF = ['dakgoot', 'kantpan', 'zonnepaneel', 'nokpan', 'nestkast',
       'gevelbetimmering', 'openingen in dak', 'regenpijp',
       'geen / onbekend', 'dakpan', 'spouwmuur', 'onder dakrand',
       'raamkozijn', 'luik', 'schoorsteen', 'daklijst', 'dakkapel',
       'in struweel / struiken', 'holte', 'op / bij nest in boom',
       'scheur', 'vleermuiskast']



# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")

# --- FUNCTIONS ---


def insert_json(json, key):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"json":json, "key":key})


def password_generator(length):
    """ Function that generates a password given a length """

    uppercase_loc = random.randint(1,4)  # random location of lowercase
    symbol_loc = random.randint(5, 6)  # random location of symbols
    lowercase_loc = random.randint(7,12)  # random location of uppercase

    password = ''  # empty string for password

    pool = string.ascii_letters + string.punctuation  # the selection of characters used

    for i in range(length):

        if i == uppercase_loc:   # this is to ensure there is at least one uppercase
            password += random.choice(string.ascii_uppercase)

        elif i == lowercase_loc:  # this is to ensure there is at least one uppercase
            password += random.choice(string.ascii_lowercase)

        elif i == symbol_loc:  # this is to ensure there is at least one symbol
            password += random.choice(string.punctuation)

        else:  # adds a random character from pool
            password += random.choice(pool)

    return password  # returns the string

def map():
    
    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    output = st_folium(m, returned_objects=["all_drawings"], width=350, height=600)
    
    return  output
    

def input_data(date,sp,gedrag,functie,verblijf,aantal,opmerking,uploaded_file):
    
    with st.container():
        output = map()
    
    with st.sidebar:
        submitted = st.button("Gegevens opslaan")
        if submitted:           

            try:

                new_dict = output
                new_dict["features"] = new_dict.pop("all_drawings")
                key = password_generator(12)

                if len(new_dict["features"]) > 1:
                    st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                    st.stop()

                else:

                    new_dict["features"][0]["properties"]["date"] = str(date)
                    new_dict["features"][0]["properties"]["sp"] = sp
                    new_dict["features"][0]["properties"]["gedrag"] = gedrag
                    new_dict["features"][0]["properties"]["functie"] = functie
                    new_dict["features"][0]["properties"]["verblijf"] = verblijf
                    new_dict["features"][0]["properties"]["aantal"] = aantal
                    new_dict["features"][0]["properties"]["opmerking"] = opmerking
                    new_dict["features"][0]["properties"]["id"] = key

                    if uploaded_file is not None:
                        bytes_data = uploaded_file.getvalue()
                        drive.put(f"{key}.jpeg", data=bytes_data)            
                        new_dict["features"][0]["properties"]["image_name"] = f"{key}.jpeg"
                        insert_json(new_dict,key)
                    else:
                        new_dict["features"][0]["properties"]["image_name"] = None
                        insert_json(new_dict,key)

                    st.success('Gegevens opgeslagen!', icon="✅")

            except:
                st.info("Markeer een waarneming")
        
        



# --- APP ---
# horizontal menu
selected = option_menu(None, ['📝',  '🗺️'], default_index=0, orientation="horizontal")


 


if selected == '📝':
    
    with st.sidebar:
        soortgroup = st.radio("", options=('🦇 Vleermuizen', '🐦 Vogels'), horizontal=True, label_visibility="visible")    
        
        "---"

        date = st.date_input("Date")
        
        if soortgroup == '🦇 Vleermuizen':
            
            sp = st.selectbox("Soort", BAT_NAMES)
            gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
            functie = st.selectbox("Functie", BAT_FUNCTIE) 
            verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
            
        elif soortgroup == '🐦 Vogels':
            
            sp = st.selectbox("Soort", BIRD_NAMES)
            gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
            functie = st.selectbox("Functie", BIRD_FUNCTIE) 
            verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
            
        aantal = st.number_input("Aantal:", min_value=0)
        opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
        with st.expander("Upload een foto"):
            uploaded_file = st.camera_input("")
            
    input_data(date,sp,gedrag,functie,verblijf,aantal,opmerking,uploaded_file)
    
    


elif selected == "🗺️":
    
    @st.experimental_memo
    def convert_df(df):
       return df.to_csv(index=False).encode('utf-8')   

    try:
        db_content = db.fetch().items
        df_point = pd.DataFrame(db_content)
        csv = convert_df(df)
        
        st.download_button(
           "Press to Download",
           csv,
           "file.csv",
           "text/csv",
           key='download-csv'
        )
        

        map = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
        LocateControl(auto_start=True).add_to(map)
        Fullscreen().add_to(map)

        for i in df_point["json"].to_list():
            folium.GeoJson(i,
                       tooltip=folium.GeoJsonTooltip(fields= ['date','sp','gedrag','functie','verblijf','aantal','opmerking'],
                                                     aliases=['Date:','Soort:','Gedrag:','Functie:','Verblijf:','Aantal:','Opmerking:'],
                                                     labels=True,
                                                     style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
                                                   )
                       ).add_to(map)

        output = st_folium(map, returned_objects=["last_active_drawing"], width=350, height=600)

        with st.sidebar:

            try:
                id = output["last_active_drawing"]["properties"]["id"]
                name = output["last_active_drawing"]["properties"]["image_name"]

                with st.sidebar:

                    try:

                        res = drive.get(name).read()
                        with st.expander("Zie foto"):
                            st.image(res)

                        with st.form("entry_form", clear_on_submit=True):
                            submitted = st.form_submit_button("Verwijder data")
                            if submitted:
                                db.delete(id)
                                drive.delete(name)
                                st.success('Gegevens verwijderd!', icon="✅")
                                st.experimental_rerun()

                    except:
                        st.warning('Geen foto opgeslagen voor deze waarneming!', icon="⚠️")
                        with st.form("entry_form", clear_on_submit=True):
                            submitted = st.form_submit_button("Verwijder data")
                            if submitted:
                                db.delete(id)
                                st.success('Gegevens verwijderd!', icon="✅")
                                st.experimental_rerun()


            except:
                st.info("Selecteer een waarneming")

    except:
        st.error('Nog geen waarnemingen!', icon="🚨")
