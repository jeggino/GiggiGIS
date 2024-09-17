import streamlit as st
from deta import Deta
import pandas as pd




st.set_page_config(page_title='References', page_icon='🔐', initial_sidebar_state='collapsed')

DICTIONARY_PROJECTS = {"Overing":["Vogels","Vleermuizen","Vleermuiskast"],
                      "A-001":["Camera","Rat val"],
                      "ALL":["Vogels","Vleermuizen","Vleermuiskast","Camera","Rat val"]}

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
    true_password = df_references.loc[index,"password"]
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.write("the password is not correct")

def project():
    index_project = df_references[df_references['username']==session_state.login["name"].index[0]
    project_list = df_references.loc[index,"project"]
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


# ___APP___
if "login" not in st.session_state:
    logIn()
    st.stop()

if 'project' not in st.session_state:  
    project()
    st.stop()
    
st.markdown(f"""
Hi **{session_state.login.name}**, 
you are working at the **{st.session_state.project.project_name}** with the assignment **{st.session_state.project.opdracht}**
""")
