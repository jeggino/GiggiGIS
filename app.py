import folium
import streamlit as st
from folium.plugins import Draw

import geopandas
import pandas as pd

from streamlit_folium import st_folium

import datetime

from deta import Deta

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
# Create a new database "example-db"
db_2 = deta.Base("project_2")

# -------------- FUNCTIONS --------------

def insert_period(date, sp, n, comment, geometry_type, geometry):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db_2.put({ "date":str(date), "sp": sp, "n_specimens":n, "comment": comment, "geometry_type":geometry_type, "geometry":geometry})



m = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
Draw().add_to(m)

c1, c2 = st.columns([3,2])


with c1:
    output = st_folium(m,width=500, height=700, returned_objects=["all_drawings"])

with c2:

    try:
        new_dict = output
        new_dict["features"] = new_dict.pop("all_drawings")

        if len(new_dict["features"]) > 1:
            st.error("You cannot upload more than one survey at time!")
            st.stop()

        # error_empty = st.empty()
        with st.form("entry_form", clear_on_submit=True):
            date = st.date_input("Date")
            sp = st.selectbox("Species", ["Anax imperator", "Ischnura elegans", "Lestes sponsa"])
            n = st.number_input("Number of specimens:", min_value=0)
            comment = st.text_input("", placeholder="Enter a comment here ...")
            geometry_type = new_dict["features"][0]["geometry"]["type"]
            geometry = new_dict["features"][0]["geometry"]
            
            st.warning("Qui é il casino!", icon="💀")

            submitted = st.form_submit_button("Save Data")
            if submitted:
                insert_period(date, sp, n, comment, geometry_type, geometry)
                st.success('Data saved!', icon="✅")

    except:
        st.info("mark an observation")
        
db_content = db_2.fetch().items
df_point = pd.DataFrame(db_content)
gdf = geopandas.GeoDataFrame(db_content, geometry=db_content.geometry)
st.dataframe(df_point)
st_folium(gdf.explore())
