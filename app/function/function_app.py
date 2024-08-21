from app.database.database import Session
from app.models.models import Markers,TP
from dash import dash_table
import plotly.graph_objs as go
from app.query.query import Take_geoodata_Municipal
colors_TP = {"ЦТП":"red","ИТП":"blue","СТП":"green"}
def function_Scatter_lat_lon_marker()->go.Figure:
    """
    Вывод координат на объектах
    """
    session = Session()
    all_matp = session.query(TP.id, TP.geoData_full,TP.Adres_TP_Full,TP.Kind_TP).all()
    name=[]
    custom_name_all = []
    lat_all = [] 
    lon_all = []
    color = []
    for i in all_matp:
        try:
            lat_all.append(i[1][1]) 
            lon_all.append(i[1][0])
            name.append(i[2])
            custom_name_all.append(i[0])
            color.append(colors_TP[i[3]])
        except:
            pass
    fig = go.Figure(go.Scattermapbox(lat=lat_all, lon=lon_all,customdata=custom_name_all,text=name,mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color=color,
            opacity=0.7
        ),))
    
    fig.update_layout(mapbox_zoom=15,
        mapbox_style='carto-positron',
        margin=dict(t=10, b=10, l=10, r=10),
        mapbox_center={'lat': 55.755864, 'lon': 37.617698},
        annotations=[{"bgcolor": "red","text":"ЦТП","x":0.98,"y":0.95,"showarrow":False,"font":{"color":"white"}},
                     {"bgcolor": "blue","text":"ИТП","x":0.98,"y":0.92,"showarrow":False,"font":{"color":"white"}}],
        )
    # fig.update_traces(cluster=dict(enabled=True))
    session.close()
    return fig
def function_Scatter_lat_lon()->go.Figure:
    """
    Вывод координат объектов на карте и границ районов
    """
    # all_matp = session.query(TP.id, TP.geoData_full,TP.Adres_TP_Full,TP.Kind_TP).all()
    session = Session()
    all_matp = session.query(TP.id, TP.geoData_full,TP.Adres_TP_Full,TP.Kind_TP).all()
    name=[]
    custom_name_all = []
    lat_all = [] 
    lon_all = []
    color = []
    for i in all_matp:
        try:
            lat_all.append(i[1][1]) 
            lon_all.append(i[1][0])
            name.append(i[2])
            custom_name_all.append(i[0])
            color.append(colors_TP[i[3]])
        except:
            pass
    data = Take_geoodata_Municipal()
    fig = go.Figure(
        data=[
            go.Scattermapbox(
                lat=[coord[1] for coord in row['geocoords'].exterior.coords],
                lon=[coord[0] for coord in row['geocoords'].exterior.coords],
                # name=row['Муницип.Район'],
                mode="lines",
                fill="toself",
                fillcolor="rgba(255, 127, 127, 0.09)",
                line_color="red",
                hoverinfo='skip',
            )
            for row in data
        ] + [
            go.Scattermapbox(lat=lat_all, lon=lon_all,customdata=custom_name_all,text=name,mode='markers',hoverinfo='text',
        marker=go.scattermapbox.Marker(
            size=8,
            color=color,
            opacity=0.7
        ),)
        ] + [
            go.Scattermapbox(
                lat=[sum([coord[1] for coord in row['geocoords'].exterior.coords])/len([coord[1] for coord in row['geocoords'].exterior.coords])],
                lon=[sum([coord[0] for coord in row['geocoords'].exterior.coords])/len([coord[0] for coord in row['geocoords'].exterior.coords])],
                # name=row['Муницип.Район'],
                mode='markers+text',
                fill="toself",
                marker=dict(size=14),
                text=row["Муницип.Район"],
                textposition="top center",
                textfont=dict(size=14, color='black'),
                hoverinfo='text',
                unselected=dict(marker=dict(opacity=0.3)),
            )
            for row in data
        ]
    )
    fig.update_layout(mapbox_zoom=15,
        mapbox_style='carto-positron',
        mapbox_center={'lat': 55.755864, 'lon': 37.617698},
        showlegend=False,
        annotations=[{"bgcolor": "red","text":"ЦТП","x":0.98,"y":0.95,"showarrow":False,"font":{"color":"white"}},
                     {"bgcolor": "blue","text":"ИТП","x":0.98,"y":0.92,"showarrow":False,"font":{"color":"white"}}],
        )
    # fig.update_traces(cluster=dict(enabled=True))
    # session.close()
    return fig

def function_sidebar()->dash_table.DataTable:
    """
    Боковая панель с отображенеим информации о ЦТП,ИТП
    """
    session = Session()
    query = session.query(TP.Adres_TP, TP.id).all()
    try:
        data = [{'Адрес': row[0]} for row in query]
        columns = [{"id": i,"name": i,} for i in data[0].keys()]
        # columns = [{"id":"0","name":"Адрес"}]
    except Exception as e:
        print(e)
        columns = []
        data = []
    session.close()
    table = dash_table.DataTable(data=data,
                                 columns=columns,
                                 style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': '#ff992c',
                                'textAlign': 'left',
                                'fontSize': '15px',
                                },
                                style_data={
                                    'backgroundColor': '#424242',
                                    'color': '#ff992c',
                                    'textAlign': 'left',
                                    'fontSize': '15px',
                                },
                                style_table={
                                'height': '70vh',
                                'overflowY': 'auto'
    },
                                id="datatable",
                                )
    return table

def find_row_index(custom_name):
    session = Session()
    query = session.query(Markers.custom_id).where(Markers.custom_id == custom_name).all()
    data = [row[0] for row in query]
    session.close()
    if data != []:
        return data[0]

    return None

