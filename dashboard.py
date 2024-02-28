import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import geopandas as gpd
import datetime
from datetime import date

from deta import Deta

st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🗺️",
    layout="wide",
    
)


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#GithubIcon {
  visibility: hidden;
}
</style> """, unsafe_allow_html=True)


# --- VARIABLES---

PASSWORD = "GiggiGIS"

GROUP = ["Vogels", "Vliermuizen"]

BAT_NAMES = ['Laatvlieger', 'Gewone dwergvleermuis', 'Watervleermuis',
       'Rosse vleermuis', 'Ruige dwergvleermuis', 'Meervleermuis',
       'Bosvleermuis', 'Franjestaart', 'Vleermuis onbekend',
       'Myotis spec.', 'Vale vleermuis', 'Gewone grootoorvleermuis',
       'Ingekorven vleermuis', 'Baardvleermuis', 'Brandts vleermuis',
       'Kleine dwergvleermuis', 'Grijze grootoorvleermuis',
       'Bechsteins vleermuis', 'Tweekleurige vleermuis',
       'Dwergvleermuis spec.', 'Plecotus spec.', 'Mopsvleermuis']

BIRD_NAMES = ['Gierzwaluw','Huismus']

BAT_BEHAVIOURS = ['foeragerend', 'roepend','verplaatsend (vliegroute)', 'sociale roep', 'uitvliegend','invliegend', 'overvliegend', 
           'nest-indicerend gedrag', 'zwermend', 'sporen', 'balts', 'verkeersslachtoffer','bezet nest']

BIRD_BEHAVIOURS = ['bezet nest', 'nest-indicerend gedrag', 'overvliegend',
       'foeragerend', 'ter plaatse', 'roepend', 'baltsend / zingend',
       'nestbouw', 'invliegend', 'uitvliegend', 'jagend',
       'roepend vanuit gebouw', 'baltsend / zingend op gebouw',
       'baltsend / zingend in vegetatie, struik of boom', 'sporen',
       'geen / onbekend', 'onbekend', 'vondst', 'paaiend',
       'verplaatsend (vliegroute)', 'copula']

BAT_FUNCTIE = ['geen / onbekend', 'zomerverblijfplaats in gebouw', 'paarverblijfplaats in gebouw','vliegroute', 'kraamverblijfplaats in gebouw',
           'vliegroute (bomen)', 'vliegroute (water)', 'zomerverblijfplaats in boom', 'paarverblijfplaats in boom', 
           'kraamverblijfplaats in boom', 'winterverblijfplaats in gebouw', 'massa winterverblijfplaats', 
           'essentieel foerageergebied (water)', 'winterverblijfplaats in bloei', 'essentieel foerageergebied (bomen)', 'vastgesteld territorium',
           'essentieel foerageergebied (grasland)']

BIRD_FUNCTIE = ['nestlocatie', 'geen / onbekend', 'vastgesteld territorium',
       'functioneel leefgebied', 'mogelijke nestlocatie',
       'voortplantingsbiotoop', 'winterverblijfplaats in boom',
       'zomerverblijfplaats']



BAT_VERBLIJF = ['geen / onbekend', 'dakgoot', 'spouwmuur', 'daklijst',
       'kantpan', 'regenpijp', 'holte', 'raamkozijn', 'luik', 'scheur',
       'schoorsteen', 'gevelbetimmering', 'nokpan', 'dakpan',
       'vleermuiskast', 'openingen in dak', 'dakkapel', 'schors']

BIRD_VERBLIJF = ['dakgoot', 'kantpan', 'zonnepaneel', 'nokpan', 'nestkast',
       'gevelbetimmering', 'openingen in dak', 'regenpijp',
       'geen / onbekend', 'dakpan', 'spouwmuur', 'onder dakrand',
       'raamkozijn', 'luik', 'schoorsteen', 'daklijst', 'dakkapel',
       'in struweel / struiken', 'holte', 'op / bij nest in boom',
       'scheur', 'vleermuiskast']



# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items



with st.sidebar:

    soortgroup = st.selectbox("Soortgroep", ['Vleermuizen',  'Vogels'])
    start_date, end_date = st.date_input('start date  - end date :', [date.today(),date.today()])
    geometry_type = st.multiselect("Type geometrie", ['Point',  'LineString', 'Polygon'])
            
    if soortgroup == 'Vleermuizen':
    
        sp = st.multiselect("Soort", BAT_NAMES)
        with st.expander("Kies het gedrag, de functie en het verblijf", expanded=False):
            gedrag = st.multiselect("Gedrag", BAT_BEHAVIOURS, BAT_BEHAVIOURS) 
            functie = st.multiselect("Functie", BAT_FUNCTIE, BAT_FUNCTIE) 
            verblijf = st.multiselect("Verblijf", BAT_VERBLIJF, BAT_VERBLIJF) 
    
    elif soortgroup == 'Vogels':
    
        sp = st.multiselect("Soort", BIRD_NAMES)
        with st.expander("Kies het gedrag, de functie en het verblijf", expanded=False):
            gedrag = st.multiselect("Gedrag", BIRD_BEHAVIOURS,BIRD_BEHAVIOURS) 
            functie = st.multiselect("Functie", BIRD_FUNCTIE,BIRD_FUNCTIE) 
            verblijf = st.multiselect("Verblijf", BIRD_VERBLIJF,BIRD_VERBLIJF) 

db_content = load_dataset()
df_point = pd.DataFrame(db_content)        
df_point['date'] = pd.to_datetime(df_point['date']).dt.date


mask_date = (df_point['date'] >= start_date) & (df_point['date'] <= end_date)
mask_geometry_type = (df_point.geometry_type.isin(geometry_type))
df_filter = df_point[mask_geometry_type & mask_date & (df_point.sp.isin(sp)) & (df_point.gedrag.isin(gedrag)) & (df_point.functie.isin(functie)) & (df_point.verblijf.isin(verblijf))]

df_filter
