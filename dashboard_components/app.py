# ****************************************************************************************** LOCAL
# added for local server
import Add_environment_variable
# extra regel om environmental variable te bepalen
# ******************************************************************************************  end local
# import modules
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import dash

# ******************************************************************************************  LOCAL
# Configurate dash application voor DASH
app = Dash(__name__, suppress_callback_exceptions=True,
           routes_pathname_prefix='/',
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True,
           )

# ****************************************************************************************** SERVER
# Configurate dash application voor server
# server = app.server

# ******************************************************************************************  START

app.layout = html.Div([
    dash.page_container
])

app.layout = html.Div([
    # html.H1('Multi-page app with Dash Pages'),
    # html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),

    dash.page_container
])

# ******************************************************************************************  LOCAL
if __name__ == '__main__':
    app.run_server(port=8051, debug=False)
    #
# ******************************************************************************************  SERVER
# if __name__ == '__main__':
#    app.run_server(debug=False)
#
# ******************************************************************************************  END
