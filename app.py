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



m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw().add_to(m)

c1, c2 = st.columns([3,2])


with c1:
    output = st_folium(m, width=700, height=500,returned_objects=["all_drawings"])

with c2:

    try:
        new_dict = output
        new_dict["features"] = new_dict.pop("all_drawings")
        new_dict["features"][0]["properties"] = {"option_selectbox":None,
                                                 "options_multiselect":None,
                                                 "age":None,
                                                 "number":None,
                                                 "date":None,}

        error_empty = st.empty()
        option_selectbox = st.selectbox('How would you like to be contacted?', ('Email', 'Home phone', 'Mobile phone'))
        new_dict["features"][0]["properties"]["option_selectbox"] = option_selectbox

        options_multiselect = st.multiselect( 'What are your favorite colors',['Green', 'Yellow', 'Red', 'Blue'],['Yellow', 'Red'])
        new_dict["features"][0]["properties"]["options_multiselect"] = options_multiselect

        age = st.slider('How old are you?', 0, 130, 25)
        new_dict["features"][0]["properties"]["age"] = age

        number = st.number_input('Insert a number')
        new_dict["features"][0]["properties"]["number"] = number

        date = st.date_input("When\'s your birthday",datetime.date(2019, 7, 6))
        new_dict["features"][0]["properties"]["date"] = date

        if len(new_dict["features"]) > 1:
            st.error("You cannot upload more than one survey at time!")
            st.stop()
            
        st.write(new_dict)

        with st.form("entry_form_2", clear_on_submit=False):
            submitted = st.form_submit_button("Save Data")
            if submitted:
                st.warning("Ti stanno prendendo per il culo!", icon="💀")
                db_2.put({"info":new_dict})
                st.success('Data saved!', icon="✅")




    except:
        st.info("mark an observation")
