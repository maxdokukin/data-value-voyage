import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import objectives, findings
from pages.landing import landing
from pages.methods import housing, quantity_affordable, gini
from pages.more import eda, data_sources, about_us

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# # # Define the app layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", style={'width': '100%'}),
])

@callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def display_page(pathname):
    if pathname == "/":
        return landing.layout
    elif pathname == "/objectives":
        return objectives.layout
    elif pathname == "/methods/quantity-affordable":
        return quantity_affordable.layout
    elif pathname == "/methods/gini":
        return gini.layout
    elif pathname == "/methods/housing":
        return housing.layout
    elif pathname == "/findings":
        return findings.layout
    elif pathname == "/eda":
        return eda.layout
    elif pathname == "/data-sources":
        return data_sources.layout
    elif pathname == "/about-us":
        return about_us.layout
    else:
        return html.Div([
            html.H1("404: Page Not Found"),
            html.P("The page you are looking for does not exist.")
        ])

# Callback to toggle the navigation menu visibility
@app.callback(
    [Output("topNav", "className"),
     Output("topBar", "className"),
     Output("menuToggle", "className")],
    [Input("menuToggle", "n_clicks")],
    prevent_initial_call=True
)
def toggle_menu(n_clicks):
    if n_clicks % 2 == 1:
        return "top-nav", "top-bar", "menu-toggle"
    else:
        return "top-nav open", "top-bar with-background", "menu-toggle active"

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
