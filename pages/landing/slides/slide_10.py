from dash import html, dcc
import dash_bootstrap_components as dbc
from src.visualize.stats_analysis_vis import build_income_distribution_pyramid, income_histogram_with_quintiles

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="income-distribution-pyramid", figure=build_income_distribution_pyramid())
            ], width=6),
            dbc.Col([
                dcc.Graph(id="histogram_quintile_vrec", figure=income_histogram_with_quintiles()),
                html.H2("Income Distribution Pyramid and Sample Distribution Histogram", className="mt-3"),
                html.P("The Result of our Boostrap Resampling is a income Distribution for every year based on three main parameters."),
                html.Li("The Palma Ratio"),
                html.Li("The Housing Affordability Gap"),
                html.Li("The Productivity Pay Gap")
            ], width=6),
        ], className="mt-3"),
    ])
])