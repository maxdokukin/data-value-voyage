from dash import html, dcc
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    get_button(
        label="Learn More about our Objectives",
        link="/objectives",
        color="#693382",
        size=(300, 50)
    ),
    html.H2("We had one question"),
    html.H3("Does an average consumer today can afford to buy more than one in 1920s?"),
    html.Div(className="scroll-hint", children="↓")
])