import streamlit.components.v1 as components
import json
from pathlib import Path

_component_func = components.declare_component(
    "ellit_leaflet",
    path=str(Path(__file__).parent / "frontend")
)

def ellit_leaflet(data, key=None):
    return _component_func(data=json.dumps(data), key=key)

def show_map(data, key="ellit_map"):
    return ellit_leaflet(data, key=key)
