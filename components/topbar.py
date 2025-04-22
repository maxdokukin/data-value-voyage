from dash import dcc, html

def get_topbar(show_home: bool = True, overlay: bool = True):
    kind = "fixed" if overlay else "static"

    if show_home:
        home_option = html.A("🏠︎", href="/", style={"fontSize": "24px"}) # 🏠
    else:
        home_option = None

    return html.Div([

        html.Link(rel='stylesheet', href='/static/css/top-bar-styles.css'),
        html.Div(
            id="topBar",
            className=f"top-bar with-background {kind}",
            children=[
                html.Div(                       # main nav
                    id="topNav",
                    className="top-nav open",
                    children=[

                        home_option,
                        html.A("Objectives", href="/objectives"),

                        # ――― Methods dropdown (CSS‑only) ―――
                        html.Div(
                            className="dropdown",
                            children=[
                                html.A("Methods ▾",
                                       className="dropbtn"),
                                html.Div(
                                    className="dropdown-content",
                                    children=[
                                        html.A("Quantity Affordable",
                                               href="/methods/quantity-affordable"),
                                        html.A("Gini Income Inequality",
                                               href="/methods/gini"),
                                        html.A("Housing Inequality",
                                               href="/methods/housing"),
                                    ],
                                ),
                            ],
                        ),

                        html.A("Findings", href="/findings"),

                        # ――― Methods dropdown (CSS‑only) ―――
                        html.Div(
                            className="dropdown",
                            children=[
                                html.A("More ▾",
                                       className="dropbtn"),
                                html.Div(
                                    className="dropdown-content",
                                    children=[
                                        html.A("Explore Data",
                                               href="/eda"),
                                        html.A("Data Sources",
                                               href="/data-sources"),
                                        html.A("About Us",
                                               href="/about-us"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ])