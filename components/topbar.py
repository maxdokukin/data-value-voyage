from dash import html

def get_topbar(current_path: str = "/", show_home: bool = True, overlay: bool = True):
    """
    Renders the top bar, highlighting (and disabling) whichever menu item
    matches current_path. No callbacks needed—just pass dash.Location.pathname.
    """
    kind = "fixed" if overlay else "static"

    # ── Home icon block ────────────────────────────────────────────────
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
        ] if show_home else []
    )

    # Determine which dropdowns should appear “active”
    methods_active = current_path.startswith("/methods")
    more_active = any(current_path.startswith(p) for p in [
        "/eda", "/data-sources", "/about-us"
    ])

    # ── Main navigation ─────────────────────────────────────────────────
    nav = html.Div(
        id="topNav",
        className="top-nav open",
        children=[
            # Objectives
            html.A(
                "Objectives",
                href="/objectives",
                className="active" if current_path == "/objectives" else None
            ),

            # Methods dropdown
            html.Div(
                className="dropdown",
                children=[
                    html.A(
                        "Methods ▾",
                        href="/methods",
                        className="dropbtn active" if methods_active else "dropbtn"
                    ),
                    html.Div(
                        className="dropdown-content",
                        children=[
                            html.A(
                                "Quantity Affordable",
                                href="/methods/quantity-affordable",
                                className="active"
                                if current_path == "/methods/quantity-affordable"
                                else None
                            ),
                            html.A(
                                "Gini Income Inequality",
                                href="/methods/gini",
                                className="active"
                                if current_path == "/methods/gini"
                                else None
                            ),
                            html.A(
                                "Housing Inequality",
                                href="/methods/housing",
                                className="active"
                                if current_path == "/methods/housing"
                                else None
                            ),
                        ],
                    ),
                ],
            ),

            # Findings
            html.A(
                "Findings",
                href="/findings",
                className="active" if current_path == "/findings" else None
            ),

            # More dropdown
            html.Div(
                className="dropdown",
                children=[
                    html.A(
                        "More ▾",
                        href="/eda",
                        className="dropbtn active" if more_active else "dropbtn"
                    ),
                    html.Div(
                        className="dropdown-content",
                        children=[
                            html.A(
                                "GitHub Repo",
                                href="https://github.com/ryanfernald/Value-Voyage",
                            ),
                            html.A(
                                "Explore Data",
                                href="/eda",
                                className="active" if current_path == "/eda" else None
                            ),
                            html.A(
                                "Data Sources",
                                href="/data-sources",
                                className="active"
                                if current_path == "/data-sources"
                                else None
                            ),
                            html.A(
                                "About Us",
                                href="/about-us",
                                className="active"
                                if current_path == "/about-us"
                                else None
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    # ── Render the bar ──────────────────────────────────────────────────
    return html.Div(
        [
            html.Link(rel="stylesheet", href="/static/css/top-bar-styles.css"),
            html.Div(
                id="topBar",
                className=f"top-bar with-background {kind}",
                children=[left_block, nav],
            ),
        ]
    )
