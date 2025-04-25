import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import plotly.graph_objects as go
import os

from components.topbar import get_topbar
from src.visualize.goods_prices import plot_goods_prices
from src.visualize.incomes import compare_income_data_sources
from src.visualize.goods_affordable import plot_incomes_inf_final_goods
from src.fetch.from_csv import fetch_final_goods_affordable

# Data paths and parameters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = 'data/db/sqlite/database.sqlite'
goods_list = [
    'bacon','bread','butter','coffee','eggs','flour','milk',
    'pork chop','round steak','sugar','gas'
]
regions = ['united states']
income_data_source = 'FRED'
salary_interval = 'monthly'

# Generate figures
fig_goods = plot_goods_prices(
    db_path=db_path,
    year_range=(1900, 2020),
    goods_list=goods_list,
    output_format='df'
)

fig_income = compare_income_data_sources(
    db_path=db_path,
    start_year=1900,
    end_year=2024,
    regions=regions,
    sources=['IRS', 'BEA', 'FRED'],
    markers=['circle', 'x', 'cross'],
    output_format='df',
    y_scale='log'
)

fig_quantity = plot_incomes_inf_final_goods(
    db_path=db_path,
    year_range=(1900, 2020),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)

# Table data: 1920s vs 2020s comparison
df_1920s = fetch_final_goods_affordable(
    year_range=(1920, 1929),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)
df_2020s = fetch_final_goods_affordable(
    year_range=(2020, 2029),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)
unit_map = df_1920s.set_index('name')['good_unit'].to_dict()
avg_1920s = df_1920s.groupby('name')['final_goods_affordable'].mean()
avg_2020s = df_2020s.groupby('name')['final_goods_affordable'].mean()
comparison_records = []
for name in goods_list:
    unit = unit_map.get(name, '')
    v20 = int(round(avg_1920s.get(name, 0)))
    v21 = int(round(avg_2020s.get(name, 0)))
    delta = v21 - v20
    pct = round((delta / v20 * 100), 1) if v20 else 0
    comparison_records.append({
        'Good (Unit)': f"{name.title()} ({unit})",
        '1920s': v20,
        '2020s': v21,
        'Delta': delta,
        '% Change': pct
    })
comparison_records = sorted(comparison_records, key=lambda x: x['% Change'], reverse=True)

# Layout definition
layout = dbc.Container(fluid=True, children=[
    # Topbar
    get_topbar(current_path='/methods/quantity-affordable', overlay=False),
    html.Link(rel='stylesheet', href='/static/css/methods-styles.css'),

    # Header / Introduction
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(html.H2('Quantifying Purchasing Power via CPI-to-Good Conversion'), width=10),
        dbc.Col(width=1),
        dbc.Col(html.P(
            'This page details how we transformed CPI indices into tangible units of everyday goods and computed the number of units an average consumer could afford each month from 1900 to 2020 (10-year intervals).'
        ), width=10),
        dbc.Col(width=1),
    ], className='my-4'),

    # Goods Price Trends
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dcc.Graph(id='goods-price-trends', figure=fig_goods), width=10),
        dbc.Col(width=1),
    ], className='mb-4'),

    # Income Trends
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dcc.Graph(id='income-trends', figure=fig_income), width=10),
        dbc.Col(width=1),
    ], className='mb-4'),

    # Calculation Formula
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(html.H3('Calculating Quantity Affordable'), width=10),
        dbc.Col(width=1),
        dcc.Markdown('''
            $$
            \\text{quantity_affordable}_{\\text{ year}} = \\frac{\\text{average_monthly_income}_{\\text{ year}}}{\\text{good_price}_{\\text{ year}}}
            $$
            ''', mathjax=True),
        dbc.Col(width=1),
    ], className='mb-4'),

    # Quantity Affordable Trends
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dcc.Graph(id='quantity-affordable-trends', figure=fig_quantity), width=10),
        dbc.Col(width=1),
    ], className='mb-4'),

    # Affordability Comparison Table
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dash_table.DataTable(
            id='affordability-table',
            columns=[{'name': c, 'id': c} for c in comparison_records[0].keys()],
            data=comparison_records,
            style_table={'width': '100%'},
            style_cell={'padding': '8px', 'textAlign': 'left'},
            style_header={'fontWeight': 'bold', 'backgroundColor': '#f4f4f4'}
        ), width=10),
        dbc.Col(width=1),
    ], className='mb-5'),
])
