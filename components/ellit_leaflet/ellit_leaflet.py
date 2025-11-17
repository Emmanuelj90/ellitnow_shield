import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "ellit_leaflet",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def show_map(data: dict, key=None):
    return _component_func(data=data, key=key)
