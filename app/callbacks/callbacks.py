from dash import callback
from dash import html, Input, Output, dcc, dash_table,Dash,State
from dash import html,dcc
active_cell_state = State('datatable', 'active_cell')
block_open_state = State('Information_about_object', 'style')
previous_cell_state = State('previous_cell', 'data')

# Обновляем функцию update_style
def get_callbacks(app):
    @app.callback(
        [Output('Information_about_object', 'style',allow_duplicate=True),
        Output('previous_cell', 'data')],
        [Input('datatable', 'active_cell'),
        active_cell_state,
        block_open_state],
        [previous_cell_state],
        prevent_initial_call=True
    )
    def update_style(active_cell, current_state, block_open, previous_cell):
        if active_cell is not None:
            if active_cell == previous_cell:
                if block_open is not None and block_open['display'] == "block":
                    return {'display': "none"}, active_cell
                else:
                    return {'display': "block"}, active_cell
            else:
                return {'display': "block"}, active_cell
        else:
            return block_open, previous_cell
    @app.callback(
        Output('Information_about_object', 'style'),
        Output('datatable', 'active_cell'),
        Input('exit', 'n_clicks'),
        prevent_initial_call=True
    )
    def exit_form(n_clicks):
        if n_clicks is not None:
            return {'display': "none"},None
