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

def logIn():
    name = st.selectbox("Wie ben je?",df_references["username"].tolist())
    
    password = st.text_input("Vul het wachtwoord in, alstublieft")
    index = df_references[df_references['username']==name].index[0]
    true_password = df.loc[index,"project"]
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.write("the password is not correct")


# ___APP___
if "login" not in st.session_state:
    logIn()
    st.stop()

st.write("It's fine!!")
