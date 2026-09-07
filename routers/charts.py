import plotly.io as pio
from fastapi import APIRouter
from fastapi.responses import Response

from src.visualize.housing_vis import housing_sankey, income_affordability_sankey
from src.visualize.stats_analysis_vis import build_lorenz_curve_fig

router = APIRouter()


def fig_response(fig):
    return Response(content=pio.to_json(fig), media_type="application/json")


@router.get("/methods/gini/lorenz-curve")
def lorenz_curve(year: int):
    return fig_response(build_lorenz_curve_fig(year))


@router.get("/methods/housing/sankey")
def housing_sankey_chart(year: int):
    return fig_response(housing_sankey(year))


@router.get("/methods/housing/income-sankey")
def housing_income_sankey_chart(year: int):
    return fig_response(income_affordability_sankey(year))
