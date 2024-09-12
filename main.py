import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users


st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')

ASSAYS = ['birds','bats','insects','rats']
 
import streamlit as st

def logIn():
    name = st.text_input("Nane ...")
    password = st.text_input("Password ...")
    if st.button("logIn"):
        st.session_state.login = {"name": name, "password": password}
        st.rerun()

def logOut():
    if st.button("logOut"):
        del st.session_state.login
        st.rerun()

def project():
 project = st.selectbox("Chose a project",ASSAYS,key='project')
 if st.button("start"):
  f"Hello {st.session_state.login['name']} you will work at {st.session_state.project} project"
        
    
    


# ___APP___
if "login" not in st.session_state:
    st.write("LogIn please")
    logIn()
    st.stop()

if st.session_state.login['password'] != st.secrets['password']:
    f"Sorry {st.session_state.login['name']} your password is not correct"
    logIn()
    st.stop()

    

def project():
logOut()
if st.button("Say hello"):
    st.write("Why hello there")
    

    

