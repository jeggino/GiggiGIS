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

with st.sidebar:
    username = st.text_input("Username")
    password = st.text_input("Password",type='password')

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






# if not authentication_status:
#     sign_up()

# if username:
#     if username in usernames:
#         if authentication_status:
#             # let User see app
#             st.sidebar.subheader(f'Welcome {username}')
#             Authenticator.logout('Log Out', 'sidebar')

#             st.subheader('This is the home page')
#             st.markdown(
#                 """
#                 ---
#                 Created with ❤️ by SnakeByte
                
#                 """
#             )

#         elif not authentication_status:
#             with info:
#                 st.error('Incorrect Password or username')
#         else:
#             with info:
#                 st.warning('Please feed in your credentials')
#     else:
#         with info:
#             st.warning('Username does not exist, Please Sign up')


# # except:
# #     st.success('Refresh Page')
