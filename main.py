import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users


st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')


# # try:
# users = fetch_users()
# emails = []
# usernames = []
# passwords = []

# for user in users:
#     emails.append(user['key'])
#     usernames.append(user['username'])
#     passwords.append(user['password'])

# credentials = {'usernames': {}}
# for index in range(len(emails)):
#     credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

# credentials 

import streamlit as st

# @st.dialog("Cast your vote")
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

if "login" not in st.session_state:
    st.write("LogIn please")
    logIn()
    st.stop()

if st.session_state.login['password'] == st.secrets['password']:
    f"Hello {st.session_state.login['name']}"
    logOut()
else:
    f"Sorry {st.session_state.login['name']} your password is not correct"
    logIn()
    st.stop()
    

