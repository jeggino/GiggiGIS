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

from streamlit import session_state

username = st.text_input("Username",key = "username")
password = st.text_input("Password",type='password',key = "password")

if st.button("Login"):
     
    if password == st.secrets['password']:
        session_state.login = True
        session_state.username = username
    else:
        st.warning("Incorrect username or password")

# Check login state 
if session_state.login == True:
    st.write("Hello {}!".format(session_state.username))
    
else:
    st.write("ciao!")
    st.stop()

