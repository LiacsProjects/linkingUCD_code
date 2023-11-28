# import modules
from dash import html
import dash


dash.register_page(__name__, path='/subject_information')

# ******************************************************************************************  START

# app.layout = html.Div([
#     dash.page_container
# ])
layout = html.Div(children=[
    html.H1(children='This is our Subject Information page'),

    html.Div(children='''
        This is our Subject Information page content.
    '''),
    ])