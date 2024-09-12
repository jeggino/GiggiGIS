import streamlit as st
from deta import Deta
import pandas as pd


st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')

ASSAYS = ['birds','bats','insects','rats']
WAARNEMERS = ["Luigi","Daan"]
 
import streamlit as st

def logIn():
    name = st.text_input("Nane ...")
    password = st.text_input("Password ...")
    if st.button("logIn"):
        st.session_state.login = {"name": name, "password": password}
        st.rerun()

def project():
 project = st.selectbox("Chose a project",ASSAYS)
 if st.button("start"):
  st.session_state.project = {"project_name": project}
  st.rerun()

def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        st.rerun()

def logOut_project():
    if st.button("logOut project",use_container_width=True):
        del st.session_state.project
        st.rerun()

        
    
    


# ___APP___
if "login" not in st.session_state:
    st.write("LogIn please")
    logIn()
    st.stop()

if st.session_state.login['password'] != st.secrets['password']:
    f"Sorry {st.session_state.login['name']} your password is not correct"
    logIn()
    st.stop()

if 'project' not in st.session_state:  
 st.write("Chose a project")
 project()
 st.stop()

with st.sidebar:
 f"Hello {st.session_state.login['name']} you will work at {st.session_state.project['project_name']} project"
 logOut_project()
 logOut()



deta = Deta(st.secrets["deta_key_other"])
db = deta.Base("df_observations")
drive = deta.Drive("df_pictures")


# --- FUNCTIONS ---
def load_dataset():
    return db.fetch().items    
    
db_content = load_dataset()
df_point = pd.DataFrame(db_content)

if st.button("Say hello"):
 st.write("Why hello there")
df_point
waarnemer = st.sidebar.selectbox("Chose an operator",WAARNEMERS)
df_point[df_point['waarnemer']==waarnemer]


 
   
    

