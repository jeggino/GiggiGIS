import streamlit as st

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
