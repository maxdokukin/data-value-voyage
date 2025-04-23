from dash import html, dcc
from components.topbar import get_topbar

layout = html.Div(className="section-slide", children=[
    html.H2("Now we combine this data"),
    dcc.Markdown('''
    $$
    \\text{quantity_affordable}_{\\text{ year}} = \\frac{\\text{average_monthly_income}_{\\text{ year}}}{\\text{good_price}_{\\text{ year}}}
    $$
    ''', mathjax=True)  # mathjax=True enables LaTeX rendering
])