from dash import html, dcc
from components.topbar import get_topbar

layout = html.Div(className="section-slide", children=[
    html.H2("We had one question"),
    html.H3("Does an average consumer today can afford to buy more than one in 1920s?")
])