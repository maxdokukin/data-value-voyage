import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import src.fetch.from_gcloud as gamma_resampling_df
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from dash import dcc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR,'..','..', 'data', 'csv')

def presidents_gini_plot():
    # Load Gini data
    csv_path = os.path.join(csv_dir, 'gini_year.csv')
    gini_trend_df = pd.read_csv(csv_path)
    
    # President data (1913-2023)
    presidents = [
        {'name': 'Woodrow Wilson', 'party': 'D', 'start': 1913, 'end': 1921},
        {'name': 'Warren Harding', 'party': 'R', 'start': 1921, 'end': 1923},
        {'name': 'Calvin Coolidge', 'party': 'R', 'start': 1923, 'end': 1929},
        {'name': 'Herbert Hoover', 'party': 'R', 'start': 1929, 'end': 1933},
        {'name': 'Franklin Roosevelt', 'party': 'D', 'start': 1933, 'end': 1945},
        {'name': 'Harry Truman', 'party': 'D', 'start': 1945, 'end': 1953},
        {'name': 'Dwight Eisenhower', 'party': 'R', 'start': 1953, 'end': 1961},
        {'name': 'John Kennedy', 'party': 'D', 'start': 1961, 'end': 1963},
        {'name': 'Lyndon Johnson', 'party': 'D', 'start': 1963, 'end': 1969},
        {'name': 'Richard Nixon', 'party': 'R', 'start': 1969, 'end': 1974},
        {'name': 'Gerald Ford', 'party': 'R', 'start': 1974, 'end': 1977},
        {'name': 'Jimmy Carter', 'party': 'D', 'start': 1977, 'end': 1981},
        {'name': 'Ronald Reagan', 'party': 'R', 'start': 1981, 'end': 1989},
        {'name': 'George H.W. Bush', 'party': 'R', 'start': 1989, 'end': 1993},
        {'name': 'Bill Clinton', 'party': 'D', 'start': 1993, 'end': 2001},
        {'name': 'George W. Bush', 'party': 'R', 'start': 2001, 'end': 2009},
        {'name': 'Barack Obama', 'party': 'D', 'start': 2009, 'end': 2017},
        {'name': 'Donald Trump', 'party': 'R', 'start': 2017, 'end': 2021},
        {'name': 'Joe Biden', 'party': 'D', 'start': 2021, 'end': 2023}
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add presidential term rectangles first (so they're behind the line)
    for president in presidents:
        fig.add_vrect(
            x0=president['start'],
            x1=president['end'],
            fillcolor='blue' if president['party'] == 'D' else 'red',
            opacity=0.2,
            layer='below',
            line_width=0,
            annotation_text=president['name'],
            annotation_position='top left',
            annotation_font_size=10,
            annotation_textangle=-90
        )
    
    # Add Gini coefficient line
    fig.add_trace(go.Scatter(
        x=gini_trend_df["Year"].astype(int).tolist(),
        y=gini_trend_df["Gini Coefficient"].astype(float).tolist(),
        mode="lines+markers",
        line=dict(color="grey", width=2),
        marker=dict(size=4),
        name="Gini Coefficient"
    ))
    
    # Update layout
    fig.update_layout(
        title="Gini Coefficient Over Time with Presidential Terms",
        xaxis_title="Year",
        yaxis_title="Gini Coefficient",
        xaxis=dict(
            tickangle=50,
            range=[1912, 2024]
        ),
        yaxis=dict(
            autorange=False,
            range=[
                gini_trend_df["Gini Coefficient"].min() - 0.02,
                gini_trend_df["Gini Coefficient"].max() + 0.02
            ]
        ),
        template="plotly_white",
        hovermode="x",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
    )
    
    return fig

def war_gini_plot():
    # Load Gini data
    csv_path = os.path.join(csv_dir, 'gini_year.csv')
    gini_trend_df = pd.read_csv(csv_path)
    
    # War data (1913-2023)
    wars = [
        {'name': 'World War I', 'start': 1914, 'end': 1918, 'color': 'darkblue'},
        {'name': 'World War II', 'start': 1941, 'end': 1945, 'color': 'navy'},
        {'name': 'Korean War', 'start': 1950, 'end': 1953, 'color': 'firebrick'},
        {'name': 'Vietnam War', 'start': 1964, 'end': 1975, 'color': 'darkgreen'},
        {'name': 'Persian Gulf War', 'start': 1990, 'end': 1991, 'color': 'mediumpurple'},
        {'name': 'Iraq War', 'start': 2003, 'end': 2011, 'color': 'darkorange'},
        {'name': 'Afghanistan War', 'start': 2001, 'end': 2021, 'color': 'darkslategray'}
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add Gini coefficient line first
    fig.add_trace(go.Scatter(
        x=gini_trend_df["Year"].astype(int).tolist(),
        y=gini_trend_df["Gini Coefficient"].astype(float).tolist(),
        mode="lines+markers",
        line=dict(color="grey", width=2),
        marker=dict(size=4),
        name="Gini Coefficient",
        hovertemplate="Year: %{x}<br>Gini: %{y:.3f}<extra></extra>"
    ))
    
    # Add war rectangles with different colors
    for war in wars:
        fig.add_vrect(
            x0=war['start'],
            x1=war['end'],
            fillcolor=war['color'],
            opacity=0.3,  # Slightly more opaque than presidents for better visibility
            layer='below',
            line_width=0,
            annotation_text=war['name'],
            annotation_position='top left',
            annotation_font_size=10,
            annotation_textangle=-90
        )
    
    # Update layout
    fig.update_layout(
        title="Gini Coefficient Over Time with Major US Wars",
        xaxis_title="Year",
        yaxis_title="Gini Coefficient",
        xaxis=dict(
            tickangle=50,
            range=[1912, 2024],
            tickmode='array',
            tickvals=list(range(1920, 2025, 10))
        ),
        yaxis=dict(
            autorange=False,
            range=[
                gini_trend_df["Gini Coefficient"].min() - 0.02,
                gini_trend_df["Gini Coefficient"].max() + 0.02
            ]
        ),
        template="plotly_white",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
    )
    
    return fig

def gini_eda_tabs():
    return dbc.Tabs([
    dbc.Tab(dcc.Graph(figure=presidents_gini_plot()), label="Presidents - Gini Coefficient Plot"),
    dbc.Tab(dcc.Graph(figure=war_gini_plot()), label="Wartime - Gini Coefficient Plot"),
])