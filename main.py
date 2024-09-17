import streamlit as st
from deta import Deta
import pandas as pd




st.set_page_config(page_title='References', page_icon='🔐', initial_sidebar_state='collapsed')



deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_authentication")
drive = deta.Drive("df_pictures")
db_content = db.fetch().items 
df_references = pd.DataFrame(db_content)
df_references
