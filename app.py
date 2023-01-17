
import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime

from deta import Deta

import string
import random



st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🍕",
    
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

BAT_BEHAVIOURS = ['foeragerend', 'roepend','verplaatsend (vliegroute)', 'sociale roep', 'uitvliegend','invliegend', 'overvliegend', 
           'nest-indicerend gedrag', 'zwermend', 'sporen', 'balts', 'verkeersslachtoffer','bezet nest']

BAT_FUNCTIE = ['geen / onbekend', 'zomerverblijfplaats in gebouw', 'paarverblijfplaats in gebouw','vliegroute', 'kraamverblijfplaats in gebouw',
           'vliegroute (bomen)', 'vliegroute (water)', 'zomerverblijfplaats in boom', 'paarverblijfplaats in boom', 
           'kraamverblijfplaats in boom', 'winterverblijfplaats in gebouw', 'massa winterverblijfplaats', 
           'essentieel foerageergebied (water)', 'winterverblijfplaats in bloei', 'essentieel foerageergebied (bomen)', 'vastgesteld territorium',
           'essentieel foerageergebied (grasland)']

BAT_VERBLIJF = ['geen / onbekend', 'dakgoot', 'spouwmuur', 'daklijst',
       'kantpan', 'regenpijp', 'holte', 'raamkozijn', 'luik', 'scheur',
       'schoorsteen', 'gevelbetimmering', 'nokpan', 'dakpan',
       'vleermuiskast', 'openingen in dak', 'dakkapel', 'schors']



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


# --- APP ---

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


with st.sidebar:
    option = st.radio("", options=('📝 Data Entry', '🗺️ Data Visualization'), horizontal=True, label_visibility="visible")
    
    "---"


if option == '📝 Data Entry':


    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3, width='100%', height='100%')
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)

    output = st_folium(m,  returned_objects=["all_drawings"])
    if output:

        with st.sidebar:

            date = st.date_input("Date")
            sp = st.selectbox("Soort", BAT_NAMES)
            n = st.number_input("Number of specimens:", min_value=0)
            comment = st.text_input("", placeholder="Enter a comment here ...")
            with st.expander("Upload a picture"):
                uploaded_file = st.camera_input("")

            try:

                new_dict = output
                new_dict["features"] = new_dict.pop("all_drawings")
                key = password_generator(12)

                if len(new_dict["features"]) > 1:
                    st.error("You cannot upload more than one survey at time!")
                    st.stop()

                else:


                    new_dict["features"][0]["properties"]["date"] = str(date)
                    new_dict["features"][0]["properties"]["sp"] = sp
                    new_dict["features"][0]["properties"]["n"] = n
                    new_dict["features"][0]["properties"]["comment"] = comment
                    new_dict["features"][0]["properties"]["id"] = key

                    with st.form("entry_form", clear_on_submit=True):
                        submitted = st.form_submit_button("Save Data")
                        if submitted:
                            # If user attempts to upload a file.
                            if uploaded_file is not None:
                                bytes_data = uploaded_file.getvalue()
                                

                                drive.put(f"{key}.jpeg", data=bytes_data)            
                                new_dict["features"][0]["properties"]["image_name"] = f"{key}.jpeg"
                                insert_json(new_dict,key)
                            else:
                                new_dict["features"][0]["properties"]["image_name"] = None
                                insert_json(new_dict,key)

                            st.success('Data saved!', icon="✅")
                            st.stop()

            except:

                st.info("Mark an observation")
                st.stop()


elif option == "🗺️ Data Visualization":
    
    try:
        db_content = db.fetch().items
        df_point = pd.DataFrame(db_content)

        map = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
        LocateControl(auto_start=True).add_to(map)

        for i in df_point["json"].to_list():
            folium.GeoJson(i,
                       tooltip=folium.GeoJsonTooltip(fields= ["date", "sp", "n", "comment"],
                                                     aliases=["Date: ", "Species: ", "Nember of specimens: ", "Comment: "],
                                                     labels=True,
                                                     style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
                                                   )
                       ).add_to(map)

        output = st_folium(map, width=500, height=700, returned_objects=["last_active_drawing"])

        with st.sidebar:

            try:
                id = output["last_active_drawing"]["properties"]["id"]
                name = output["last_active_drawing"]["properties"]["image_name"]
                
                with st.sidebar:
                
                    try:

                        res = drive.get(name).read()
                        with st.expander("See image"):
                            st.image(res)

                        with st.form("entry_form", clear_on_submit=True):
                            submitted = st.form_submit_button("Deleted Data")
                            if submitted:
                                db.delete(id)
                                drive.delete(name)
                                st.success('Data deleted!', icon="✅")

                    except:
                        st.warning('No picture saved!', icon="⚠️")
                        with st.form("entry_form", clear_on_submit=True):
                            submitted = st.form_submit_button("Deleted Data")
                            if submitted:
                                db.delete(id)
                                st.success('Data deleted!', icon="✅")
                        

            except:
                st.info("Select an observation")
                
    except:
        st.error('No data yet!', icon="🚨")
