from dash import html, dcc
import dash_bootstrap_components as dbc
from src.visualize.housing_vis import housing_vs_budget_trend
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dcc.Graph(id="housing-budget-trend", figure=housing_vs_budget_trend())
            ], width=10),
        ], className="mt-1"),
    ]),

    get_button(
        label="Learn More about this Method",
        link="/methods/housing",
        color="#693382",
        size=(300, 50)
    )
])