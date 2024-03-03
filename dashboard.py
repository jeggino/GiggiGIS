import streamlit as st
import pandas as pd

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




# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items


db_content = load_dataset()
df_point = pd.DataFrame(db_content)        
df_point['datum'] = pd.to_datetime(df_point['datum']).dt.date



df_point
