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
def vote():
    
    name = st.text_input("Nane ...")
    password = st.text_input("Password ...")
    if st.button("Submit"):
        st.session_state.vote = {"name": name, "password": password}
        st.rerun()

if "vote" not in st.session_state:
    st.write("LogIn please")
    vote()

if st.session_state.vote['name'] == st.secrets['password']:
    f"Hello {st.session_state.vote['name']}"
else:
    f"Sorry {st.session_state.vote['name']}} your password is not correct"
    

