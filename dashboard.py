import streamlit as st
import pandas as pd

from deta import Deta

st.set_page_config(
    page_title="Dashboard_jobert_2024",
    page_icon="🗺️",
    initial_sidebar_state="collapsed",
    layout="wide",
    
)


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#GithubIcon {
  visibility: hidden;
}
</style> """, unsafe_allow_html=True)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)




# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---

def load_dataset():
    return db.fetch().items


db_content = pd.DataFrame(load_dataset())

st.dataframe(data=db_content, width=None, height=None, use_container_width=False, hide_index=True, column_order=None, column_config=None)
