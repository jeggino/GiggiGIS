import folium
import streamlit as st

from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium
# from streamlit_js_eval import get_geolocation

import pandas as pd
import geopandas as gpd

import datetime

from deta import Deta


st.set_page_config(
    page_title="GiggiGIS",
    page_icon="🍕",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'mail':"jeggino@gmail.com"
#         'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
# Create a new database "example-db"
db_3 = deta.Base("GiggiGIS_data")
drive = deta.Drive("GiggiGIS_pictures")

# loc = get_geolocation()
# lat = loc['coords']['latitude']
# lon = loc['coords']['longitude']

# # ---CUSTUMIZE---

# st.markdown("""
#     <style>
#       section[data-testid="stSidebar"][aria-expanded="true"]{
#         width: 100% !important;
#       }
#       section[data-testid="stSidebar"][aria-expanded="false"]{
#         width: 100% !important;
#       }
#     </style>""", unsafe_allow_html=True)

# -------------- FUNCTIONS --------------


def insert_json(json):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db_3.put({"json":json})

# with st.sidebar:
#     add_radio = st.radio("", horizontal=False, options = ["📝", "🗺️"], label_visibility="collapsed")

# if add_radio == "📝":      
                
m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
Fullscreen().add_to(m)
# Geocoder(collapsed=True, position='topright', add_marker=True).add_to(m)
LocateControl(auto_start=False).add_to(m)

with st.container():
    output = st_folium(m, width=1200, height=500, returned_objects=["all_drawings"])
        
# with st.form("entry_form", clear_on_submit=True):
    
with st.sidebar:

    try:
        new_dict = output
        new_dict["features"] = new_dict.pop("all_drawings")
    except:
        st.info("mark an observation")
        st.stop()

    if len(new_dict["features"]) > 1:
        st.error("You cannot upload more than one survey at time!")
        st.stop()

    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("Date")
        sp = st.selectbox("Species", ["Anax imperator", "Ischnura elegans", "Lestes sponsa"])
        n = st.number_input("Number of specimens:", min_value=0)
        comment = st.text_input("", placeholder="Enter a comment here ...")
        with st.expander("Upload a picture"):
            uploaded_file = st.camera_input("")


        new_dict["features"][0]["properties"]["date"] = str(date)
        new_dict["features"][0]["properties"]["sp"] = sp
        new_dict["features"][0]["properties"]["n"] = n
        new_dict["features"][0]["properties"]["comment"] = comment

        submitted = st.form_submit_button("Save Data")
        if submitted:
            # If user attempts to upload a file.
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                image_name = uploaded_file.name

                drive.put(image_name, data=bytes_data)            
                new_dict["features"][0]["properties"]["image_name"] = image_name
                insert_json(new_dict)
            else:
                new_dict["features"][0]["properties"]["image_name"] = None
                insert_json(new_dict)
                
            st.success('Data saved!', icon="✅")
                



    
            
# elif add_radio == "🗺️":
    
#     with st.sidebar:
#         option = st.selectbox('',('Cloud', 'Load dataset'))

    
#     if option == 'Cloud':
        
#         c1, c2 = st.columns([3,2])
    
#         with c1:
#             db_content = db_3.fetch().items
#             df_point = pd.DataFrame(db_content)

#             map = folium.Map(location=[52.370898, 4.898065], zoom_start=8)
#             for i in df_point["json"].to_list():
#                 folium.GeoJson(i,
#                               tooltip=folium.GeoJsonTooltip(fields= ["date", "sp", "n", "comment"],
#                                                             aliases=["Date: ", "Species: ", "Nember of specimens: ", "Comment: "],
#                                                             labels=True,
#                                                             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
#                                                           )
#                               ).add_to(map)
#             output_2 = st_folium(map, width=500, height=700)

#         with c2:
#             try:
#                 name = output_2["last_active_drawing"]["properties"]["image_name"]
#                 comment = output_2["last_active_drawing"]["properties"]["comment"]
#                 with st.container():
#                     image = drive.get(name).read()
#                     st.image(image, caption=comment, use_column_width='always')
#             except:
#                 st.info("No image")

                
#     elif option == 'Load dataset':
                
#         try:
            
#             with st.sidebar:
#                 uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
#                 df = pd.read_csv(uploaded_file)
#                 city = st.multiselect("", df["stad"].unique(), default=None,label_visibility="collapsed")
#                 nlnaam = st.multiselect("", df["nlnaam"].unique(), default=None,label_visibility="collapsed")
#                 functie = st.multiselect("", df["functie"].unique(), default=None,label_visibility="collapsed")
                
                
                
                
#             filter = df[(df["stad"].isin(city)) & (df["nlnaam"].isin(nlnaam)) & (df["functie"].isin(functie))]
#             gdf = gpd.GeoDataFrame(filter, geometry=gpd.points_from_xy(filter.lon,filter.lat))

#             map = folium.Map(location=[filter.lat.mean(),filter.lon.mean()], zoom_start=8)
#             folium.GeoJson(gdf.to_json(),
# #                               tooltip=folium.GeoJsonTooltip(fields= ["Data", "Profondità", "magnitudo_score"],
# #                                                             aliases=["Date: ", "Deepness: ", "Magnitudo: "],
# #                                                             labels=True,
# #                                                             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 20px;")
# #                                                           )
#                           ).add_to(map)

#             output = st_folium(map, width=1200)
                
#             st.sidebar.write(output)

#         except:
#             st.stop()

            
        
        
   

