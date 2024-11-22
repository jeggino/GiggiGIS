import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from datetime import datetime, timedelta, date

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

from credentials import *
import ast

#---DATASET---
ttl = 0
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="ratten-terschelling")
df_references = conn.read(ttl=ttl_references,worksheet="users-ratten_terschelling-input")


# --- FUNCTIONS ---
def popup_html(row,df_2):
    
    i = row

    datum=df_2['datum'].iloc[i] 
    datum_2=df_2['datum_2'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
    aantal=df_2['aantal'].iloc[i]
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum verwijderd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum_2) + """
    </tr>
    <tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal geschoten </span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
    </tr>

    </tbody>
    </table>
    </html>
    """
    return html


def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft")
    try:
        if name == None:
            st.stop()
        
        index = df_references[df_references['username']==name].index[0]
        true_password = df_references.loc[index,"password"]

    except:
        st.warning("De gebruikersnaam is niet correct.")
        st.stop()
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")


def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        # del st.session_state.project     
        st.rerun()


# --- FUNCTIONS ---
def insert_json(key,waarnemer,datum,datum_2,time,soortgroup,functie,geometry_type,lat,lng,aantal,opmerking,df_old):
    
    data = [{"key":key, "waarnemer":waarnemer,"datum":datum,"datum_2":datum_2,"time":time,"soortgroup":soortgroup, 
             "functie":functie,"geometry_type":geometry_type,"lat":lat,"lng":lng,"aantal":aantal,"opmerking":opmerking}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="ratten-terschelling",data=df_updated)
  
def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False},
        position="topright",).add_to(m)
    Fullscreen(position="topright").add_to(m)
      
    LocateControl(auto_start=True,position="topright").add_to(m)
        
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    output["features"] = output.pop("all_drawings")
    
    return  output

        
@st.dialog(" ")
def input_data(output,df_old):

    waarnemer = st.session_state.login['name']
    
    datum = st.date_input("Datum","today")       
    nine_hours_from_now = datetime.now() + timedelta(hours=2)
    time = st.time_input("Tijd", nine_hours_from_now)

    geometry_type = output["features"][0]["geometry"]["type"]
    
    st.divider()

    soortgroup = st.selectbox("Opdracht", ['Camera','Vangkooi','Rat val','Rat geschoten'])
    
    if soortgroup == 'Camera':
        functie = st.selectbox("Camera", CAMERA_OPTIONS,label_visibility='hidden')
        
        if functie in ["Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd"]:
          datum_2 = st.date_input("Datum camera verwijderd","today")
        else:
          datum_2 = None

        aantal = None
                
    elif soortgroup == 'Vangkooi':
    
        functie = st.selectbox("Rat vangkooi", RAT_VANGKOOI_OPTIONS,label_visibility='hidden')
    
        if functie in ['vangkooi verwijderd, rat gevangen','vangkooi verwijderd, geen rat gevangen']:
          datum_2 = st.date_input("Datum vangkooi verwijderd","today")
        else:
          datum_2 = None

        aantal = None
        
    elif soortgroup == 'Rat val':
    
        functie = st.selectbox("Rat val", RAT_VAL_OPTIONS,label_visibility='hidden')
    
        if functie in ['Schietval verwijderd, geen rat gedood','Schietval verwijderd, rat gedood']:
          datum_2 = st.date_input("Datum rat val verwijderd","today")
        else:
          datum_2 = None
            
        aantal = None

    elif soortgroup == 'Rat geschoten':

        functie = 'Rat geschoten'
        aantal = st.number_input("Aantal geschoten", min_value=1) 
        datum_2 = None
    
        
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    st.divider()
        
    submitted = st.button("**Gegevens opslaan**",use_container_width=True)
    
    if submitted:           

        try:

            coordinates = output["features"][0]["geometry"]["coordinates"] 
                        
            lng = coordinates[0]
            lat = coordinates[1]
            coordinates = None
            
            key = str(lng)+str(lat)

            if len(output["features"]) > 1:
                st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                st.stop()

            else:

                insert_json(key,waarnemer,str(datum),str(datum_2),str(time),soortgroup,functie,geometry_type,lat,lng,aantal,opmerking,df_old)

                # st.success('Gegevens opgeslagen!', icon="✅")       
                # st.rerun()
            st.success('Gegevens opgeslagen!', icon="✅")
                
        except:
            st.stop()
        st.switch_page("🗺️_Home.py")

@st.dialog(" ")
def update_item(id):

  datum = st.date_input("Datum","today")
  nine_hours_from_now = datetime.now() + timedelta(hours=2)
  time = st.time_input("Tijd", nine_hours_from_now)

  soortgroup = st.selectbox("Opdracht", ['Camera','Vangkooi','Rat val','Rat geschoten'])

  
  if soortgroup == 'Camera':
    
    functie = st.selectbox("Camera", CAMERA_OPTIONS)
    
    if functie in ["Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd"]:
      datum_2 = st.date_input("Datum camera verwijderd","today")
    else:
      datum_2 = None

    aantal = None
  
  elif soortgroup == 'Rat val':
    
    functie = st.selectbox("Rat val", RAT_VAL_OPTIONS)

    if functie in ['Schietval verwijderd, geen rat gedood','Schietval verwijderd, rat gedood']:
      datum_2 = st.date_input("Datum Val verwijderd","today")
    else:
      datum_2 = None

    aantal = None
      
  elif soortgroup == 'Vangkooi':
    
    functie = st.selectbox("Rat vangkooi", RAT_VANGKOOI_OPTIONS)

    if functie in ['vangkooi verwijderd, rat gevangen','vangkooi verwijderd, geen rat gevangen']:
      datum_2 = st.date_input("Datum vangkooi verwijderd","today")
    else:
      datum_2 = None

    aantal = None
      
  elif soortgroup == 'Rat geschoten':
  
    datum_2 = None
    functie = 'Rat geschoten'
    aantal = st.number_input("Aantal geschoten", min_value=1)
    
  opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")

  if st.button("**Update**",use_container_width=True):
    df = conn.read(ttl=0,worksheet="ratten-terschelling")
    df_filter = df[df["key"]==id].reset_index(drop=True)
    id_lat = df_filter['lat'][0]
    id_lng = df_filter['lng'][0]
    id_waarnemer = df_filter['waarnemer'][0]
    id_key = df_filter['key'][0]
    id_soortgroup = df_filter['soortgroup'][0]
    id_geometry_type = df_filter['geometry_type'][0]
      
    df_drop = df[~df.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
    conn.update(worksheet='df_observations',data=df_drop)
    df = conn.read(ttl=0,worksheet="df_observations")
      
    data = [{"key":id_key, "waarnemer":id_waarnemer,"datum":str(datum),"datum_2":str(datum_2),"time":time,"soortgroup":id_soortgroup,"functie":functie,
             "geometry_type":id_geometry_type,"lat":id_lat,"lng":id_lng,"aantal":aantal,"opmerking":opmerking}]
      
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df,df_new],ignore_index=True)
    conn.update(worksheet='ratten-terschelling',data=df_updated)
    st.switch_page("🗺️_Home.py")
