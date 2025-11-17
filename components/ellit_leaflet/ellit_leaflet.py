import os
import streamlit.components.v1 as components

# Ruta absoluta hacia la carpeta "build" del componente
_component_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_component_dir, "frontend", "build")

# Carga el componente (modo producción)
ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=_build_dir
)


def ellit_leaflet_map(threat_data, height=500, key=None):
    """
    Wrapper para usar el componente desde Streamlit.
    Envía 'threat_data' al frontend.
    """
    return ellit_leaflet_component(
        threatData=threat_data,
        height=height,
        key=key
    )
