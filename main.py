import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users


st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')


# try:
users = fetch_users()
emails = []
usernames = []
passwords = []

for user in users:
    emails.append(user['key'])
    usernames.append(user['username'])
    passwords.append(user['password'])

credentials = {'usernames': {}}
for index in range(len(emails)):
    credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

credentials 


import streamlit as st

@st.cache_resource(experimental_allow_widgets=True)
def logIn(name,password):
    

    if password == st.secret["password"]:
       return True, name
    
    else:
        return False

# _____APP_____
name = st.text_input("Insert your name", "")
password = st.text_input("Insert yput password", "")



if logIn(name,password) == False:
    st.error(f"password incorrect, {name}")
    st.stop()

st.write(f"Welkom {name}")

@st.cache_resource()
def logOut():
    st.cache_resource.clear()
    st.rerun()





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
