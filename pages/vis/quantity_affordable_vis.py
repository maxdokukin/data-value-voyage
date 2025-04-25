from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import os
import pandas as pd
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

#### Heatmap for Dollar Chagen #######

def create_goods_price_change_heatmap_dollar_change():

    csv_path = os.path.join(csv_dir, 'goods_prices.csv')
    df = pd.read_csv(csv_path)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    df = df[df['month'] == 7]

    # Filter for specific goods
    goods_of_interest = ['sugar', 'round steak', 'pork chop', 'milk', 'gas',
                         'flour', 'eggs', 'coffee', 'butter', 'bread', 'bacon']
    df = df[df['name'].str.lower().isin([g.lower() for g in goods_of_interest])]

    # Pivot table: rows = goods, columns = decade years, values = price
    df_decades = df[df['year'] % 10 == 0]
    pivot = df_decades.pivot_table(index='name', columns='year', values='price')

    # Calculate dollar change and drop the first column (e.g., 1890)
    dollar_change = pivot.diff(axis=1).iloc[:, 1:].round(2)  # skip the first column
    years = dollar_change.columns.to_list()
    goods = dollar_change.index.to_list()

    # Build annotations
    annotations = []
    for i, good in enumerate(goods):
        for j, year in enumerate(years):
            value = dollar_change.iloc[i, j]
            if pd.notna(value):
                annotations.append(dict(
                    text=f"{value:+.2f}",
                    x=year,
                    y=good,
                    showarrow=False,
                    font=dict(color="black", size=12)
                ))

    # Build heatmap
    fig = go.Figure(data=go.Heatmap(
        z=dollar_change.values,
        x=years,
        y=goods,
        colorscale='BrBG',
        zmid=0,
        colorbar=dict(title="Dollar Change")
    ))

    fig.update_layout(
        title="Decadal Price Change in USD",
        xaxis=dict(title="Year", side="top", tickmode="array", tickvals=years),
        yaxis=dict(title="Good"),
        annotations=annotations,
        height=600
    )

    return fig

##### Heatmap for Percent Change #######

def create_goods_price_change_heatmap_percent_change():

    csv_path = os.path.join(csv_dir, 'goods_prices.csv')
    df = pd.read_csv(csv_path)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Filter for July entries only
    df = df[df['month'] == 7]

    # Filter for specific goods
    goods_of_interest = ['sugar', 'round steak', 'pork chop', 'milk', 'gas',
                         'flour', 'eggs', 'coffee', 'butter', 'bread', 'bacon']
    df = df[df['name'].str.lower().isin([g.lower() for g in goods_of_interest])]

    # Pivot table: rows = goods, columns = decade years, values = price
    df_decades = df[df['year'] % 10 == 0]
    pivot = df_decades.pivot_table(index='name', columns='year', values='price')

    # Calculate percent change and drop the first column (no prior comparison)
    pct_change = pivot.pct_change(axis=1, fill_method=None).iloc[:, 1:] * 100
    pct_change = pct_change.round(2)
    years = pct_change.columns.to_list()
    goods = pct_change.index.to_list()

    # Build annotations
    annotations = []
    for i, good in enumerate(goods):
        for j, year in enumerate(years):
            value = pct_change.iloc[i, j]
            if pd.notna(value):
                annotations.append(dict(
                    text=f"{value:+.1f}%",
                    x=year,
                    y=good,
                    showarrow=False,
                    font=dict(color="black", size=12)
                ))

    # Build heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pct_change.values,
        x=years,
        y=goods,
        colorscale='RdBu',
        zmid=0,
        colorbar=dict(title="% Change")
    ))

    fig.update_layout(
        title="Decadal Price Change in Percent",
        xaxis=dict(title="Year", side="top", tickmode="array", tickvals=years),
        yaxis=dict(title="Good"),
        annotations=annotations,
        height=600
    )

    return fig


####### Price Change Tabs #########

def price_change_tabs():
    return dbc.Tabs(
        [
            dbc.Tab(
                children=[
                    html.Div(
                        "Dollar Value Changes for Goods by Decade",
                        style={"text-align": "center", "font-size": "16px", "color": "black"}
                    ),
                    dcc.Graph(figure=create_goods_price_change_heatmap_dollar_change())
                ],
                tab_id="create_goods_price_change_heatmap_dollar_change",
                label="Dollar Change"
            ),
            dbc.Tab(
                children=[
                    html.Div(
                        "Percent Value Changes for Goods by Decade",
                        style={"text-align": "center", "font-size": "16px", "color": "black"}
                    ),
                    dcc.Graph(figure=create_goods_price_change_heatmap_percent_change())
                ],
                tab_id="create_goods_price_change_heatmap_percent_change",
                label="Percent Change"
            )
        ],
        id="price-change-tabs",
        active_tab="create_goods_price_change_heatmap_dollar_change"
    )