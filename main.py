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

@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

