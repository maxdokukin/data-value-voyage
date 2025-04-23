# components/learn_more_button.py
from dash import dcc, html
from typing import Tuple, Union, Optional

def get_button(
    label: str,
    link: str,
    color: str = "#007bff",
    size: Optional[Tuple[Union[int, str], Union[int, str]]] = None
):
    """
    Returns a styled 'Learn More' button positioned top-right.

    Args:
      label: Text to display on the button.
      link:  URL or path to navigate to.
      color: Background color for the button.
      size:  Optional (width, height). Integers become px, or pass strings like '2rem'.
    """
    # base button style
    btn_style = {
        "backgroundColor": color,
        "color": "white",
        "fontWeight": "bold",
        "border": "none",
        "padding": "10px 20px",
        "borderRadius": "5px",
        "cursor": "pointer",
    }

    # apply size if provided
    if size:
        w, h = size
        btn_style["width"]  = f"{w}px" if isinstance(w, int) else w
        btn_style["height"] = f"{h}px" if isinstance(h, int) else h

    return dcc.Link(
        html.Button(label, style=btn_style),
        href=link,
        style={
            "position": "absolute",
            "top": "20px",
            "right": "20px",
            "textDecoration": "none",
        },
    )
