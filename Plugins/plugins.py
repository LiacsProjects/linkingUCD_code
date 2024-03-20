#
# Set environment base path
#
ON_SERVER = False
if not ON_SERVER:
    # added for local server
    # extra regel om environmental variable te bepalen
    # voor server draaien dashboard.wsgi ?
    from Plugins import add_environment_variable

#
# Imports
#
#from dash import dcc, html, Input, Output, Dash
import dash
import dash_bootstrap_components as dbc

from Plugins.Data import exceldata as data
from Plugins.Pages.Timeline import timelinegraphs as professorfigures

#
# Configurate dash application
#
if ON_SERVER:
    # SERVER
    app = dash.Dash(
        __name__,
        use_pages=True,
        suppress_callback_exceptions=True,
        title="Leiden Univercity Plugins",
        routes_pathname_prefix='/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        requests_pathname_prefix='/plugins/'
    )

else:
    # LOCAL
    app = dash.Dash(
        __name__,
        use_pages=True,
        suppress_callback_exceptions=False,
        title="Leiden Univercity Plugins",
        routes_pathname_prefix='/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

dash.register_page(
    "home",
    layout="This is a test bench for plugins for the LUCD project.",
    path="/",
    order=0
)

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="LUCD plugin test bench",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
    ],
    className="dbc",
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)

# Configure dash application for server
#server = app.server
