import streamlit as st
from streamlit_js_eval import streamlit_js_eval

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date
import random

from deta import Deta

from credencials import *


# ---LAYOUT---
st.set_page_config(
    page_title="GigGIS",
    initial_sidebar_state="collapsed",
    page_icon="📝",
    layout="wide",
    
)


WIDTH_SCREEN = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
HEIGHT_SCREEN = streamlit_js_eval(js_expressions='screen.height', key = 'SCR1')
OUTPUT_height = int(HEIGHT_SCREEN) * 0.75
OUTPUT_width = WIDTH_SCREEN 
ICON_SIZE = (20,20)
ICON_SIZE_huismus = (28,28)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_ } 
    </style>
    """,
    unsafe_allow_html=True)

reduce_header_height_style = """
<style>
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem;}  header { visibility: hidden; padding-top: 0rem}
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


# --- DATASET ---
deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")
db_content = db.fetch().items 
df_point = pd.DataFrame(db_content)


db_2 = deta.Base("df_authentication")
db_content_2 = db_2.fetch().items 
df_references = pd.DataFrame(db_content_2)





# --- FUNCTIONS ---    
def load_dataset():
    return db.fetch().items





def popup_html(row):
    
    i = row

    project=df_2['project'].iloc[i]
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Project</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(project) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Verblijf</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(verblijf) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(int(aantal)) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html

@st.dialog(" ")
def update_item():

  datum = st.date_input("Datum","today")
  nine_hours_from_now = datetime.now() + timedelta(hours=2)
  time = st.time_input("Tijd", nine_hours_from_now)
  
  if st.session_state.project['opdracht'] == 'Vleermuizen':

    sp = st.selectbox("Soort", BAT_NAMES,key="Soort")
    gedrag = st.selectbox("Gedrag", BAT_BEHAVIOURS) 
    functie = st.selectbox("Functie", BAT_FUNCTIE, help=HELP_FUNCTIE ) 
    verblijf = st.selectbox("Verblijf", BAT_VERBLIJF) 
    aantal = st.number_input("Aantal", min_value=1)

  elif st.session_state.project['opdracht'] == 'Vogels':
  
    sp = st.selectbox("Soort", BIRD_NAMES)
    gedrag = st.selectbox("Gedrag", BIRD_BEHAVIOURS) 
    functie = st.selectbox("Functie", BIRD_FUNCTIE) 
    verblijf = st.selectbox("Verblijf", BIRD_VERBLIJF) 
    aantal = st.number_input("Aantal", min_value=1)
  
  elif st.session_state.project['opdracht'] == 'Vleermuiskast':
    
    functie = st.selectbox("Voorwaarde", VLEERMUISKAST_OPTIONS)
    BAT_NAMES = ["onbekend"] + BAT_NAMES
    sp = st.selectbox("Soort", BAT_NAMES) 
    gedrag = None
    verblijf = None
    aantal = st.number_input("Aantal", min_value=1)
  
  elif st.session_state.project['opdracht'] == 'Camera':
    
    functie = st.selectbox("Camera", CAMERA_OPTIONS)
    sp = None 
    gedrag = None
    verblijf = None
    aantal = st.number_input("Aantal", min_value=1)
  
  elif st.session_state.project['opdracht'] == 'Rat val':
    
    functie = st.selectbox("Rat val", RAT_VAL_OPTIONS)
    sp = None 
    gedrag = None
    verblijf = None
    aantal = st.number_input("Aantal", min_value=1)
  
  opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")


  update = {"datum":str(datum),"time":str(time),"sp":sp,
            "aantal":aantal, "gedrag":gedrag, "functie":functie, 
            "verblijf":verblijf,"opmerking":opmerking}
    
  if st.button("Update",use_container_width=True): 
    db.update(update,id)
    st.rerun()

def logIn():
    name = st.selectbox("Wie ben je?",df_references["username"].tolist(),index=None)  
    password = st.text_input("Vul het wachtwoord in, alstublieft")
    if name == None:
        st.stop()
    index = df_references[df_references['username']==name].index[0]
    true_password = df_references.loc[index,"password"]
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

def project():
    st.subheader(f"Welkom {st.session_state.login['name'].split()[0]}!!",divider='grey')
    index_project = df_references[df_references['username']==st.session_state.login["name"]].index[0]
    project_list = df_references.loc[index_project,"project"]
    project = st.selectbox("Aan welke project ga je werken?",project_list,label_visibility="visible")
    opdracht = st.selectbox("Aan welke opdracht ga je werken?",DICTIONARY_PROJECTS[project],label_visibility="visible")
    if st.button("begin"):
         st.session_state.project = {"project_name": project,"opdracht": opdracht}
         st.rerun()
def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        del st.session_state.project     
        st.rerun()

def logOut_project():
    if st.button("Opdracht wijzigen",use_container_width=True):
        del st.session_state.project
        st.rerun()
        


if "login" not in st.session_state:
    logIn()
    st.stop()


if 'project' not in st.session_state:  
    project()
    st.stop()

#______________NEW___________________



with st.sidebar:
    logOut_project()
    logOut()
    st.divider()

    
    

IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, icon_image=None)

try:

    db_content = load_dataset()
    df_point = pd.DataFrame(db_content)
    
       
    df_2 = df_point[df_point['soortgroup']==st.session_state.project['opdracht']]
    df_2["datum_2"] = pd.to_datetime(df_2["datum"]).dt.date
    st.sidebar.subheader("Filter op",divider=False)
    d = st.sidebar.date_input(
        "Datum",
        min_value = df_2.datum_2.min(),
        max_value = df_2.datum_2.max(),
        value=(df_2.datum_2.min(),
         df_2.datum_2.max()),
        format="YYYY.MM.DD",
    )
    
    df_2 = df_2[(df_2['datum_2']>=d[0]) & (df_2['datum_2']<=d[1])]
    
    if st.session_state.project['opdracht'] in ["Vleermuizen","Vogels"]:
        species_filter_option = df_2["sp"].unique()
        species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
        df_2 = df_2[df_2['sp'].isin(species_filter)]

    st.sidebar.divider()

    
    
    df_2["icon_data"] = df_2.apply(lambda x: icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen'] 
                                   else icon_dictionary[x["soortgroup"]][x["functie"]], 
                                   axis=1
                     )
    
    map = folium.Map()
    LocateControl(auto_start=True).add_to(map)
    Fullscreen().add_to(map)
    
    functie_dictionary = {}
    functie_len = df_2['functie'].unique()
    
    for functie in functie_len:
        functie_dictionary[functie] = folium.FeatureGroup(name=functie)     
    
    for feature_group in functie_dictionary.keys():
        map.add_child(functie_dictionary[feature_group])

    folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False).add_to(map)
    folium.LayerControl().add_to(map)    

    for i in range(len(df_2)):

        if df_2.iloc[i]['geometry_type'] == "Point":

            if (df_2.iloc[i]['sp']=="Huismus") & (df_2.iloc[i]['functie'] in ["mogelijke nestlocatie","nestlocatie"]):
                ICON_SIZE_2 = ICON_SIZE_huismus

            else:
                ICON_SIZE_2 = ICON_SIZE
                

            html = popup_html(i)
            popup = folium.Popup(folium.Html(html, script=True), max_width=300)
            fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
    
            folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                          popup=popup,
                          icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
                         ).add_to(fouctie_loop)
        
                

        elif df_2.iloc[i]['geometry_type'] == "LineString":

            folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(fg)

    output_2 = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
                         feature_group_to_add=list(functie_dictionary.values()))
        
    try:
        
        id = str(output_2["last_active_drawing"]['geometry']['coordinates'][0])+str(output_2["last_active_drawing"]['geometry']['coordinates'][1])
        name = f"{id}.jpeg"

        with st.sidebar:

            
            try:

                res = drive.get(name).read()
                with st.expander("Zie foto"):
                    st.image(res)
                if st.button("Do you want to update?",use_container_width=True):
                    update_item()
                    
                with st.form("entry_form", clear_on_submit=True):
                    submitted = st.form_submit_button("Verwijder data")
                    if submitted:
                        # if waarnemer ==  df_point.set_index("key").loc[id,"waarnemer"]:
                            db.delete(id)
                            drive.delete(name)
                            st.success('Gegevens verwijderd!', icon="✅")
                            st.page_link("🗺️_Home.py", label="vernieuwen", icon="🔄")
                        # else:
                        #     st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")
                            

            except:
                st.info('Geen foto opgeslagen voor deze waarneming!')

                if st.button("Do you want to update?",use_container_width=True):
                    update_item()
                
                with st.form("entry_form", clear_on_submit=True):
                    submitted = st.form_submit_button("Verwijder data")
                    if submitted:
                        # if waarnemer == df_point.set_index("key").loc[id,"waarnemer"]:
                            db.delete(id)
                            st.success('Gegevens verwijderd!', icon="✅")
                            st.page_link("🗺️_Home.py", label="vernieuwen", icon="🔄")
                        # else:
                        #     st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")

    except:
        st.stop()

except:
    st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
    st.stop()
