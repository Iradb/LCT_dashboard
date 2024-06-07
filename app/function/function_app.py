from app.database.database import Session
from app.models.models import Markers
from dash import dash_table
import plotly.graph_objs as go
def function_Scatter_lat_lon():
    session = Session()
    all_matp = session.query(Markers.custom_id, Markers.lat, Markers.lon).all()
    custom_name_all = []
    lat_all = [] 
    lon_all = []
    for i in all_matp:
        lat_all.append(i[1]) 
        lon_all.append(i[2])
        custom_name_all.append(i[0])
    fig = go.Figure(go.Scattermapbox(lat=lat_all, lon=lon_all,customdata=custom_name_all,marker=dict(size=10,color='red')))
    fig.update_layout(mapbox_zoom=15,
        mapbox_style='carto-positron',
        margin=dict(t=10, b=10, l=10, r=10),
        mapbox_center={'lat': 59.935567, 'lon': 30.338619})
    session.close()
    return fig

def function_sidebar():
    session = Session()
    query = session.query(Markers.custom_name, Markers.custom_id).all()
    data = [{'custom_name': row[0]} for row in query]
    table = dash_table.DataTable(data=data,
                                 columns=[{"id": i,"name": i,} for i in data[0].keys()],
                                 style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': '#ff992c',
                                'textAlign': 'center',
                                'fontSize': '15px',
                                },
                                style_data={
                                    'backgroundColor': '#424242',
                                    'color': '#ff992c',
                                    'textAlign': 'center',
                                    'fontSize': '15px',
                                },
                                style_table={
                                'height': '70vh',
                                'overflowY': 'auto'
    },
                                id="datatable",
                                )
    session.close()
    return table

def find_row_index(custom_name):
    session = Session()
    query = session.query(Markers.custom_id).where(Markers.custom_id == custom_name).all()
    data = [row[0] for row in query]
    print(data)
    session.close()
    if data != []:
        return data[0]

    return None
