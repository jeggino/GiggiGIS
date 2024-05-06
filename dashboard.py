import streamlit as st
import pandas as pd

from deta import Deta

st.set_page_config(
    page_title="Dashboard_jobert_2024",
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
deta = Deta(st.secrets["deta_key_jobert"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items


db_content = load_dataset()
st.write(db_content)
