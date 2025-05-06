from dash import html, dcc
import dash_bootstrap_components as dbc
from src.visualize.stats_analysis_vis import create_gini_trend_plot
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dcc.Graph(id="gini-trend", figure=create_gini_trend_plot())
            ], width=10),
        ], className="mt-1"),
    ]),

    get_button(
        label="Learn More about this Method",
        link="/methods/gini",
        color="#693382",
        size=(300, 50)
    )
])