#
# Dash example taken from:
#   https://dash.plotly.com/layout
# 

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# This configuration is necessary because the application is served
# as /test/, but Apache stripts the /test/ prefix from the URL before
# passing it to the Web app.
app = Dash(__name__,
           routes_pathname_prefix='/',
           requests_pathname_prefix='/test/')
server = app.server


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
