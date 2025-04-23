from dash import html, dcc
from components.button import get_button

layout = html.Div(className="section-slide", children=[
    html.H2("Here are key findings recapped:"),
    html.H3("Average consumer today can afford to buy more food and gas, than one in 1920s"),
    html.H3("Income inequality has been decreasing since 1970s"),
    html.H3("Housing affordability significantly decreased, compared to 1970s"),

    get_button(
        label="Learn More about our Findings",
        link="/findings",
        color="#693382",
        size=(300, 50)
    )
])