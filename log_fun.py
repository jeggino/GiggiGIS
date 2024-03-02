import streamlit as st
from credencials import dict


@st.cache_resource(experimental_allow_widgets=True)
def login():
  
  placeholder = st.empty()
  container =  placeholder.container(height=None, border=True)
  id_input = container.text_input( "Enter your user name here",value="")
  id_input_2 = container.text_input( "Enter your password here",type="password")
  
  if container.button('Login'):
      if id_input in dict.keys():
          
          if dict[id_input]['password'] == id_input_2:
              placeholder.empty()
              st.title(f"HI :blue[{dict[id_input]['name']}]")
                            
          else:
              container.write('Password incorrect')
              st.stop()
      else:
          container.write("User name incorrect")
          st.stop()
  else:
    st.stop()
