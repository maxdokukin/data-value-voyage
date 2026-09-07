import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

PAGE_ROUTES = [
    "/",
    "/objectives",
    "/methods/quantity-affordable",
    "/methods/gini",
    "/methods/housing",
    "/findings",
    "/eda",
    "/data-sources",
    "/about-us",
]


@pytest.mark.parametrize("path", PAGE_ROUTES)
def test_page_returns_200(path):
    response = client.get(path)
    assert response.status_code == 200


def test_unknown_path_returns_404():
    response = client.get("/nonexistent-page")
    assert response.status_code == 404


@pytest.mark.parametrize("path,params", [
    ("/methods/gini/lorenz-curve", {"year": 1950}),
    ("/methods/housing/sankey", {"year": 1970}),
    ("/methods/housing/income-sankey", {"year": 1970}),
])
def test_chart_endpoint_returns_plotly_json(path, params):
    response = client.get(path, params=params)
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "layout" in body
