from dash import html, dcc
from components.topbar import get_topbar

layout = html.Div(className="section-slide", children=[
    html.H2("So we collected some data"),
    html.H3("1. The average price of goods from 1900 - 2020"),
    html.H3("2. The average incomes from 1900 - 2020")
])