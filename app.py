
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
    layout="wide"
)


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
db = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")

# -------------- FUNCTIONS --------------


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


with st.sidebar:
    option = st.radio("", options=('📝', '🗺️'), horizontal=True, label_visibility="visible")
#     option = st.selectbox('',('📝', '🗺️'))
    
    "---"


if option == '📝':


    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3, width='100%', height='100%')
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)

    output = st_folium(m,  returned_objects=["all_drawings"])
    if output:

        with st.sidebar:

            date = st.date_input("Date")
            sp = st.selectbox("Species", ["Anax imperator", "Ischnura elegans", "Lestes sponsa"])
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
                                

                                drive.put(image_name, data=bytes_data)            
                                new_dict["features"][0]["properties"]["image_name"] = key
                                insert_json(new_dict,key)
                            else:
                                new_dict["features"][0]["properties"]["image_name"] = None
                                insert_json(new_dict,key)

                            st.success('Data saved!', icon="✅")
                            st.stop()

            except:

                st.info("Mark an observation")
                st.stop()


elif option == "🗺️":
    
    db_content = db.fetch().items
    df_point = pd.DataFrame(db_content)

    map = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
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
            res = drive.get(name).read()
            
            with st.sidebar:
                with st.expander("See image"):
                    st.image(res)
            
            with st.form("entry_form", clear_on_submit=True):
                submitted = st.form_submit_button("Cancel Data")
                if submitted:
                    db.delete(id)
        except:
            st.info("Select an observation")







