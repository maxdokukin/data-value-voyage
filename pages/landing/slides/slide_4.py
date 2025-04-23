from dash import html, dcc
from src.visualize.goods_prices import plot_goods_prices

fig = plot_goods_prices(
    db_path='data/db/sqlite/database.sqlite',
    year_range=(1900, 2020),
    goods_list=[
        'bacon','bread','butter','coffee','eggs','flour','milk',
        'pork chop','round steak','sugar','gas'
    ],
    output_format='df'
)

layout = html.Div(
    className="section-slide",
    children=[
        html.Div(
            className="plot-container",
            children=dcc.Graph(
                id="goods-prices-graph",
                figure=fig,
                config={"displayModeBar": False},
                style={"width": "100%", "height": "100%"}
            )
        )
    ]
)
