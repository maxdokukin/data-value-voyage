from dash import html, dcc
from components.topbar import get_topbar

layout = html.Div(className="section-slide", children=[
            get_topbar(show_home=True, overlay=True),

            html.Div(className="hero", children=[
                html.Div(className="overlay", children=[
                    html.Div(className="overlay-content", children=[
                        html.H1("Value Voyage"),
                        html.H2("A journey through decades of prices")
                    ]),
                    html.Div(className="overlay-footer", children=[
                        html.H3("by Max Dokukin and Ryan Fernald")
                    ])
                ]),
                html.Div(className="scroll-hint", children="↓")
            ])
        ])