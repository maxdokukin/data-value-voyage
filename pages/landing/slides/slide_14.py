from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.vis.housing_vis import housing_sankey, income_affordability_sankey

layout = html.Div(className="section-slide", children=[
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dcc.Graph(id="sankey-graph", figure=housing_sankey(2023))
            ], width=10),
            dbc.Col([], width=1),
        ], className="mt-1"),
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dcc.Graph(id="income-graph", figure=income_affordability_sankey(2023))
            ], width = 5, className="mt-1"),
            # dbc.Col([], width=1),
            dbc.Col([
                html.H2("Remarks:", className="mt-1 mb-3 ml-5"), 
                html.Ul([ 
                    html.Li(
                        "20% Down Payment is assumed to avoid PMI (Private Mortgage Insurance).",
                        className="mb-2",  
                        style={"list-style-type": "disc"}  
                    ),
                    html.Li(
                        "30-Year Fixed Rate Mortgage is assumed.",
                        className="mb-2",
                        style={"list-style-type": "disc"}
                    ),
                    html.Li(
                        "Property Tax and Home Insurance are paid monthly. Annual costs approximated at:",
                        className="mb-2",
                        style={"list-style-type": "disc"}
                    ),
                    html.Ul([ 
                        html.Li("1.1% of Property Value for Property Tax"),
                        html.Li("0.07% of Home Value for Home Insurance")
                    ], style={"margin-left": "20px", "list-style-type": "circle"}),  
                    html.Li(
                        "Affordable Housing defined as spending ≤30% of income on housing costs.",
                        className="mb-2",
                        style={"list-style-type": "disc"}
                    )
                ], style={"padding-left": "20px"}) 
            ], width=4),
        ], className="mt-3"),
    ]),
    

])