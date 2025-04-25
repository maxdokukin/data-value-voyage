from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from src.fetch.from_csv import fetch_final_goods_affordable
from components.topbar import get_topbar
import plotly.graph_objects as go
from dash import html, dcc, callback, Output, Input
import os
import pandas as pd

# Parameters for fetching data
goods_list = [
    'bacon','bread','butter','coffee','eggs','flour','milk',
    'pork chop','round steak','sugar','gas'
]
regions = ['United States']
income_data_source = 'FRED'
salary_interval = 'monthly'

# Fetch decade data
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

# Map good names to units
unit_map = df_1920s.set_index('name')['good_unit'].to_dict()

# Compute average affordable quantities
avg_1920s = df_1920s.groupby('name')['final_goods_affordable'].mean()
avg_2020s = df_2020s.groupby('name')['final_goods_affordable'].mean()

# Build comparison records
comparison_records = []
for name in goods_list:
    unit = unit_map.get(name, '')
    val_1920 = int(round(avg_1920s.get(name, 0)))
    val_2020 = int(round(avg_2020s.get(name, 0)))
    delta = val_2020 - val_1920
    pct_change = round((delta / val_1920 * 100), 1) if val_1920 else 0
    comparison_records.append({
        'Good (Unit)': f"{name.title()} ({unit})",
        '1920s': val_1920,
        '2020s': val_2020,
        'Delta': delta,
        '% Change': pct_change
    })

# Sort by percent change descending
comparison_records = sorted(comparison_records, key=lambda x: x['% Change'], reverse=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', 'data', 'csv')
def fetch_gini_over_time():
    csv_path = os.path.join(csv_dir, 'gini_year.csv')
    return pd.read_csv(csv_path)

gini_trend_df = fetch_gini_over_time()
gini_trend_fig = go.Figure(
    data=go.Scatter(
        x=gini_trend_df["Year"].astype(str).tolist(),
        y=gini_trend_df["Gini Coefficient"].astype(float).tolist(),
        mode="lines+markers",
        line=dict(color="orange", width=2),
        marker=dict(size=4),
        name="Gini Coefficient"
    )
)

# Findings page layout
layout = html.Div(className='container-findings', children=[
    # Topbar
    get_topbar(current_path="/findings", overlay=False),
    html.Link(rel='stylesheet', href='/static/css/findings-styles.css'),

    # Section: Quantity-Affordable Findings
    html.Div(className="section", children=[
        html.H3('Purchasing Power Findings'),
        html.P(
            'We calculated the number of units an average consumer could afford per month ' 
            'by dividing average monthly income by CPI-based prices for a basket of goods. ' 
            'Comparing the 1920s to the 2020s reveals that affordability declined across all items.'
        ),
        html.P(
            'Staples like flour and sugar saw the greatest drops—over 90%. Eggs were the most ' 
            'resilient, decreasing by about 13%, while pork chops and bacon dropped roughly 40–45%. ' 
            'Milk affordability fell by 57%, and butter became effectively unaffordable.'
        ),
        html.Div(className="table-container", children=[
            dash_table.DataTable(
                id="affordable-comparison-table",
                columns=[{'name': col, 'id': col} for col in comparison_records[0].keys()],
                data=comparison_records,
                style_table={'width': '100%'},
                style_cell={'textAlign': 'left', 'padding': '8px', 'fontSize': '14px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f4f4f4', 'padding': '8px'}
            )
        ])
    ]),

    # Section: Income Inequality Findings (Gini Analysis)
    html.Div(className="section", children=[
        html.H3('Income Inequality Findings'),
        html.P(
            'Using Lorenz curves and Gini coefficients, we quantified income distribution from 1900 to 2020. ' 
            'The Gini coefficient rose from approximately 0.45 in the early 20th century to over 0.49 ' 
            'in recent decades, indicating increased inequality.'
        ),
        html.P(
            'Composite metrics—Palma Ratio, Housing Affordability Delta, and Productivity Gap—were ' 
            'normalized and used as parameters (alpha and beta) in a Gamma distribution to model skewness and spread. ' 
            'Over time, decreasing alpha and increasing beta reflect more right-skewed and dispersed income distributions.'
        ),
        # Section: Lorenz Curve Interactive Plot
        dbc.Row([
            dbc.Col([
            ], width=1),
            dbc.Col([
                dcc.Graph(id="gini-trend-plot", figure=gini_trend_fig)
            ], width=10),
            dbc.Col([
            ], width=1),
        ]),
    ])
])
