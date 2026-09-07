import os

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.fetch.from_csv import fetch_final_goods_affordable
from src.visualize.analysis_vis import (
    presidents_gini_plot,
    war_gini_plot,
    recession_gini_plot,
    get_goods_prices_graph,
    get_goods_prices_graph_after_1970,
    get_affordable_goods_graph,
    get_affordable_goods_graph_no_flower_sugar_after1980,
)
from src.visualize.goods_affordable import plot_incomes_inf_final_goods
from src.visualize.goods_prices import plot_goods_prices
from src.visualize.housing_vis import (
    housing_sankey,
    income_affordability_sankey,
    housing_vs_budget_trend,
    housing_affordability_delta_trend,
)
from src.visualize.incomes import compare_income_data_sources
from src.visualize.quantity_affordable_vis import (
    create_goods_price_change_heatmap_dollar_change,
    create_goods_price_change_heatmap_percent_change,
)
from src.visualize.stats_analysis_vis import (
    build_income_distribution_pyramid,
    income_histogram_with_quintiles,
    multiyear_lorenz_curve,
    create_gini_trend_plot,
    build_income_distplot,
    build_lorenz_curve_fig,
    gamma_resampling_years,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, '..', 'data', 'csv')

GOODS_LIST = [
    'bacon', 'bread', 'butter', 'coffee', 'eggs', 'flour', 'milk',
    'pork chop', 'round steak', 'sugar', 'gas'
]
REGIONS = ['united states']
INCOME_DATA_SOURCE = 'FRED'
SALARY_INTERVAL = 'monthly'
DISTPLOT_YEARS = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]


def fig_json(fig):
    return pio.to_json(fig)


def affordability_comparison_records():
    df_1920s = fetch_final_goods_affordable(
        year_range=(1920, 1929), goods_list=GOODS_LIST, regions=REGIONS,
        income_data_source=INCOME_DATA_SOURCE, salary_interval=SALARY_INTERVAL, output_format='df'
    )
    df_2020s = fetch_final_goods_affordable(
        year_range=(2020, 2029), goods_list=GOODS_LIST, regions=REGIONS,
        income_data_source=INCOME_DATA_SOURCE, salary_interval=SALARY_INTERVAL, output_format='df'
    )
    unit_map = df_1920s.set_index('name')['good_unit'].to_dict()
    avg_1920s = df_1920s.groupby('name')['final_goods_affordable'].mean()
    avg_2020s = df_2020s.groupby('name')['final_goods_affordable'].mean()

    records = []
    for name in GOODS_LIST:
        unit = unit_map.get(name, '')
        v20 = int(round(avg_1920s.get(name, 0)))
        v21 = int(round(avg_2020s.get(name, 0)))
        delta = v21 - v20
        pct = round((delta / v20 * 100), 1) if v20 else 0
        records.append({
            'Good (Unit)': f"{name.title()} ({unit})",
            '1920s': v20,
            '2020s': v21,
            'Delta': delta,
            '% Change': pct
        })
    return sorted(records, key=lambda x: x['% Change'], reverse=True)


def gini_page_metric_figs():
    df = pd.read_csv(os.path.join(CSV_DIR, 'analysis.csv'))

    metrics_fig = go.Figure()
    metrics_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Palma Ratio"].astype(float).tolist(), mode="lines", name="Palma Ratio"))
    metrics_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Housing Affordability Delta"))
    metrics_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Productivity Gap Delta"))
    metrics_fig.update_layout(
        title="Income Inequality Metrics Over Time", xaxis_title="Year", yaxis_title="Value",
        yaxis=dict(range=[0, 6]), template="plotly_white", hovermode="x"
    )

    norm_fig = go.Figure()
    norm_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Normalized Palma Ratio"].astype(float).tolist(), mode="lines", name="Normalized Palma Ratio"))
    norm_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Normalized Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Normalized Housing Affordability Delta"))
    norm_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Normalized Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Normalized Productivity Gap Delta"))
    norm_fig.update_layout(
        title="Normalized Income Inequality Metrics", xaxis_title="Year", yaxis_title="Normalized Value",
        yaxis=dict(range=[0, 1]), template="plotly_white", showlegend=False, hovermode="x"
    )

    alpha_beta_fig = go.Figure()
    alpha_beta_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Alpha"].astype(float).tolist(), mode="lines", name="Alpha", line=dict(color="blue")))
    alpha_beta_fig.add_trace(go.Scatter(x=df["Year"].astype(str).tolist(), y=df["Beta"].astype(float).tolist(), mode="lines", name="Beta", line=dict(color="red")))
    alpha_beta_fig.update_layout(
        title="Gamma Distribution Parameters Over Time", xaxis_title="Year", yaxis_title="Parameter Value",
        yaxis=dict(range=[0, 9]), template="plotly_white", hovermode="x"
    )

    return metrics_fig, norm_fig, alpha_beta_fig


def housing_years():
    df = pd.read_csv(os.path.join(CSV_DIR, 'analysis.csv'))
    df = df[df['Year'].str.endswith('-07')]
    return sorted(df['Year'].str[:4].astype(int).unique().tolist())


@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    fig_goods = plot_goods_prices(db_path=None, year_range=(1900, 2020), goods_list=GOODS_LIST, output_format='df')
    fig_income = compare_income_data_sources(
        db_path=None, start_year=1900, end_year=2024, regions=REGIONS,
        sources=['IRS', 'BEA', 'FRED'], markers=['circle', 'x', 'cross'], output_format='df', y_scale='log'
    )
    fig_quantity = plot_incomes_inf_final_goods(
        db_path=None, year_range=(1929, 2024), goods_list=GOODS_LIST, regions=REGIONS,
        income_data_source=INCOME_DATA_SOURCE, salary_interval=SALARY_INTERVAL, output_format='df'
    )
    context = {
        "request": request,
        "goods_prices_fig_json": fig_json(fig_goods),
        "compare_income_fig_json": fig_json(fig_income),
        "quantity_affordable_fig_json": fig_json(fig_quantity),
        "comparison_records": affordability_comparison_records(),
        "income_pyramid_fig_json": fig_json(build_income_distribution_pyramid()),
        "income_histogram_fig_json": fig_json(income_histogram_with_quintiles()),
        "multiyear_lorenz_fig_json": fig_json(multiyear_lorenz_curve()),
        "gini_trend_fig_json": fig_json(create_gini_trend_plot()),
        "presidents_fig_json": fig_json(presidents_gini_plot()),
        "wartime_fig_json": fig_json(war_gini_plot()),
        "recessions_fig_json": fig_json(recession_gini_plot()),
        "housing_sankey_fig_json": fig_json(housing_sankey(2023)),
        "income_sankey_fig_json": fig_json(income_affordability_sankey(2023)),
        "housing_budget_trend_fig_json": fig_json(housing_vs_budget_trend()),
    }
    return templates.TemplateResponse(request, "pages/landing.html", context)


@router.get("/objectives", response_class=HTMLResponse)
def objectives(request: Request):
    return templates.TemplateResponse(request, "pages/objectives.html", {})


@router.get("/about-us", response_class=HTMLResponse)
def about_us(request: Request):
    return templates.TemplateResponse(request, "pages/about_us.html", {})


@router.get("/findings", response_class=HTMLResponse)
def findings(request: Request):
    context = {
        "request": request,
        "comparison_records": affordability_comparison_records(),
        "gini_trend_fig_json": fig_json(create_gini_trend_plot()),
        "housing_sankey_fig_json": fig_json(housing_sankey(2023)),
        "housing_budget_trend_fig_json": fig_json(housing_vs_budget_trend()),
    }
    return templates.TemplateResponse(request, "pages/findings.html", context)


@router.get("/methods/quantity-affordable", response_class=HTMLResponse)
def quantity_affordable(request: Request):
    fig_goods = plot_goods_prices(db_path=None, year_range=(1900, 2020), goods_list=GOODS_LIST, output_format='df')
    fig_income = compare_income_data_sources(
        db_path=None, start_year=1900, end_year=2024, regions=REGIONS,
        sources=['IRS', 'BEA', 'FRED'], markers=['circle', 'x', 'cross'], output_format='df', y_scale='log'
    )
    fig_quantity = plot_incomes_inf_final_goods(
        db_path=None, year_range=(1900, 2020), goods_list=GOODS_LIST, regions=REGIONS,
        income_data_source=INCOME_DATA_SOURCE, salary_interval=SALARY_INTERVAL, output_format='df'
    )
    context = {
        "request": request,
        "goods_prices_fig_json": fig_json(fig_goods),
        "compare_income_fig_json": fig_json(fig_income),
        "quantity_affordable_fig_json": fig_json(fig_quantity),
        "comparison_records": affordability_comparison_records(),
    }
    return templates.TemplateResponse(request, "pages/methods/quantity_affordable.html", context)


@router.get("/methods/gini", response_class=HTMLResponse)
def gini(request: Request):
    years = gamma_resampling_years()
    min_year, max_year = min(years), max(years)
    metrics_fig, norm_fig, alpha_beta_fig = gini_page_metric_figs()
    distplot_figs_json = {year: fig_json(build_income_distplot(year)) for year in DISTPLOT_YEARS}

    context = {
        "request": request,
        "gini_trend_fig_json": fig_json(create_gini_trend_plot()),
        "min_year": min_year,
        "max_year": max_year,
        "lorenz_curve_fig_json": fig_json(build_lorenz_curve_fig(min_year)),
        "metrics_fig_json": fig_json(metrics_fig),
        "norm_fig_json": fig_json(norm_fig),
        "alpha_beta_fig_json": fig_json(alpha_beta_fig),
        "income_pyramid_fig_json": fig_json(build_income_distribution_pyramid()),
        "income_histogram_fig_json": fig_json(income_histogram_with_quintiles()),
        "distplot_years": DISTPLOT_YEARS,
        "distplot_figs_json": distplot_figs_json,
        "multiyear_lorenz_fig_json": fig_json(multiyear_lorenz_curve()),
        "presidents_fig_json": fig_json(presidents_gini_plot()),
        "wartime_fig_json": fig_json(war_gini_plot()),
        "recessions_fig_json": fig_json(recession_gini_plot()),
    }
    return templates.TemplateResponse(request, "pages/methods/gini.html", context)


@router.get("/methods/housing", response_class=HTMLResponse)
def housing(request: Request):
    years = housing_years()
    default_year = 2023 if 2023 in years else years[-1]
    context = {
        "request": request,
        "years": years,
        "default_year": default_year,
        "housing_sankey_fig_json": fig_json(housing_sankey(default_year)),
        "income_sankey_fig_json": fig_json(income_affordability_sankey(default_year)),
        "housing_budget_trend_fig_json": fig_json(housing_vs_budget_trend()),
        "housing_affordability_delta_fig_json": fig_json(housing_affordability_delta_trend()),
    }
    return templates.TemplateResponse(request, "pages/methods/housing.html", context)


@router.get("/data-sources", response_class=HTMLResponse)
def data_sources(request: Request):
    goods_data = [
        {"Good Name": "bacon", "Good Unit": "lb", "1900": "0.14", "1950": "0.64", "2000": "3.03", "2020": "5.58"},
        {"Good Name": "bread", "Good Unit": "lb", "1900": "...", "1950": "0.14", "2000": "0.93", "2020": "1.45"},
        {"Good Name": "butter", "Good Unit": "lb", "1900": "0.26", "1950": "0.73", "2000": "2.52", "2020": "..."},
        {"Good Name": "coffee", "Good Unit": "lb", "1900": "...", "1950": "0.79", "2000": "3.40", "2020": "4.40"},
        {"Good Name": "eggs", "Good Unit": "dozen", "1900": "0.21", "1950": "0.60", "2000": "0.91", "2020": "1.51"},
        {"Good Name": "flour", "Good Unit": "lb", "1900": "0.03", "1950": "0.10", "2000": "0.29", "2020": "0.41"},
        {"Good Name": "gas", "Good Unit": "gallon", "1900": "...", "1950": "0.27", "2000": "1.52", "2020": "2.25"},
        {"Good Name": "milk", "Good Unit": "1/2 gal", "1900": "0.14", "1950": "0.41", "2000": "2.78", "2020": "3.32"},
        {"Good Name": "pork chop", "Good Unit": "lb", "1900": "0.12", "1950": "0.75", "2000": "3.37", "2020": "4.12"},
        {"Good Name": "round steak", "Good Unit": "lb", "1900": "0.13", "1950": "0.94", "2000": "3.24", "2020": "6.53"},
        {"Good Name": "sugar", "Good Unit": "lb", "1900": "0.06", "1950": "0.10", "2000": "0.42", "2020": "0.63"},
    ]
    housing_table = [
        {"Housing": "Average Cost of Housing", "Interest Rates": "1913-2024", "Year": "1913 - 2024"}
    ]
    income_table = [
        {"Source": "Quarterly Journal of Economics: IRS Income", "Year": "1913 - 1998"},
        {"Source": "Bureau of Economic Analysis (BEA)", "Year": "1929 - 2024"},
        {"Source": "Federal Reserve Data", "Year": "1929 - 2024"},
    ]
    context = {
        "request": request,
        "goods_data": goods_data,
        "housing_table": housing_table,
        "income_table": income_table,
    }
    return templates.TemplateResponse(request, "pages/data_sources.html", context)


@router.get("/eda", response_class=HTMLResponse)
def eda(request: Request):
    context = {
        "request": request,
        "price_change_percent_fig_json": fig_json(create_goods_price_change_heatmap_percent_change()),
        "price_change_dollar_fig_json": fig_json(create_goods_price_change_heatmap_dollar_change()),
        "presidents_fig_json": fig_json(presidents_gini_plot()),
        "wartime_fig_json": fig_json(war_gini_plot()),
        "recessions_fig_json": fig_json(recession_gini_plot()),
        "price_trends_fig_json": fig_json(get_goods_prices_graph()),
        "price_trends_after_1970_fig_json": fig_json(get_goods_prices_graph_after_1970()),
        "affordable_goods_fig_json": fig_json(get_affordable_goods_graph()),
        "affordable_goods_no_flower_sugar_fig_json": fig_json(get_affordable_goods_graph_no_flower_sugar_after1980()),
    }
    return templates.TemplateResponse(request, "pages/eda.html", context)
