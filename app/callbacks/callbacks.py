import dash
from dash import callback
from dash import html, Input, Output, dcc, dash_table,Dash,State
from dash import html,dcc
from app.query.query import take_group,take_data_TCP
from app.function.function_app import function_Scatter_lat_lon,function_Scatter_lat_lon_marker
from app.function.function_app import find_row_index
active_cell_state = State('datatable', 'active_cell')
block_open_state = State('Information_about_object', 'style')
previous_cell_state = State('previous_cell', 'data')
clicked_indices = []
# Обновляем функцию update_style
def get_callbacks(app):
#     @app.callback(
#         [Output(f'sub_area_{i["id"]}', 'style') for i in take_group()],
#         # [Output(f'sub_area_{i["id"]}', 'n_clicks') for i in take_group()],
#         [Input(f'div_{i["id"]}', 'n_clicks') for i in take_group()],
#         prevent_initial_call=True
#         # [State(f'div_{i["id"]}', 'id') for i in take_group()]
#     )
#     def click_show(*args):
#         styles = []
#         args = list(args)
#         for i, n_clicks in enumerate(args):
#             if n_clicks is not None and n_clicks % 2 == 1:
#                 styles.append({'display': 'block'})
#             else:
#                 styles.append({'display': 'none'})

#         return styles
            
        # print(clicked_index)
        # if clicked_index is not None:
            # return f'Clicked div: {clicked_index}'
        # else:
            # return 'No div clicked'
    # @app.callback(
    #     [Output('Information_about_object', 'style',allow_duplicate=True),
    #     Output('previous_cell', 'data')],
    #     [Input('datatable', 'active_cell'),
    #     State('datatable', 'active_cell'),
    #     State('Information_about_object', 'style')],
    #     [State('previous_cell', 'data')],
    #     prevent_initial_call=True
    # )
    # def update_style(active_cell, current_state, block_open, previous_cell):
    #     if active_cell is not None:
    #         if active_cell == previous_cell:
    #             if block_open is not None and block_open['display'] == "block":
    #                 return {'display': "none"}, active_cell
    #             else:
    #                 return {'display': "block"}, active_cell
    #         else:
    #             return {'display': "block"}, active_cell
    #     else:
    #         return block_open, previous_cell
    @app.callback(
        Output('Information_about_object', 'style'),
        # Output('datatable', 'active_cell'),
        Input('exit', 'n_clicks'),
        prevent_initial_call=True
    )
    def exit_form(n_clicks):
        if n_clicks is not None:
            return {'display': "none"}
    @app.callback(
            Output("sidebar","children"),
            Input('sub_area', 'clickData'),
            prevent_initial_call=True
    )
    def create_side_bar(clickData):
        if clickData:
            data = take_data_TCP(clickData['points'][0]['customdata'])
            print(data)
            sidebar_items = []
            if data and data[0].get("Адрес"):
                sidebar_items.append(html.Div([html.P("Адрес",className="title_sidebar"),html.Div(data[0]["Адрес"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))
            if data and data[0].get("Вид ТП"):
                sidebar_items.append(html.Div([html.P("ТП",className="title_sidebar"),html.Div(data[0]["Вид ТП"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))
            if data and data[0].get("UNOM"):
                sidebar_items.append(html.Div([html.P("UNOM",className="title_sidebar"),html.Div(data[0]["UNOM"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))
            if data and data[0].get("ODS_name"):
                sidebar_items.append(html.Div([html.P("№ ОДС",className="title_sidebar"),html.Div(data[0]["ODS_name"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))
            if data and data[0].get("ODS_adrs"):
                sidebar_items.append(html.Div([html.P("Адрес ОДС",className="title_sidebar"),html.Div(data[0]["ODS_adrs"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))
            if data and data[0].get("ODS_number"):
                sidebar_items.append(html.Div([html.P("Номер телефона ОДС",className="title_sidebar"),html.Div(data[0]["ODS_number"],className="sidebar_subblock"),html.Hr()],className="sidebar_new"))

            if sidebar_items:
                return html.Div(sidebar_items, className="sidebar_item")
            else:
                return html.Div("No data available")
    # query = [{"id":str(row[0]),'Адрес': row[1],'Вид ТП': row[2],'UNOM': row[3]} for row in query]
    @app.callback(
    Output('Information_about_object', 'style',allow_duplicate=True),
    # Output('datatable', 'active_cell',allow_duplicate=True),
    Input('sub_area', 'clickData'),
    prevent_initial_call=True
)
    def update_figure(click_data):
        # print(click_data)
        if click_data is not None:
            # print(click_data)
            marker_id = click_data['points'][0]['customdata']
            # print(marker_id)
            # row = find_row_index(marker_id)
            # if row is not None:
            # Set the active cell to the clicked marker's row and column
                # active_cell = {'row': row, 'column': 0}
            # Perform the desired action when a marker is clicked
            # For example, you can update the figure or display information
            # based on the clicked marker
            # ...
            return {'display': "block"}
        else: return{'display': "none"}

    @app.callback(
        Output('sub_area', 'figure',allow_duplicate=True),
        [Input('sub_area', 'relayoutData')],
        prevent_initial_call=True
    )
    def function_update(relayoutData):
        if relayoutData is None:
            relayoutData = {'mapbox.zoom':13}
        if relayoutData is not None and 'mapbox.zoom' in relayoutData:
            zoom_level = relayoutData['mapbox.zoom']
            if zoom_level > 12:
                print("function_Scatter_lat_lon_marker")
                fig = function_Scatter_lat_lon_marker()
                print(fig)
                return fig
            elif zoom_level < 12 and zoom_level > 8:
                print("function_Scatter_lat_lon")
                fig = function_Scatter_lat_lon()
                print(fig)
                return fig
            else:
                return dash.no_update