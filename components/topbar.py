from dash import dcc, html

def get_topbar(show_home: bool = True, overlay: bool = True):
    kind = "fixed" if overlay else "static"

    # ── left-hand block ────────────────────────────────────────────────
    left_block = html.Div(
        className="side-block",
        children=[
            html.A(
                html.Img(
                    src="/static/assets/home_icon.png",
                    alt="Home",
                    className="icon-home",
                ),
                href="/",
            )
        ] if show_home else []          # still reserves the space if home hidden
    )

    # ── main navigation (unchanged minus the home link) ───────────────
    nav = html.Div(
        id="topNav",
        className="top-nav open",
        children=[
            html.A("Objectives", href="/objectives"),

            # Methods dropdown
            html.Div(
                className="dropdown",
                children=[
                    html.A("Methods ▾", className="dropbtn"),
                    html.Div(
                        className="dropdown-content",
                        children=[
                            html.A("Quantity Affordable", href="/methods/quantity-affordable"),
                            html.A("Gini Income Inequality", href="/methods/gini"),
                            html.A("Housing Inequality", href="/methods/housing"),
                        ],
                    ),
                ],
            ),

            html.A("Findings", href="/findings"),

            # More dropdown
            html.Div(
                className="dropdown",
                children=[
                    html.A("More ▾", className="dropbtn"),
                    html.Div(
                        className="dropdown-content",
                        children=[
                            html.A("Explore Data", href="/eda"),
                            html.A("Data Sources", href="/data-sources"),
                            html.A("About Us", href="/about-us"),
                        ],
                    ),
                ],
            ),
        ],
    )

    # ── right-hand placeholder block ──────────────────────────────────
    right_block = html.Div(className="side-block")  # empty – just a spacer

    return html.Div(
        [
            html.Link(rel="stylesheet", href="/static/css/top-bar-styles.css"),
            html.Div(
                id="topBar",
                className=f"top-bar with-background {kind}",
                children=[left_block, nav, right_block],
            ),
        ]
    )
