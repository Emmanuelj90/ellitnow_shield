import os
import streamlit.components.v1 as components

_component_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(_component_dir, "frontend")

EllitLeaflet = components.declare_component(
    "ellit_leaflet",
    path=frontend_dir
)

def threat_map(data: dict, key: str = None):
    """
    Renderiza el mapa global de amenazas geopolíticas & ciber.
    """
    return EllitLeaflet(data=data, key=key)
