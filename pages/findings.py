from dash import dcc, html
from components.topbar import get_topbar

layout = html.Div(className='container-objectives', children=[
    get_topbar(current_path="/findings", overlay=False),

    # html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),
    html.H2('Construction findings', className='section__title'),
])
