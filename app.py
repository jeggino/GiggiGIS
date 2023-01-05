import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium import st_folium

import datetime

from deta import Deta

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
# Create a new database "example-db"
db_2 = deta.Base("project_2")

# -------------- FUNCTIONS --------------

def insert_period(option_selectbox, options_multiselect, age, number, lat, lon, date):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db_2.put({"option_selectbox": option_selectbox, "options_multiselect": options_multiselect, "age": age, "number": number, "lat": lat, "lon": lon, "date":str(date)})



m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw().add_to(m)

c1, c2 = st.columns([3,2])


with c1:
    output = st_folium(m, width=700, height=500,returned_objects=["all_drawings"])

with c2:

    try:
        new_dict = output
        new_dict["features"] = new_dict.pop("all_drawings")
        
        if len(new_dict["features"]) > 1:
            st.error("You cannot upload more than one survey at time!")
            st.stop()
      
        # error_empty = st.empty()
        option_selectbox = st.selectbox('How would you like to be contacted?', ('Email', 'Home phone', 'Mobile phone'))
        options_multiselect = st.multiselect( 'What are your favorite colors',['Green', 'Yellow', 'Red', 'Blue'],['Yellow', 'Red'])
        age = st.slider('How old are you?', 0, 130, 25)
        number = st.number_input('Insert a number')
        date = st.date_input("When\'s your birthday",datetime.date(2019, 7, 6))
        lat = new_dict["features"][0]["geometry"]["coordinates"][0]
        lon = new_dict["features"][0]["geometry"]["coordinates"][1]

        
        with st.form("entry_form_2", clear_on_submit=False):
            submitted = st.form_submit_button("Save Data")
            if submitted:
                insert_period(option_selectbox, options_multiselect, age, number, lat, lon, date)
                # st.warning("Ti stanno prendendo per il culo!", icon="💀")
                st.success('Data saved!', icon="✅")




    except:
        st.info("mark an observation")
