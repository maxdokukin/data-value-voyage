from dash import html, dcc
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    get_button(
        label="Learn More about this Method",
        link="/methods/housing",
        color="#693382",
        size=(300, 50)
    ),

    html.H2("Housing slide"),
])