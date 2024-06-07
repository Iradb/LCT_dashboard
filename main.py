import os
import app.__init__
from dash import html, Input, Output, dcc, dash_table,Dash,State
import plotly.graph_objs as go
from app.database.database import Base,engine
from app.models.models import Markers
from flask import send_from_directory
from app.function.function_app import function_sidebar
from app.function.function_app import function_Scatter_lat_lon
from app.models.models import add_db
from app.schems.schem import to_pydantic,Object_take
from app.callbacks.callbacks import get_callbacks
import dash_auth
app = Dash(__name__)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# VALID_USERNAME_PASSWORD_PAIRS = {
#     'admin': 'admin'
# }

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )
Base.metadata.create_all(engine)
# add_db()
@app.server.route('/assests/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assests')
    return send_from_directory(static_folder, path)

fig = function_Scatter_lat_lon()

sidebar = html.Div(
    [function_sidebar()],className='sidebar',
)

first_layer = html.Div(   
)
# Создаем содержимое
content = html.Div(
    [
        html.Div([html.Div(html.A(href="/", children="Карта"),className="Cart"),
                  html.Div(html.A(href="/", children="Дашборд"),className="Cart"),
                  html.Div(html.A(href="/", children="Что-то"),className="Cart")],className="UpSide",id="UpSide"),
        dcc.Graph(figure=fig, id='sub_area',className="sub_area", style={"width": "100%", "height": "90vh"}),
        html.Div([html.Button(["X"],className="exit",id="exit")],style={'display':'none'},className="Information_about_object",id="Information_about_object")
    ],
    className='content',
)

app.layout = html.Div([
    html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='previous_cell', storage_type='memory'),
        html.Link(
            rel='stylesheet',
            href='/assests/css/main_01.css'
        ),
    ]),
    html.Div(id='page-content',className="page_main", children=[sidebar,content]),

])

# app.layout = html.Div([sidebar,content])
get_callbacks(app)
if __name__ == '__main__':
    # app.callback()
    app.run_server(port=os.getenv("PORT_DASH"),debug=True)