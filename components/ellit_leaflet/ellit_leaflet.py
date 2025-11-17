import streamlit.components.v1 as components
from pathlib import Path

# Ruta al directorio del frontend (HTML/JS)
COMPONENT_DIR = Path(__file__).parent / "frontend"

# Declaramos el componente con esa ruta
ellit_leaflet = components.declare_component(
    "ellit_leaflet",
    path=str(COMPONENT_DIR)
)

def show_map(data: dict = None):
    """
    Renderiza el componente Leaflet desde el frontend.
    """
    return ellit_leaflet(data=data or {}, default={})
