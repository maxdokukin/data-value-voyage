from dash import dcc, html
from components.topbar import get_topbar

layout = html.Div(className='container-objectives', children=[
    get_topbar(current_path="/data-sources", overlay=False),

    # html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),
    html.H2('Construction data-sources', className='section__title'),
])
