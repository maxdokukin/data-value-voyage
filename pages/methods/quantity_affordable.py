from dash import dcc, html
from components.topbar import get_topbar
import dash_bootstrap_components as dbc
from pages.vis.quantity_affordable_vis import create_goods_price_change_heatmap_dollar_change, create_goods_price_change_heatmap_percent_change, price_change_tabs
from dash import dcc, html, Input, Output, callback


layout = html.Div(className='container-objectives', children=[
    get_topbar(current_path="/methods/quantity-affordable", overlay=False),

    # html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([
                dbc.Col([
                    price_change_tabs()
                ])
            ], width=8)
        ])
    ])
])