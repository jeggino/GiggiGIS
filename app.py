
import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime

from deta import Deta

    
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


def insert_json(json):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"json":json})

option = st.selectbox('',('Insert data', 'Data visualizsation'))


if option == 'Insert data':


    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3, width='100%', height='100%')
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=False).add_to(m)

    output = st_folium(m,  returned_objects=["all_drawings"])
    st.write(output)
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

                if len(new_dict["features"]) > 1:
                    st.error("You cannot upload more than one survey at time!")
                    st.stop()

                else:


                    new_dict["features"][0]["properties"]["date"] = str(date)
                    new_dict["features"][0]["properties"]["sp"] = sp
                    new_dict["features"][0]["properties"]["n"] = n
                    new_dict["features"][0]["properties"]["comment"] = comment

                    with st.form("entry_form", clear_on_submit=True):
                        submitted = st.form_submit_button("Save Data")
                        if submitted:
                            # If user attempts to upload a file.
                            if uploaded_file is not None:
                                bytes_data = uploaded_file.getvalue()
                                image_name = uploaded_file.name

                                drive.put(image_name, data=bytes_data)            
                                new_dict["features"][0]["properties"]["image_name"] = image_name
                                insert_json(new_dict)
                            else:
                                new_dict["features"][0]["properties"]["image_name"] = None
                                insert_json(new_dict)

                            st.success('Data saved!', icon="✅")
                            st.stop()

            except:

                st.info("mark an observation")
                st.stop()


elif option == "Data visualizsation":
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

    output = st_folium(map, width=500, height=700)
    
    
    output
    key = df_point[df_point.lat==output["last_object_clicked"]["lat"]]["key"].value[0]
    st.write(output["last_object_clicked"]["lat"])
    st.write(key)
    







