from dash import html, dcc
from src.visualize.incomes import compare_income_data_sources

# build the figure
fig = compare_income_data_sources(
    db_path='data/db/sqlite/database.sqlite',
    start_year=1900,
    end_year=2024,
    regions=['united states'],
    sources=['IRS', 'BEA', 'FRED'],
    markers=['circle', 'x', 'cross'],
    output_format='df',
    y_scale='log'
)

layout = html.Div(
    className="section-slide",
    children=[
        html.Div(
            className="plot-container",
            children=dcc.Graph(
                id="compare-income-graph",
                figure=fig,
                config={"displayModeBar": False},
                style={"width": "100%", "height": "100%"}
            )
        )
    ]
)
