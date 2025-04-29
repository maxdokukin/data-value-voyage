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


def build_income_distribution_pyramid():
    csv_path = os.path.join(csv_dir, 'quintile_historical.csv')
    df = pd.read_csv(csv_path)

    df = df.sort_values("Year", ascending=True)
    quintiles = [
        ("Lowest fifth", "blue"),
        ("Second fifth", "firebrick"),
        ("Middle fifth", "gold"),
        ("Fourth fifth", "forestgreen"),
        ("Highest fifth", "darkorange"),
        ("Top 5 percent", "lightblue")
    ]
    for quintile, _ in quintiles:
        df[quintile] = df[quintile].replace(',', '', regex=True).astype(float).astype(int).tolist()

    fig = go.Figure()

    for quintile, color in quintiles:
        fig.add_trace(go.Bar(
            y=df["Year"].astype(str).tolist(),
            x=df[quintile].astype(float).tolist(),
            name=quintile,
            orientation='h',
            marker=dict(color=color),
        ))

    fig.update_layout(
        barmode='stack',
        title="Income Distribution by Population Group (Mean Income per Group)",
        xaxis_title="Mean Income for Each Group",
        yaxis_title="Year",
        template="plotly_white",
        height=900,
        margin=dict(l=80, r=20, t=60, b=60),
        legend=dict(title="Income Groups"),
        hovermode="y unified",
    )

    return fig

# example hist income distrubition function plot

def income_histogram_with_quintiles():
    # df = gamma_resampling_df

    csv_path = os.path.join(csv_dir, 'gamma_resampling.csv')
    df = pd.read_csv(csv_path)

    df_2023 = df[df['Year'] == 2023]
    incomes = df_2023['Income Sample'].sort_values()
    
    q = incomes.quantile([0.2, 0.4, 0.6, 0.8])
    quintile_edges = [incomes.min()] + q.tolist() + [incomes.max()]
    quintile_medians = [
        incomes[(incomes >= quintile_edges[i]) & (incomes < quintile_edges[i+1])].median()
        for i in range(5)
    ]
    
    fig = ff.create_distplot(
        [incomes],
        group_labels=['Income Sample'],
        bin_size=5000,
        curve_type='kde',
        show_hist=True,
        colors=['#888'],
        show_rug=False
    )

    colors = ['#FFDDC1', '#FFABAB', '#a0ffc3', '#D5AAFF', '#A0C4FF']
    for i in range(5):
        fig.add_shape(
            type="rect",
            x0=quintile_edges[i],
            x1=quintile_edges[i+1],
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            fillcolor=colors[i],
            opacity=0.8,
            layer="below",
            line_width=0
        )

    for median in quintile_medians:
        fig.add_shape(
            type="line",
            x0=median,
            x1=median,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="black", width=1, dash="dash")
        )

    fig.update_layout(
        title="Income Distribution with KDE and Quintiles",
        xaxis_title="Income",
        yaxis=dict(title="Density", showticklabels=False),
        showlegend=False,
        hovermode="x unified",
    )

    return fig

# income hist helper function

def build_income_distplot(year):

    csv_path = os.path.join(csv_dir, 'gamma_resampling.csv')
    df = pd.read_csv(csv_path)

    df_year = df[df['Year'] == year]
    incomes = df_year['Income Sample'].sort_values()

    q = incomes.quantile([0.2, 0.4, 0.6, 0.8])
    quintile_edges = [incomes.min()] + q.tolist() + [incomes.max()]
    quintile_medians = [
        incomes[(incomes >= quintile_edges[i]) & (incomes < quintile_edges[i+1])].median()
        for i in range(5)
    ]
    bin_size = incomes.max() / 50

    fig = ff.create_distplot(
        [incomes],
        group_labels=[str(year)],
        bin_size=bin_size,
        curve_type='kde',
        show_hist=True,
        colors=['#888'],
        show_rug=False,
    )

    # Add colored quintile rectangles
    colors = ['#FFDDC1', '#FFABAB', '#a0ffc3', '#D5AAFF', '#A0C4FF']
    for i in range(5):
        fig.add_shape(
            type="rect",
            x0=quintile_edges[i],
            x1=quintile_edges[i+1],
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            fillcolor=colors[i],
            opacity=0.8,
            layer="below",
            line_width=0
        )

    # Add median lines
    for median in quintile_medians:
        fig.add_shape(
            type="line",
            x0=median,
            x1=median,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="black", width=1, dash="dash")
        )

    fig.update_layout(
        title=f"Income Distribution Resampling — {year}",
        xaxis_title="Income Sample",
        yaxis=dict(title="Density", showticklabels=False),
        template="plotly_white",
        showlegend=False,
        hovermode="x unified"
    )

    return fig

def income_distplot_1940():
    return build_income_distplot(1940)

def income_distplot_1950():
    return build_income_distplot(1950)

def income_distplot_1960():
    return build_income_distplot(1960)

def income_distplot_1970():
    return build_income_distplot(1970)

def income_distplot_1980():
    return build_income_distplot(1980)

def income_distplot_1990():
    return build_income_distplot(1990)

def income_distplot_2000():
    return build_income_distplot(2000)

def income_distplot_2010():
    return build_income_distplot(2010)

def income_distplot_2020():
    return build_income_distplot(2020)

def income_distplot_tabs():
    return dbc.Tabs([
    dbc.Tab(dcc.Graph(figure=income_distplot_1940()), label="1940"),
    dbc.Tab(dcc.Graph(figure=income_distplot_1950()), label="1950"),
    dbc.Tab(dcc.Graph(figure=income_distplot_1960()), label="1960"),
    dbc.Tab(dcc.Graph(figure=income_distplot_1970()), label="1970"),
    dbc.Tab(dcc.Graph(figure=income_distplot_1980()), label="1980"),
    dbc.Tab(dcc.Graph(figure=income_distplot_1990()), label="1990"),
    dbc.Tab(dcc.Graph(figure=income_distplot_2000()), label="2000"),
    dbc.Tab(dcc.Graph(figure=income_distplot_2010()), label="2010"),
    dbc.Tab(dcc.Graph(figure=income_distplot_2020()), label="2020"),
])


def multiyear_lorenz_curve():
    csv_path = os.path.join(csv_dir, 'gamma_resampling.csv')
    df = pd.read_csv(csv_path)
    
    years_to_plot = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    
    def lorenz_curve(values):
        sorted_vals = np.sort(values)
        cumvals = np.cumsum(sorted_vals)
        total = cumvals[-1]
        lorenz = np.insert(cumvals / total, 0, 0)  # prepend 0
        x_vals = np.linspace(0, 1, len(lorenz))
        return x_vals, lorenz
    
    fig = go.Figure()
    
    for year in years_to_plot:
        incomes = df[df['Year'] == year]['Income Sample'].values
        x_lorenz, y_lorenz = lorenz_curve(incomes)
        fig.add_trace(go.Scatter(
            x=x_lorenz,
            y=y_lorenz,
            mode='lines',
            name=str(year),
            line=dict(width=2),
        ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Perfect Equality',
        line=dict(color='black', dash='dash')
    ))
    
    fig.update_layout(
        title="Lorenz Curves for Selected Years",
        xaxis_title="Cumulative Share of Population",
        yaxis_title="Cumulative Share of Income",
        legend_title="Year",
        plot_bgcolor='white',
        hovermode='x unified',
        height=900,
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    return fig