from dash import dcc, html
from components.topbar import get_topbar

layout = html.Div(className='container-objectives', children=[
    get_topbar(overlay=False),

    # html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),
    html.H2('Construction about-us', className='section__title'),
])
