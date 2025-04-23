from dash import dcc, html
from components.topbar import get_topbar

layout = html.Div(className='container-objectives', children=[
    get_topbar(current_path="/objectives", overlay=False),

    html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),

    # Primary objective section
    html.Div(className='section', children=[
        html.H2('Primary Objective', className='section__title'),
        html.P(
            'Transform CPI and purchasing‑power data into quantities of everyday goods and '
            'calculate how many units an average consumer could buy per month, '
            'across decades from 1900 to 2020 (10‑year intervals).',
            className='section__description'
        ),
        html.Ul([
            html.Li('Convert CPI indices into quantities of goods (milk, eggs, sugar, etc.)'),
            html.Li('Model average monthly purchasing power for each decade'),
            html.Li('Visualize trends in a clear, user‑friendly format'),
        ], className='objective-list'),
    ]),

    # Secondary objectives
    html.Div(className='section', children=[
        html.H2('Secondary Objectives', className='section__title'),
        html.Ul([
            html.Li('Analyze generational income data and affordability shifts'),
            html.Li('Identify historical periods of relative economic prosperity'),
            html.Li('Experiment with ML‑based forecasting of future price trends'),
        ], className='objective-list'),
    ]),

    # Broader impact
    html.Div(className='section', children=[
        html.H2('Broader Impact', className='section__title'),
        html.P(
            'Offer an accessible dashboard that demystifies inflation and purchasing power, '
            'helping non‑expert users grasp the real‑world impact of price changes.',
            className='section__description'
        ),
    ]),

])
