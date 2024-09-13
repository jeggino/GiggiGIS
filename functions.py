import streamlit as st
import pandas as pd

def popup_html(row):
    
    i = row
     
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    soortgroup=df_2['soortgroup'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soortgroup</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(soortgroup) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html

def insert_json(key,waarnemer,datum,time,soortgroup,aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates):

    return db.put({"key":key, "waarnemer":waarnemer,"datum":datum,"time":time,"soortgroup":soortgroup, "aantal":aantal,
                   "sp":sp, "gedrag":gedrag, "functie":functie, "verblijf":verblijf,
                   "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates})
        

def map():
    
    m = folium.Map()
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': False,}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    

    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    
    return  output



def input_data():

    with st.container(height=CONTAINER_height, border=True):
        
        output = map()
    
        
    submitted = popover.button("Gegevens opslaan")
    
    if submitted:           

        try:

            output["features"] = output.pop("all_drawings")
            geometry_type = output["features"][0]["geometry"]["type"]
            coordinates = output["features"][0]["geometry"]["coordinates"] 
            
            if geometry_type == "LineString":
                
                lng = None
                lat = None
                key = None
            
            else: 
                
                lng = coordinates[0]
                lat = coordinates[1]
                coordinates = None
                
                key = str(lng)+str(lat)

            if len(output["features"]) > 1:
                popover.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
                st.stop()

            else:

                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    drive.put(f"{key}.jpeg", data=bytes_data)            
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates)
                
                else:
                    insert_json(key,waarnemer,str(datum),str(time),GROUP_DICT[soortgroup],aantal,sp,gedrag,functie,verblijf,geometry_type,lat,lng,opmerking,coordinates)

                popover.success('Gegevens opgeslagen!', icon="✅")
                
                
                

        except:
            popover.info("Markeer een waarneming")
            st.stop()

        st.switch_page("main.py")


def logIn():
    name = st.text_input("Nane ...")
    password = st.text_input("Password ...")
    if st.button("logIn"):
        st.session_state.login = {"name": name, "password": password}
        st.rerun()

def project():
    project = st.selectbox("Chose a project",SOORTGROUP)
    if st.button("start"):
         st.session_state.project = {"project_name": project}
         st.rerun()

def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        del st.session_state.project     
        st.rerun()

def logOut_project():
    if st.button("logOut project",use_container_width=True):
        del st.session_state.project
        st.rerun()
