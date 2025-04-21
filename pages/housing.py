from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os
from pages.vis.housing_vis import housing_sankey, income_affordability_sankey, housing_vs_budget_trend


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', 'data', 'csv')

csv_path = os.path.join(csv_dir, 'analysis.csv')
df = pd.read_csv(csv_path)

df = df[df['Year'].str.endswith('-07')]
years = sorted(df['Year'].str[:4].astype(int).unique())

# Layout for the housing page
layout = dbc.Container([
    html.H3("Housing Cost Sankey Diagram"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sankey-graph')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='year-slider',
                min=years[0],
                max=years[-1],
                step=1,
                value=2023,
                marks={str(year): str(year) for year in years[::5]},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='income-sankey-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='housing-budget-trend',
                figure=housing_vs_budget_trend()
            )
        ], width=6)
    ]),
], fluid=True)

# Callback to update the Sankey graph based on selected year
@callback(
    Output('sankey-graph', 'figure'),
    Input('year-slider', 'value')
)
def update_graph(selected_year):
    return housing_sankey(selected_year)

@callback(
    Output('income-sankey-graph', 'figure'),
    Input('year-slider', 'value')
)
def update_income_graph(selected_year):
    from pages.vis.housing_vis import income_affordability_sankey
    return income_affordability_sankey(selected_year)

exprort_layout = layout
