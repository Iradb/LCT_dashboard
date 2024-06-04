import os
import app.__init__
from dash import html, Input, Output, dcc, dash_table,Dash,State
import plotly.graph_objs as go
from app.database.database import session
from app.models.models import Markers
from flask import send_from_directory
from app.function.function_app import function_sidebar
from app.function.function_app import function_Scatter_lat_lon
from app.models.models import add_db
from app.schems.schem import to_pydantic,Object_take
app = Dash(__name__)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


add_db()
@app.server.route('/app/style/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'app/style')
    return send_from_directory(static_folder, path)

fig = function_Scatter_lat_lon()
# da = session.query(Markers.custom_name,Markers.custom_id).all()
# da = session.query(Markers).all()
# dict_objects = [db_object.to_dict() for db_object in da]
# print(dict_objects)
# dict_objects = [{column.name: getattr(db_object, column.name) for column in db_object.__table__.columns} for db_object in db_objects]
# print(to_pydantic(da, Object_take))
# Создаем боковую панель
# sidebar = html.Div(
#     html.Ul([
#             html.Li(i[0],className='UL_item',id=str(i[1]),value=str(i[1]))for i in session.query(Markers.custom_name,Markers.custom_id).all()
#             ],className='sidebar'), 
#             className='sidebar',
# )
query = session.query(Markers.custom_name, Markers.custom_id).all()
data = [{'custom_name': row[0], 'custom_id': row[1]} for row in query]
table = dash_table.DataTable(data=data,columns=[{"id": i,"name": i,} for i in data[0].keys()],id="datatable")

sidebar = html.Div(
    [table],className='sidebar',
)

@app.callback(
    Output('Information_about_object', 'style'),
    Input('datatable', 'active_cell'),
    State('Information_about_object', 'style'),
)
def update_style(active_cell, current_style):
    print(active_cell)
    print(current_style)
    if active_cell is not None:
        print(active_cell)
        return {'z-index': 4}  # Change the style to your desired value
    else:
        return current_style

first_layer = html.Div(   
)
# Создаем содержимое
content = html.Div(
    [
        html.Div([],className="UpSide"),
        dcc.Graph(figure=fig, id='sub_area', style={"width": "100%", "height": "90vh"}),
        html.Div([],className="Information_about_object",style={'z_index':-1})
    ],
    className='content',
    # style=styles['content']
)
# # Создаем макет страницы
# app.layout = html.Div(
#     html.Div(dcc.Location(id='url', refresh=False),html.Link(
#             rel='stylesheet',
#             href='/app/style/main.css'
#         )),[sidebar, content])

# app.layout = html.Div(html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Link( rel='stylesheet', href='/app/style/main.css' ),        
# ]), [sidebar, content])

app.layout = html.Div([
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Link(
            rel='stylesheet',
            href='/app/style/main.css'
        ),
    ]),
    html.Div(id='page-content', children=[sidebar,content]),

])

# app.layout = html.Div([sidebar,content])

app.run_server(debug=True)