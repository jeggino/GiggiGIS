import folium
import streamlit as st

from folium.plugins import Draw, Fullscreen
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

import pandas as pd

import datetime

from deta import Deta


st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🍕",
    layout="wide",
)


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
# Create a new database "example-db"
db_3 = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")


# -------------- FUNCTIONS --------------


def insert_json(json):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db_3.put({"json":json})

with st.sidebar:
    
    add_radio = st.radio(
        "pagina",
        ("📝", "🗺️")
    )

if add_radio == "📝":   
    loc = get_geolocation()
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
#     st.warning("Qui é il casino!", icon="💀")   
    c1, c2 = st.columns([3,2])
    with c1:
                
        m = folium.Map(location=[lat, lon], zoom_start=18)
        Draw().add_to(m)
        Fullscreen().add_to(m)
        output = st_folium(m, width=500, height=700, returned_objects=["all_drawings"])
        
                   
    with c2:

        try:
            new_dict = output
            new_dict["features"] = new_dict.pop("all_drawings")

            if len(new_dict["features"]) > 1:
                st.error("You cannot upload more than one survey at time!")
                st.stop()

            with st.form("entry_form", clear_on_submit=True):
                date = st.date_input("Date")
                sp = st.selectbox("Species", ["Anax imperator", "Ischnura elegans", "Lestes sponsa"])
                n = st.number_input("Number of specimens:", min_value=0)
                comment = st.text_input("", placeholder="Enter a comment here ...")
                with st.expander("Upload a picture"):
                    uploaded_file = st.camera_input("")
                
#                 geometry_type = new_dict["features"][0]["geometry"]["type"]
#                 geometry = new_dict["features"][0]   
                
                new_dict["features"][0]["properties"]["date"] = str(date)
                new_dict["features"][0]["properties"]["sp"] = sp
                new_dict["features"][0]["properties"]["n"] = n
                new_dict["features"][0]["properties"]["comment"] = comment
                
                submitted = st.form_submit_button("Save Data")
                if submitted:
                    # If user attempts to upload a file.
                    if uploaded_file is not None:
                        bytes_data = uploaded_file.getvalue()
                        # Upload the image to deta using put with filename and data.
                        drive.put(uploaded_file.name, data=bytes_data)
                        
                        # Generate random image name
                        image_name = ''
                        length = 12
                        for _ in range(length):
                            bits = random.getrandbits(8)
                            num = (int('{0:b}'.format(bits),2) + 33) % 127
                            image_name+= chr(num)
                            
                        new_dict["features"][0]["properties"]["image_name"] = image_name
                        
                        insert_json(new_dict)
                    else:
                        new_dict["features"][0]["properties"]["image_name"] = None
                        insert_json(new_dict)
                    
                    st.success('Data saved!', icon="✅")

        except:
            st.info("mark an observation")
            
elif add_radio == "🗺️":
    db_content = db_3.fetch().items
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
    st_folium(map)
   

