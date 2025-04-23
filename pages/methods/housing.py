from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os
from pages.vis.housing_vis import housing_sankey, income_affordability_sankey, housing_vs_budget_trend, housing_affordability_delta_trend
from components.topbar import get_topbar


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

csv_path = os.path.join(csv_dir, 'analysis.csv')
df = pd.read_csv(csv_path)

df = df[df['Year'].str.endswith('-07')]
years = sorted(df['Year'].str[:4].astype(int).unique())

def get_housing_tabs():
    return dbc.Tabs(
        [
            dbc.Tab(
                children=[
                    html.Div(
                        "Housing Budget Trends",
                        style={"text-align": "center", "font-size": "16px", "color": "black"}
                    ),
                    dcc.Graph(figure=housing_vs_budget_trend())
                ],
                tab_id="housing-budget-trends",
                label="Housing Budget Trends"
            ),
            dbc.Tab(
                children=[
                    html.Div(
                        "Housing Budget Affordability Delta",
                        style={"text-align": "center", "font-size": "16px", "color": "black"}
                    ),
                    dcc.Graph(figure=housing_affordability_delta_trend())
                ],
                tab_id="housing-budget-affordability-delta",
                label="Affordability Delta"
            )
        ],
        id="housing-tabs",
        active_tab="housing-budget-trends"
    )

# Layout for the housing page
layout = dbc.Container([
    get_topbar(current_path="/methods/housing", overlay=False),

    html.Link(rel="stylesheet", href="/static/css/methods-styles.css"),

    html.H4("Housing Cost Sankey Diagram", className="mt-4"),
    dbc.Row([
        dbc.Col([
            ],width=1),
        dbc.Col([
            dcc.Graph(id='sankey-graph')
        ], width=10, className="mt-4"),
        dbc.Col([
            ],width=1),
    ]),
    dbc.Row([
        dbc.Col([
            ],width=1),
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
        ], width=10, className="mt-4"),
        dbc.Col([
            ],width=1),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='income-sankey-graph')
        ], width=6),
        dbc.Col([
            get_housing_tabs()  # Call the reusable tabs function here
        ], width=6, className="mt-4"),
    ]),
    dbc.Row([
        dbc.Col([
            html.A(
                href="https://www.ocregister.com/2015/08/30/oc-faces-bifurcated-threat-inequality-and-insufficient-housing/",
                target="_blank",
                children=html.Img(
                    src="/static/assets/housing_inequality.png",
                    style={"width": "100%", "display": "block", "margin": "2 auto"}
                )
            ),
            html.P([
                "Source: ",
                html.A(
                    "The Orange County Register",
                    href="https://www.ocregister.com/2015/08/30/oc-faces-bifurcated-threat-inequality-and-insufficient-housing/",
                    target="_blank"
                )
            ]),
        ], width=3),
        dbc.Col([
            html.H3("Structural Barriers to Homeownership and Wealth Accumulation"),
            html.H4("The 20% Down Payment Threshold"),
            html.P("A 20% down payment is conventionally required to avoid Private Mortgage Insurance (PMI), an additional cost that disproportionately burdens lower-income buyers. This upfront financial hurdle exacerbates wealth stratification, as those without intergenerational wealth or substantial savings are effectively excluded from the market or forced into costlier financing structures."),
            html.H4("The True Cost of Ownership and Intergenerational Disparities"),
            html.P("The Sankey diagram illustrates how interest payments, property taxes, and insurance compound over a 30-year mortgage, significantly inflating the total expenditure. This dynamic entrenches intergenerational inequality, as households that purchased homes in earlier decades (when prices were lower relative to income) benefit from equity accumulation, while newer entrants face diminished purchasing power due to stagnant wage growth and rising housing costs."),
            html.H4("Housing Budget Affordability Delta: A Metric of Economic Polarization"),
            html.P("The delta between monthly housing costs (mortgage + taxes + insurance) and the recommended 30% housing budget serves as a stark indicator of affordability erosion. As this gap widens, middle- and working-class households are forced to allocate a larger share of income to housing, reducing disposable income for savings, education, or investment—key drivers of upward mobility."),
        ], width=6, className="mt-4"),
        dbc.Col([
            html.A(
                href="https://www.seattletimes.com/opinion/maybe-income-inequality-is-all-about-housing/",
                target="_blank",
                children=html.Img(
                    src="/static/assets/housing_rising_cost.png",
                    style={"width": "70%", "display": "block", "margin": "2 auto"}
                )
            ),
            html.P([
                "Source: ",
                html.A(
                    "The Seattle Times",
                    href="https://www.seattletimes.com/opinion/maybe-income-inequality-is-all-about-housing/",
                    target="_blank"
                )
            ]),
        ], width=3)
    ])
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