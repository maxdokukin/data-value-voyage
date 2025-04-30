import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import numpy as np
from components.topbar import get_topbar

from pages.vis.stats_analysis_vis import build_income_distribution_pyramid, income_histogram_with_quintiles, income_distplot_tabs, multiyear_lorenz_curve
from pages.vis.analysis_vis import gini_eda_tabs
# from src.fetch.from_gcloud import 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

############################################
############# Graph Call Backs #############
############################################

####### Gini Coefficient and Lorenz Curve #######
def fetch_gini_samples():
    csv_path = os.path.join(csv_dir, 'gamma_resampling.csv')
    return pd.read_csv(csv_path)

gini_df = fetch_gini_samples()
available_years = sorted(gini_df["Year"].unique())

@callback(
    Output("lorenz-curve-plot", "figure"),
    Input("year-slider", "value")
)
def update_lorenz_plot(selected_year):
    df = fetch_gini_samples()
    incomes = df[df["Year"] == selected_year]["Income Sample"].sort_values().values

    if len(incomes) == 0:
        return px.line(title="No data available for selected year.")

    cumulative_income = np.cumsum(incomes)
    cumulative_income = np.insert(cumulative_income, 0, 0)
    cumulative_income = cumulative_income / cumulative_income[-1]
    population_share = np.linspace(0, 1, len(cumulative_income))

    equality_x = [0, 1]
    equality_y = [0, 1]
    fill_x = list(population_share) + equality_x[::-1]
    fill_y = list(cumulative_income) + equality_y[::-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill="toself", fillcolor="rgba(255, 0, 0, 0.2)",
                             line=dict(color="rgba(255,255,255,0)"), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=population_share.tolist(), y=cumulative_income.tolist(), mode="lines", name="Lorenz Curve",
                             line=dict(color="blue", width=2)))
    fig.add_trace(go.Scatter(x=equality_x, y=equality_y, mode="lines", name="Line of Equality",
                             line=dict(dash="dash", color="gray")))

    gini = 1 - 2 * np.trapz(cumulative_income, population_share)

    fig.update_layout(
        title=f"Lorenz Curve - {selected_year} — Gini Coefficient: {gini:.4f}",
        xaxis_title="Cumulative Population",
        yaxis_title="Cumulative Income",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        showlegend=True,
        hovermode="x",

    )

    return fig

######### Gini Coefficient Over Time #########
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

gini_trend_fig.update_layout(
    title="Gini Coefficient (inequality coefficient) Over Time",
    xaxis_title="Year",
    yaxis_title="Gini Coefficient",
    xaxis=dict(
        tickangle=50
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
)

######## Income Inequality Metrics ########
def fetch_analysis_metrics():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

def fetch_normalized_analysis_metrics():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

analysis_df = fetch_analysis_metrics()
metrics_fig = go.Figure()
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Palma Ratio"].astype(float).tolist(), mode="lines", name="Palma Ratio"))
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Housing Affordability Delta"))
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Productivity Gap Delta"))
metrics_fig.update_layout(
    title="Income Inequality Metrics Over Time",
    xaxis_title="Year",
    yaxis_title="Value",
    yaxis=dict(range=[0, 6]),
    template="plotly_white",
    hovermode="x"
)

normalized_df = fetch_normalized_analysis_metrics()
norm_fig = go.Figure()
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Palma Ratio"].astype(float).tolist(), mode="lines", name="Normalized Palma Ratio"))
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Normalized Housing Affordability Delta"))
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Normalized Productivity Gap Delta"))
norm_fig.update_layout(
    title="Normalized Income Inequality Metrics",
    xaxis_title="Year",
    yaxis_title="Normalized Value",
    yaxis=dict(range=[0, 1]),
    template="plotly_white",
    showlegend=False,
    hovermode="x"
)

######### Alpha and Beta Parameters #########
def fetch_alpha_beta_trend():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

alpha_beta_df = fetch_alpha_beta_trend()

alpha_beta_fig = go.Figure()
alpha_beta_fig.add_trace(go.Scatter(
    x=alpha_beta_df["Year"].astype(str).tolist(),
    y=alpha_beta_df["Alpha"].astype(float).tolist(),
    mode="lines",
    name="Alpha",
    line=dict(color="blue")
))
alpha_beta_fig.add_trace(go.Scatter(
    x=alpha_beta_df["Year"].astype(str).tolist(),
    y=alpha_beta_df["Beta"].astype(float).tolist(),
    mode="lines",
    name="Beta",
    line=dict(color="red")
))

alpha_beta_fig.update_layout(
    title="Gamma Distribution Parameters Over Time",
    xaxis_title="Year",
    yaxis_title="Parameter Value",
    yaxis=dict(range=[0, 9]),
    template="plotly_white",
    hovermode="x"
)


############################################
################# Layout ###################
############################################


layout = dbc.Container(fluid=True, children=[
    get_topbar(current_path="/methods/gini", overlay=False),

    # Section: Header / Introduction
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col(html.H2("Understanding Income Inequality Through Statistical Modeling"), width=11),
        dbc.Col([
            ],width=1),
        dbc.Col(html.P("This page summarizes the methodology and metrics used to quantify income inequality over time. Using the Palma Ratio, Housing Affordability Delta, and the Productivity Gap, we normalized each metric and derived Alpha and Beta parameters to simulate income distributions via a Gamma distribution. Gini coefficients and Lorenz curves offer visual and numeric validation of inequality over time."), width=10),
        dbc.Col([],width=1),
    ], className="my-4"),
    
    # Section: Lorenz Curve Interactive Plot
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            dcc.Graph(id="gini-trend-plot", figure=gini_trend_fig)
        ], width=10),
        dbc.Col([],width=1),
    ]),

    # Section: Gini Coefficients Text + Visual Pair
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Interpreting Gini Coefficients"),
            html.P("""
                The Gini coefficient summarizes income inequality on a scale from 0 (perfect equality) to 1 (maximum inequality).
                It is derived from the Lorenz Curve and provides a snapshot of income concentration across a population.
                Here we analyze Gini trends using bootstrapped income samples across time.
            """),
            dcc.Markdown("""
            ### PDF (Probability Density Function) of the Gamma Distribution

            The probability density function (PDF) of the Gamma distribution is defined as:

            $$
            f(x; \\alpha, \\beta) = \\frac{1}{\\Gamma(\\alpha) \\beta^\\alpha} x^{\\alpha - 1} e^{-x / \\beta}
            $$

            Where:
            - $$\\alpha$$ is the shape parameter  
            - $$\\beta$$ is the scale parameter  
            - $$\\Gamma(f;\\alpha,\\beta)$$ is the Gamma function
            """, mathjax=True)
        ], width=5),
        dbc.Col([
            html.H4("Lorenz Curve by Year"),
            dcc.Slider(
                id="year-slider",
                min=min(available_years),
                max=max(available_years),
                value=min(available_years),
                step=1,  # or None if your years are not continuous integers
                marks={
                    int(year): {
                        "label": str(year),
                        "style": {
                            "transform": "rotate(45deg)",
                            "font-size": "10px"
                        }
                    }
                    for year in available_years if int(year) % 5 == 0
                },
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Graph(id="lorenz-curve-plot")
        ], width=5),
        dbc.Col([],width=1),
    ], className="mb-4"),

    # Section: Expressing Income Inequality
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Expressing Income Inequality"),
            html.H5("Income Inequality Metrics"),
            html.P("""
                To help understand the purchasing power of the dollar we wanted to better understand what it means for income inequality to be expressed in a few specific metrics. 
                To model and quantify income inequality in a dynamic and interpretable way, we developed a composite framework that utilizes three parameters: 
                The Palma Ratio, along with two delta values related to Housing Affordability and Productivity. The overall goal is to express these metrics as the hyperparameters in a Gamma distribution.
            """),
            html.H5("Here's a brief summary and explanation as to why we used these parameters:"),
            html.P("✤ Palma Ratio: This is a widely accepted measure of income inequality, defined as the ratio of the income share of the top 10% to that of the bottom 40%. It is a direct expression of income concentration and wealth disparity."),
            html.P("✤ Housing Affordability Delta: This metric measures the gap between what median-income individuals can afford and the actual cost of home ownership, including mortgage payments, insurance, and property taxes. This represents how economic inequality manifests in housing access and financial pressure, particularly for middle and lower-income earners."),
            html.P("✤ Productivity-Pay Gap: This captures the divergence between labor productivity and real wage growth. It reflects structural trends in wage stagnation, capital-labor imbalance, and broader systemic inequality that may not appear immediately in direct income ratios."),
            html.P("""
                A small note about the Pay Gap Delta: The data we have only goes back to 1948, so we set pay and performance equivalent for years before 1948. 
                This ensures their values represent equal pay for equal productivity and do not skew our Alpha or Beta values. 
                We thought it was an important metric to include as it represents overall economic inequality in the US.
            """)
        ], width=10),
        dbc.Col([],width=1),
    ], className="mb-4"),

    # Section: Income Indquality Metrics Graphs
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            dcc.Graph(id="income_inequality_metrics", figure=metrics_fig)
        ], width=5),
        dbc.Col([
            dcc.Graph(id="normalized_income_inequality_metrics", figure=norm_fig)
        ], width=5),
        dbc.Col([],width=1),
    ], className="mb-4"),
    
    # Section: Alpha and Beta Parameter Visualization
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Gamma Distribution Parameters, Alpha and Beta"),
            html.P("An income distribution is always skewed like a Gamma Distribution — this has been consistent throughout history. We wanted to find out just how skewed and how spread the data should be using a bootstrap resampling method. As a result, we chose our Gamma parameters: Alpha and Beta, each designated with special weights according to their relevance."),

            html.H4("Alpha (Shape Parameter)"),
            html.H5("Represents inequality skew. Lower alpha values create more right-skewed distributions (i.e., higher inequality), while higher values create more symmetric distributions (i.e., more equitable)."),
            html.P("We weighted the inputs for Alpha as follows:"),
            html.P("✤ Palma Ratio: 50% — it directly measures inequality concentration"),
            html.P("✤ Housing Delta: 30% — reflects local volatility and financial pressure"),
            html.P("✤ Productivity Gap: 20% — reflects slow-moving but systemic divergence"),

            html.H4("Beta (Scale Parameter)"),
            html.H5("Represents the breadth or variance of the distribution. It reflects how spread out the income distribution is, with higher values indicating greater dispersion."),
            html.P("We weighted the inputs for Beta as follows:"),
            html.P("✤ Productivity Gap: 50% — systemic wage divergence creates long-term spread"),
            html.P("✤ Housing Delta: 30% — affordability shocks influence volatility"),
            html.P("✤ Palma Ratio: 20% — still relevant, but more focused on distribution extremes"),
        ], width=5),
        dbc.Col([
            dcc.Graph(id="beta-trend-plot", figure=alpha_beta_fig)
        ], width=5),
        dbc.Col([],width=1),

    ], className="mb-5"),
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Why the Gamma Distribution is a Fair Choice to Measure Income Distribution"),
            html.P("    ✤  We understood from our research that the Income Distribution is always skewed like a Gamma Distribution. This has been consistent throughout history. We wanted to find out just how skewed and how spread the data should be using a bootstrap resampling method. As a result, we chose our Gamma parameters: Alpha and Beta, each designated with special weights according to their relevance."),
            html.P("    ✤  The Gamma distribution is a continuous probability distribution that is often used to model skewed data, such as income distributions. It is defined by two parameters: shape (α) and scale (β). The shape parameter determines the skewness of the distribution, while the scale parameter determines the spread of the distribution. The Gamma distribution is flexible and can take on various shapes depending on the values of α and β, making it suitable for modeling income distributions that are typically right-skewed."),
            html.P("    ✤  We found data from the census representing the mean income for each quintile group. We then used this data to create a pyramid chart that shows the distribution of income across different quintiles. The pyramid chart is a useful way to visualize the distribution of income and to see how it has changed over time."),
        ], width=5),
        dbc.Col([
            dbc.Col([
                html.A(
                    href="https://www.ft.com/content/98ce14ee-99a6-11e5-95c7-d47aa298f769#axzz3tsfi86Qz",
                    target="_blank",
                    children=html.Img(
                        src="/static/assets/income_distribution.gif",
                        # style={"width": "100%", "display": "block", "margin": "2rem auto"}
                    )
                ),
                html.P([
                    "Source: ",
                    html.A(
                        "Financial Times",
                        href="https://www.ft.com/content/98ce14ee-99a6-11e5-95c7-d47aa298f769#axzz3tsfi86Qz",
                        target="_blank"
                    )
                ]),
            ], width=6),
        ])
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Income Distribution Pyramid"),
            dcc.Graph(id="income-distribution-pyramid", figure=build_income_distribution_pyramid())
        ], width=5),
        dbc.Col([
            html.H3("← How to Interpret the Income Distribution Pyramid"),
            html.P("Imagine we have the income distribution for all incomes from every year in our dataset, and we devided the entire distribution into 5 pieces each representing 1/5 of the total population. For each quintile group, the value represented by each bar is the mean income for that group. The pyramid chart shows how the distribution of income has changed over time, as well as the top 5% of earners represented by the top bar."),
            html.P("The histogram below is a visual representation of just one year of the Income Distribution Pyramid on the Left. The histogram is divided up into colors representing each one fifth of the income distribution, or the quintile groups. The dashed lines are the median value for each quintile group. These median values for each quintile group are the represented as the size of each bar for each year in the figure to the left."),
            dcc.Graph(id="histogram_quintile_vrec", figure=income_histogram_with_quintiles()),
            html.P("The data is sourced from the U.S. Census Bureau. More about the data can be found in our data page."),
        ], width=5),
        dbc.Col([],width=1),
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Verifying our Bootstrap Resampling Merhod Produced Accurate and Reasonable Results."),
            html.P("We used a bootstrap resampling method to generate 1000 samples of income data for each year in our dataset, and calculated the Gini coefficient for each sample."),
            html.P("But we cant just assume the resampling method will be a perfect representation of the actual data. What we can do is compare how closely each resampled quintle values fall to the actual quintile values from the census bureau data."),
            html.H4("A selecting a few years to visualize the income distribution. 1940 - 2020"),
            income_distplot_tabs(),
        ], width=10),
        dbc.Col([],width=1),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            html.H3("Insight from these disrtibutions"),
            html.P("The first thing we can derive from these income distributions is that the most recent years, after 2020 are much more accurate compared to the years from 1940 - 1980. We can clearly see the differences in shape between each distribution, caused by each of our three main parameters, Palma Ratio, Housing Affordability Delta, and Productivity / Pay gap Delta, parameters. In fact the bootstrap resampling almost perfectly aligns with true values for the most recent years, so if anything that should tell us that our Gini Coefficient for the last 2-3 decades is a fair estimate based on our statistical model we developed."),
        ], width=10),
        dbc.Col([],width=1),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([],width=2),
        dbc.Col([
            dcc.Graph(id="multiyear-lorenz-curve", figure=multiyear_lorenz_curve())
        ], width = 8),
        dbc.Col([],width=2)
    ]),

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
])

exprort_layout = layout