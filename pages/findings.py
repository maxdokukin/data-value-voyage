from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import os
import pandas as pd
# Housing visuals
from src.visualize.housing_vis import housing_sankey, housing_vs_budget_trend


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


# Gini coefficient trend\BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', 'data', 'csv')

def fetch_gini_over_time(): return pd.read_csv(os.path.join(csv_dir,'gini_year.csv'))
gini_df = fetch_gini_over_time()
gini_fig = go.Figure(data=go.Scatter(
    x=gini_df['Year'].astype(str),
    y=gini_df['Gini Coefficient'],
    mode='lines+markers', line=dict(color='orange',width=2), marker=dict(size=4)
))

# Findings page layout
layout = html.Div(className='container-findings', children=[
    get_topbar(current_path='/findings', overlay=False),
    html.Link(rel='stylesheet', href='/static/css/findings-styles.css'),

    # Method 1: Purchasing Power Findings
    html.Div(className='section', children=[
        html.Div(className='section-header d-flex align-items-center justify-content-between', children=[
            html.H3('Purchasing Power Findings'),
            dbc.Button('View Method', href='/methods/quantity-affordable', color='secondary', size='sm')
        ]),
        html.P('By dividing average monthly income by CPI-based prices for a basket of goods, we measured how many units an average consumer could afford per month. Comparing the 1920s to the 2020s shows declines across all items.'),
        html.P('Flour and sugar affordability dropped by over 90%, eggs fell ~13%, pork chops and bacon by ~40–45%, milk by ~57%, and butter became effectively unaffordable.'),
        html.Div(className='table-container', children=[
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
    ]),

    # Method 2: Income Inequality Findings
    html.Div(className='section', children=[
        html.Div(className='section-header d-flex align-items-center justify-content-between', children=[
            html.H3('Income Inequality Findings'),
            dbc.Button('View Method', href='/methods/gini', color='secondary', size='sm')
        ]),
        html.P('Using Lorenz curves and Gini coefficients, income distribution was quantified from 1900 to 2020. The Gini rose from ~0.45 to >0.49, indicating growing inequality.'),
        html.P('Normalized metrics (Palma Ratio, Housing Delta, Productivity Gap) served as alpha/beta parameters in a Gamma distribution, revealing increasing skew and dispersion over time.'),
        dbc.Row([dbc.Col([],width=1), dbc.Col([dcc.Graph(id='gini-trend',figure=gini_fig)],width=10), dbc.Col([],width=1)])
    ]),

    # Method 3: Housing Affordability Findings
    html.Div(className='section', children=[
        html.Div(className='section-header d-flex align-items-center justify-content-between', children=[
            html.H3('Housing Affordability Findings'),
            dbc.Button('View Method', href='/methods/housing', color='secondary', size='sm')
        ]),
        html.P('Our housing analysis combined Sankey diagrams, budget trend charts, and affordability delta metrics to assess structural barriers in homeownership.'),
        html.P('A 20% down payment requirement and cumulative costs (interest, taxes, insurance) disproportionately exclude lower-income households. The gap between actual housing expenditures and the recommended 30% budget has widened, straining disposable income.'),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=housing_sankey(2023))], width=6),
            dbc.Col([dcc.Graph(figure=housing_vs_budget_trend())], width=6)
        ])
    ])
])
