import streamlit as st
import datetime

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)

reduce_header_height_style = """
<style>
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; margin-top: 1em; margin-bottom: 2em;}
</style>
"""

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #FFFFFF;">
  <a class="navbar-brand" target="_blank">   </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
</nav>
""", unsafe_allow_html=True)

IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, icon_image=None)

st.subheader(" :blue[EXAMPLE] :sunglasses:")
DOEL = ["Groepsvorming laatvlieger","Kraamperiode (avond)","Kraamperiode (ochtend)","Winterverblijfplaatsen","Paarverblijfplaatsen (Gewonedwerge vleermuis)","Paarverblijfplaatsen (Meervleermuis)", "Kolonie tellen"]

GEBIED = ['P', 'O', 'Q', 'B', 'R', 'M', 'N', 'L']

WAARNEMERS = ['Luigi', 'Alko', 'Tobias', 'Sanders','Mats']

datum = st.date_input("Datum", datetime.datetime.today())
gebied = st.selectbox('Gebied',GEBIED,key='area',placeholder="Kies een gebied...",index=None)
doel = st.selectbox('Doel',DOEL,key='doel',placeholder="Kies een doel...",index=None)
waarnemer = st.multiselect('Waarnemer(s)',WAARNEMERS,key='waarnemer',placeholder="Kies voor een waarnemer...")

submitted = st.button("Gegevens invoegen")
