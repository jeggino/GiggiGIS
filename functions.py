import streamlit as st
import pandas as pd



# --- FUNCTIONS ---
def popup_html(row,df_2):
    
    i = row

    datum=df_2['datum'].iloc[i] 
    datum_2=df_2['datum_2'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
    try:
        aantal=int(df_2['aantal'].iloc[i])
    except:
        aantal=df_2['aantal'].iloc[i]
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"

    if functie == 'Rat geschoten':
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
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal geschoten </span></td>
        <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
        <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
        </tr>
    
        </tbody>
        </table>
        </html>
        """
    else:    
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
    
        </tbody>
        </table>
        </html>
        """
    return html


