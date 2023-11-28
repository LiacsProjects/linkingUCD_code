# import modules
from dash import html
import dash


dash.register_page(__name__, path='/individual_information')

# ******************************************************************************************  START

# app.layout = html.Div([
#     dash.page_container
# ])
layout = html.Div(children=[
    html.H1(children='This is our Individual Information page'),

    html.Div(children='''
        This is our Individual Information page content.
    '''),
    ])