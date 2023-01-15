import folium
import streamlit as st

from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd

import datetime

from deta import Deta

st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🗺️",
    layout="wide"
)


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
# Create a new database "example-db"
db_3 = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")

# -------------- FUNCTIONS --------------

  with st.sidebar:
  
    option = st.selectbox('',('Cloud', 'Load dataset'))


    if option == 'Cloud':

         c1, c2 = st.columns([3,2])

         with c1:
             db_content = db_3.fetch().items
             df_point = pd.DataFrame(db_content)

             map = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
             for i in df_point["json"].to_list():
                 folium.GeoJson(i,
                               tooltip=folium.GeoJsonTooltip(fields= ["date", "sp", "n", "comment"],
                                                             aliases=["Date: ", "Species: ", "Nember of specimens: ", "Comment: "],
                                                             labels=True,
                                                             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
                                                           )
                               ).add_to(map)
             output_2 = st_folium(map, width=500, height=700)
         with c2:
             try:
                 name = output_2["last_active_drawing"]["properties"]["image_name"]
                 comment = output_2["last_active_drawing"]["properties"]["comment"]
                 with st.container():
                     image = drive.get(name).read()
                     st.image(image, caption=comment, use_column_width='always')
             except:
                 st.info("No image")

     elif option == 'Load dataset':

         try:

             with st.sidebar:
                 uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
                 df = pd.read_csv(uploaded_file)
                 city = st.multiselect("", df["stad"].unique(), default=None,label_visibility="collapsed")
                 nlnaam = st.multiselect("", df["nlnaam"].unique(), default=None,label_visibility="collapsed")
                 functie = st.multiselect("", df["functie"].unique(), default=None,label_visibility="collapsed")



             filter = df[(df["stad"].isin(city)) & (df["nlnaam"].isin(nlnaam)) & (df["functie"].isin(functie))]
             gdf = gpd.GeoDataFrame(filter, geometry=gpd.points_from_xy(filter.lon,filter.lat))

             map = folium.Map(location=[filter.lat.mean(),filter.lon.mean()], zoom_start=8)
             folium.GeoJson(gdf.to_json(),
#                            tooltip=folium.GeoJsonTooltip(fields= ["Data", "Profondità", "magnitudo_score"],
#                                                             aliases=["Date: ", "Deepness: ", "Magnitudo: "],
#                                                             labels=True,
#                                                             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
#                                                           )
                           ).add_to(map)

             output = st_folium(map, width=1200)

             st.sidebar.write(output)

         except:
             st.stop()

