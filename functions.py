import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from datetime import datetime, timedelta, date

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

from credentials import *
import ast

#---DATASET---
ttl = 0
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="ratten-terschelling")
df_references = conn.read(ttl=ttl_references,worksheet="users-ratten_terschelling-input")


# --- FUNCTIONS ---
def popup_html(row,df_2):
    
    i = row

    datum=df_2['datum'].iloc[i] 
    datum_2=df_2['datum_2'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
    aantal=df_2['aantal'].iloc[i]
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum verwijderd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum_2) + """
    </tr>
    <tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal geschoten </span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
    </tr>

    </tbody>
    </table>
    </html>
    """
    return html


