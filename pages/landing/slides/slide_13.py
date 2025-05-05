from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.vis.analysis_vis import gini_eda_tabs

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                gini_eda_tabs(),
            ], width=10),
        ], className="mt-1"),
    ]),
])