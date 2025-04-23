from dash import html, dcc
from src.visualize.goods_affordable import plot_incomes_inf_final_goods

fig = plot_incomes_inf_final_goods(
    db_path='data/db/sqlite/database.sqlite',
    year_range=(1929, 2024),
    goods_list=[
        'bacon','bread','butter','coffee','eggs','flour','milk',
        'pork chop','round steak','sugar','gas'
    ],
    regions=['united states'],
    income_data_source='FRED',
    salary_interval='monthly',
    output_format='df'
)

layout = html.Div(
    className="section-slide",
    children=[
        html.Div(
            className="plot-container",
            children=dcc.Graph(
                id="plot1",
                figure=fig,
                config={"displayModeBar": False},
                style={"height": "100%", "width": "100%"}
            )
        )
    ]
)


