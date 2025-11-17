import streamlit.components.v1 as components
from pathlib import Path

# Path al frontend del componente
COMPONENT_DIR = Path(__file__).parent / "frontend"

ellit_leaflet = components.declare_component(
    "ellit_leaflet",
    path=str(COMPONENT_DIR)
)

def show_map(data: dict):
    """
    Renderiza el mapa Leaflet enviando datos desde Streamlit.
    """
    return ellit_leaflet(data=data, default={})
