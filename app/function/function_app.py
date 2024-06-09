from app.database.database import Session
from app.models.models import Markers,TP
from dash import dash_table
import plotly.graph_objs as go
def function_Scatter_lat_lon():
    session = Session()
    all_matp = session.query(TP.id, TP.geoData_full,TP.Adres_TP_Full).all()
    name=[]
    custom_name_all = []
    lat_all = [] 
    lon_all = []
    for i in all_matp:
        lat_all.append(i[1][1]) 
        lon_all.append(i[1][0])
        name.append(i[2])
        custom_name_all.append(i[0])
    fig = go.Figure(go.Scattermapbox(lat=lat_all, lon=lon_all,customdata=custom_name_all,text=name,marker=dict(size=10,color='red')))
    fig.update_layout(mapbox_zoom=15,
        mapbox_style='carto-positron',
        margin=dict(t=10, b=10, l=10, r=10),
        mapbox_center={'lat': 55.755864, 'lon': 37.617698})
    fig.update_traces(cluster=dict(enabled=True))
    session.close()
    return fig

import plotly.graph_objects as go

# def function_Scatter_lat_lon():
#     session = Session()
#     all_matp = session.query(TP.id, TP.geoData_full).all()
#     custom_name_all = []
#     lat_all = []
#     lon_all = []
#     for i in all_matp:
#         lat_all.append(i[1][1])
#         lon_all.append(i[1][0])
#         custom_name_all.append(i[0])

#     fig = go.Figure(
#         go.Scattergeo(
#             lat=lat_all,
#             lon=lon_all,
#             customdata=custom_name_all,
#             mode='markers',
#             marker=dict(
#                 size=10,
#                 color='red'
#             ),
#             hoverinfo='text',
#             text=custom_name_all,
#             visible=False
#         )
#     )

#     fig.update_layout(
#         geo=dict(
#             resolution=50,
#             showframe=False,
#             showcoastlines=False,
#             landcolor='rgb(204, 204, 204)',
#             countrycolor='rgb(204, 204, 204)',
#             lataxis=dict(range=[min(lat_all), max(lat_all)]),
#             lonaxis=dict(range=[min(lon_all), max(lon_all)])
#         ),
#         margin=dict(t=10, b=10, l=10, r=10),
#         annotations=[
#             dict(
#                 showarrow=False,
#                 text="Number of points: {}".format(len(lat_all)),
#                 xref="paper",
#                 yref="paper",
#                 x=0.5,
#                 y=0.5,
#                 font=dict(
#                     size=16,
#                     color="blue"
#                 )
#             )
#         ]
#     )

#     fig.update_traces(
#         hovertemplate="ID: %{customdata}<br>Latitude: %{lat}<br>Longitude: %{lon}",
#         hoverinfo='text',
#         visible=True
#     )

    # fig.data[0].visible = [True if i > 10 else False for i in range(len(lat_all))]
    # print(fig.data)

    # def update_points(visible):
    #     for i, trace in enumerate(fig.data):
    #         trace.visible = visible

    # fig.add_traces([go.Scattergeo(
    #     lat=[],
    #     lon=[],
    #     mode='markers',
    #     marker=dict(
    #         size=10,
    #         color='red'
    #     ),
    #     visible=False
    # )])

    # fig.data[-1].visible = False

    # fig.update_layout(
    #     updatemenus=[
    #         dict(
    #             buttons=list([
    #                 dict(
    #                     args=[{'visible': [True if i < 10 else False for i in range(len(lat_all))]}]
    #                 ),
    #                 dict(
    #                     args=[{'visible': [True if i >= 10 else False for i in range(len(lat_all))]}]
    #                 )
    #             ]),
    #             direction='down',
    #             pad={'r': 10, 't': 10},
    #             showactive=True,
    #             x=0.5,
    #             xanchor='center',
    #             y=1.1,
    #             yanchor='top'
    #         )
    #     ]
    # )

    # session.close()
    # return fig

def function_sidebar():
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
