import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from datetime import datetime, timedelta, date

from credentials import *



# ---LAYOUT---
st.set_page_config(
    page_title="🦇🪶 SMPs",
    initial_sidebar_state="collapsed",
    page_icon="🦇🪶",
    layout="centered",
)


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

# --- FUNCTIONS ---
def insert_dagverslag(key,waarnemer,opdracht,gebied_id,bemonsteringsmoment,datum,start_time,eind_time,extra_velfwerker,temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking,df_old):
    
    data = [{"key":key, "waarnemer":waarnemer,"project":project,"gebied_id":gebied_id,'bemonsteringsmoment':bemonsteringsmoment,"datum":datum,
             "start_time":start_time,"eind_time":eind_time, "extra_velfwerker":extra_velfwerker, "temperatuur":temperatuur, "bewolking":bewolking,
             "neerslag":neerslag,"windkrcht":windkrcht,"windrichting":windrichting,"opmerking":opmerking}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="df_ekomaps_dagverslagen",data=df_updated)

#---DATASET---
ttl = '10m'
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=ttl,worksheet="df_ekomaps_dagverslagen")
df_projects = conn.read(ttl=ttl_references,worksheet="df_ekomaps_projects")

# --- APP ---
# try:
waarnemer = st.session_state.login['name']
project = st.session_state.project['project_name']
opdracht = st.session_state.project['opdracht']
gebied_id = st.session_state.project['area']
key = None

st.title(f'{project}')
st.header(f'Opdracht: **{opdracht}**',divider=True)

try:
    st.subheader(f'Opdracht: **{opdracht}**',divider=True)
except:
    pass

with st.form("my_form", clear_on_submit=True,border=False):
    bemonsteringsmoment = st.selectbox('Bemonsteringsmoment',('Kraamverblijf','Winterverblijf','Paarverblijf'))
    datum = st.date_input("Datum","today")       
    two_hours_from_now = datetime.now() + timedelta(hours=1)
    four_hours_from_now = datetime.now() + timedelta(hours=3)
    start_time = st.time_input("Start tijd", two_hours_from_now)
    eind_time = st.time_input("Eind tijd", four_hours_from_now)
    
    extra_velfwerker_list = df_projects.set_index('project').loc[project,"user"].split(',')
    extra_velfwerker_list.remove(waarnemer)
    extra_velfwerker = st.multiselect("Extra velfwerker",extra_velfwerker_list)
    
    temperatuur = st.number_input("Temperatuur",key='temperatuur', min_value=0)
    bewolking = st.selectbox("Bewolking",("Onbewolkt (<10%)", "Halfbewolkt (10-80%)", "Bewolkt (>80%)"))
    neerslag = st.selectbox("Neerslag",("Droog", "Nevel/mist", "Motregen", "Regen","Zware regen","Sneeuw"))
    windkrcht = st.number_input("windkrcht",key='windkrcht', min_value=1)
    windrichting = st.selectbox("Windrichting",("Noord", "Noordoost", "Oost", "Zuidoost","Zuid","Zuidwest","West","Noordwest"))
    
    if gebied_id == None:
        st.markdown("Vergeet a.u.b. niet in de opmerking te schrijven welke soort je hebt gevonden, de dichtstbijzijnde locaties en het doel van het onderzoek.")
        
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")
    
    
    if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):
        insert_dagverslag(key,waarnemer,opdracht,gebied_id,bemonsteringsmoment,datum,start_time,eind_time,extra_velfwerker,temperatuur,bewolking,neerslag,windkrcht,windrichting,opmerking,df_old)
    





