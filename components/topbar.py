from dash import dcc, html

def get_topbar():
    return html.Div([

        html.Link(rel='stylesheet', href='/static/css/top-bar-styles.css'),
        html.Div(
            id="topBar",
            className="top-bar with-background",
            children=[
                html.Div(                       # hamburger icon
                    id="menuToggle",
                    className="menu-toggle active",
                    n_clicks=0,
                    children=[html.Div(), html.Div(), html.Div()],
                ),
                html.Div(                       # main nav
                    id="topNav",
                    className="top-nav open",
                    children=[
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
                                               href="/methods/quantity_affordable"),
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