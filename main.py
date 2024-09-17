import streamlit as st
from deta import Deta
import pandas as pd



deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_authentication")
db_content = db.fetch().items 
df_references = pd.DataFrame(db_content)


@st.dialog("Cast your vote")
def update_item():
  
  key_update = st.selectbox("chose a key to udate",df_references["key"].tolist(),label_visibility="visible")
  password_update = title = st.text_input("Write the new password")

  update = {"password":password_update}
  if st.button("Update",use_container_width=True): 
    db.update(update,key_update)
    del st.session_state.login
    del st.session_state.project
    st.rerun()


st.set_page_config(page_title='References', page_icon='🔐', initial_sidebar_state='collapsed')



#___APP____

df_references

if st.button("Do you want to update?",use_container_width=True):
  update_item()
    

