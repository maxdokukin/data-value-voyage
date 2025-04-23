from dash import html, dcc
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    get_button(
        label="Learn More about this Method",
        link="/methods/gini",
        color="#693382",
        size=(300, 50)
    ),

    html.H2("Income inequality slide"),
])