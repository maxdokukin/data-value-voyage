from dash import html, dcc
import dash_bootstrap_components as dbc
from src.visualize.stats_analysis_vis import multiyear_lorenz_curve

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[ 
        dbc.Row([
            dbc.Col([],width=1),
            dbc.Col([
                dcc.Graph(id="multiyear-lorenz-curve", figure=multiyear_lorenz_curve())
            ], width = 10),
        ], className="mt-1"),
    ])
])