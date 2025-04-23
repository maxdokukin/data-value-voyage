from dash import html
import importlib.util
from pathlib import Path
import re

def load_slides(slides_dir="slides"):
    def slide_key(path: Path):
        # grab the first integer in the filename; fallback to 0
        m = re.search(r"\d+", path.stem)
        return int(m.group()) if m else 0

    slides = []
    for py_path in sorted(Path(slides_dir).glob("*.py"), key=slide_key):
        spec = importlib.util.spec_from_file_location(py_path.stem, str(py_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # assuming each module has `content`; switch to `layout` if that's what you use
        slides.append(module.layout)
    return slides


slides = load_slides("pages/landing/slides")

# Layout of the app
layout = html.Div([
    html.Link(rel='stylesheet', href='/static/css/global-styles.css'),
    html.Link(rel='stylesheet', href='/static/css/homepage-styles.css'),

    html.Div(slides, className="container-slide"),
])
