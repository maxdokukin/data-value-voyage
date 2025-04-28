# pages/eda.py
import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import sqlite3
import os
import numpy as np
# from src.functions.db.fetch import fetch_goods_prices
# from src.functions.db.fetch import fetch_bea_incomes
# from scripts.python.data_visualization.visualize_final_goods import plot_incomes_inf_final_goods
from components.topbar import get_topbar
from pages.vis.quantity_affordable_vis import create_goods_price_change_heatmap_dollar_change, create_goods_price_change_heatmap_percent_change, price_change_tabs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

def get_goods_prices_graph():
    csv_path = os.path.join(csv_dir, 'goods_prices.csv')
    df = pd.read_csv(csv_path)

    # Filter to selected goods only
    selected_goods = ['bacon', 'bread', 'butter', 'coffee', 'eggs', 'flour', 'milk', 'pork chop', 'round steak', 'sugar', 'gas']
    df = df[df['name'].isin(selected_goods)]

    df['Year'] = df['date'].str.slice(0, 7)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.sort_values(by=['name', 'Year'])
    df['price'] = df.groupby('name')['price'].transform(lambda group: group.interpolate(method='linear'))

    fig = go.Figure()

    for good in df['name'].unique():
        subset = df[df['name'] == good]
        legend_name = f"{good} /{subset['good_unit'].iloc[0]}"
        x_vals = subset['Year'].astype(str).tolist()
        y_vals = np.round(subset['price'].astype(float), 2).tolist()

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name=legend_name,
            hovertemplate=legend_name + ": %{y}<extra></extra>"
        ))

    fig.update_layout(
        title="Price Trends Over Time",
        xaxis_title="Year-Month",
        yaxis_title="Price",
        hovermode="x unified"
    )
    return fig

def get_affordable_goods_graph():
    csv_path = os.path.join(csv_dir, 'affordable_goods.csv')
    df = pd.read_csv(csv_path)

    goods = ['bacon', 'bread', 'butter', 'coffee', 'eggs', 'flour', 'milk', 'pork chop', 'round steak', 'sugar']
    df = df[df['good_name'].isin(goods)]

    fig = go.Figure()

    for good in df['good_name'].unique():
        subset = df[df['good_name'] == good]
        legend_name = f"{good} /{subset['good_unit'].iloc[0]}"
        x_vals = subset['year'].astype(str).tolist()
        y_vals = subset['affordable_monthly_quantity'].astype(int).tolist()
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name=legend_name,
            hovertemplate=legend_name + ": %{y}<extra></extra>"
        ))

    fig.update_layout(
        title="Affordable Quantity of Goods per Month",
        xaxis_title="Year-Month",
        yaxis_title="Affordable Monthly Quantity",
        hovermode="x unified"
    )
    return fig

def get_affordable_goods_graph_no_flower_sugar():
    csv_path = os.path.join(csv_dir, 'affordable_goods.csv')
    df = pd.read_csv(csv_path)

    goods = ['bacon', 'bread', 'butter', 'coffee', 'eggs', 'milk', 'pork chop', 'round steak', 'gas']
    df = df[df['good_name'].isin(goods)]

    fig = go.Figure()

    for good in df['good_name'].unique():
        subset = df[df['good_name'] == good]
        legend_name = f"{good} /{subset['good_unit'].iloc[0]}"
        x_vals = subset['year'].astype(str).tolist()
        y_vals = subset['affordable_monthly_quantity'].astype(int).tolist()
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name=legend_name,
            hovertemplate=legend_name + ": %{y}<extra></extra>"
        ))

    fig.update_layout(
        title="Affordable Quantity of Goods per Month (No Flour or Sugar)",
        xaxis_title="Year-Month",
        yaxis_title="Affordable Monthly Quantity",
        hovermode="x unified"
    )
    return fig

def get_income_averages_graph():
    income = pd.read_csv("https://raw.githubusercontent.com/ryanfernald/Value-Voyage-A-Journey-Through-Decades-of-Prices/refs/heads/main/data/ryans_data/income1913-1998.csv")

    income_graph_fig = go.Figure()

    income_graph_fig.add_trace(go.Scatter(x=income["year"], y=income["tax-units"],
                             mode='lines+markers',
                             name="Tax Units"))

    income_graph_fig.add_trace(go.Scatter(x=income["year"], y=income["Average Income Adjusted $ 1998"],
                             mode='lines+markers',
                             name="Avg Income Adjusted (1998 $)"))

    income_graph_fig.add_trace(go.Scatter(x=income["year"], y=income["Income Unadjusted"],
                             mode='lines+markers',
                             name="Income Unadjusted"))

    income_graph_fig.update_layout(
        title="Income Trends Over Years",
        xaxis_title="Year",
        yaxis_title="Income / Tax Units",
        template="plotly_white",
        hovermode="x"
    )
    return income_graph_fig

def get_income_shares_graph():
    income = pd.read_csv("https://raw.githubusercontent.com/ryanfernald/Value-Voyage-A-Journey-Through-Decades-of-Prices/refs/heads/main/data/ryans_data/income1913-1998.csv")
    columns_to_plot = [
        "P90-100", "P90-95", "P95-99", "P99-100",
        "P99.5-100", "P99.9-100", "P99.99-100"
    ]

    income_shares = go.Figure()

    for col in columns_to_plot:
        income_shares.add_trace(go.Scatter(x=income["year"], y=income[col],
                             mode='lines+markers',
                             name=col))

    income_shares.update_layout(
        title="Top Income Shares by Percentage",
        xaxis_title="Year",
        yaxis_title="Income Share (%)",
        template="plotly_white",
        hovermode="x"
    )
    return income_shares



# Define the layout for the analysis page
layout = dbc.Container(
    [
        get_topbar(current_path="/eda", overlay=False),

        dbc.Row([
            dbc.Col([],width=1),
            dbc.Col([
                html.H2("Price Change From Decade to Decade for Various Goods"),
                html.H4("Each cell of the heatmap shows the change in price from one decade to the next."),
             ], width=10, className="mb-4 mt-2"),
             dbc.Col([],width=1),
        ]),
        dbc.Row(
            [
                dbc.Col([],width=1),
                dbc.Col(
                    price_change_tabs(), width=10
                ),
                dbc.Col([],width=1),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H1("Price Trends Over Time"),
                        html.H2("Data Source:"),
                        html.P("This is a detailed explanation of the analysis. It can include multiple paragraphs and should provide context for the visualizations.")
                    ]),
                    width=5
                ),
                dbc.Col(
                    dcc.Graph(id="price-trends-graph", figure=get_goods_prices_graph()), 
                    width=7
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="affordable-goods-graph", figure=get_affordable_goods_graph()),  
                    width=7
                ),
                dbc.Col(
                    html.Div([
                        html.H1("Affordable Quantity of Goods over a Century"),
                        html.H2("Data Source:"),
                        html.P("Additional context or insights related to the second graph.")
                    ]),
                    width=5
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="affordable-goods-graph", figure=get_affordable_goods_graph_no_flower_sugar()),  
                    width=7
                ),
                dbc.Col(
                    html.Div([
                        html.H1("Same Graph as Above without flower and sugar"),
                    ]),
                    width=5
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H1("Income Shares by Percentage"),
                        html.H2("Data Source:"),
                        html.P("Additional context or insights related to the third graph.")
                    ]),
                    width=5
                ),
                dbc.Col(
                    dcc.Graph(id="income-shares-graph", figure=get_income_shares_graph()), 
                    width=7
                ),
            ]
        ),
    ],
    fluid=True
)

# Export the layout
export_layout = layout
