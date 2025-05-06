# pages/eda.py
from dash import dcc, html
import dash_bootstrap_components as dbc
import os
# from src.functions.db.fetch import fetch_goods_prices
# from src.functions.db.fetch import fetch_bea_incomes
# from scripts.python.data_visualization.visualize_final_goods import plot_incomes_inf_final_goods
from components.topbar import get_topbar
from src.visualize.quantity_affordable_vis import price_change_tabs
from src.visualize.analysis_vis import gini_eda_tabs, get_goods_prices_graph, get_goods_prices_graph_after_1970, get_affordable_goods_graph, get_affordable_goods_graph_no_flower_sugar_after1980

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

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
        ], className="mt-4"),
        dbc.Row(
            [
                dbc.Col([],width=1),
                dbc.Col(
                    price_change_tabs(), width=10
                ),
                dbc.Col([],width=1),
            ]
        ),

        dbc.Row([
            dbc.Col([],width=1),
            dbc.Col([
                html.H2("Gini Coefficient Analysis About US Presidents, Wartime Events, and Major Economic Recessions."),
                html.H3("The Gini Coefficient is a measure of income inequality within a population, but it is also a lagging indicator, meaning it reflects past events rather than current conditions."),
                html.Li("The US Presidents don't seem to have a significant impact on the Gini Coefficient, there is no notable trend between Republic (red blocks) and Democrat (blue blocks) presidents."),
                html.Li("The Wartime events seem to have a more obvious impact on the Gini Coefficient, especially around WWII, The Korean War and the Vietnam War."),
                html.Li("Major Economic Recessions don't seem to have a significant impact on the Gini Coefficnent.", className="mb-4"),
                gini_eda_tabs()
            ], width=10,)
        ], className="mb-4 mt-3"),
        
        dbc.Row(
            [
                dbc.Col([],width=1),
                dbc.Col(
                    html.Div([
                        html.H2("Price Trends Over Time"),
                        html.P("Double Click on the Legend on a specific Good to isolate it."),
                    ]),
                    width=10
                ),
                dbc.Col([],width=1),
            ]
        ),

        dbc.Row([
            # dbc.Col([],width=1),
            dbc.Col(
                    dcc.Graph(id="price-trends-graph", figure=get_goods_prices_graph()), 
                    width=6
                ),
            dbc.Col(
                    dcc.Graph(id="price-trends-graph", figure=get_goods_prices_graph_after_1970()), 
                    width=6
                ),
            # dbc.Col([],width=1),
            ]
        ),

        dbc.Row(
            [
                dbc.Col([],width=1),
                dbc.Col(
                    html.Div([
                        html.H2("Affordable Quantity of Goods over a Century"),
                        html.P("Affordable Quantity is the Monthly Income Divited by the price of Goods. So when income increases and the price of goods stays relatively the same, the affordable quantity goes up.")
                    ]),
                    width=10
                ),
                dbc.Col([],width=1),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="affordable-goods-graph", figure=get_affordable_goods_graph()),  
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id="affordable-goods-graph-noflower-nosugar", figure=get_affordable_goods_graph_no_flower_sugar_after1980()),  
                    width=6
                )
            ]
        ),

    ],
    fluid=True
)

# Export the layout
export_layout = layout
