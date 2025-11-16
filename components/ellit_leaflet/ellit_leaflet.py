import os
import json
import streamlit.components.v1 as components

# Ruta al frontend del componente (index.html, script.js, style.css)
COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

# Declaración REAL del componente
ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH,
)

def ellit_leaflet_map(threat_data: dict, height: int = 520, key: str | None = None):
    """
    Wrapper del componente Leaflet para usar desde Streamlit.
    Envía threatData como JSON al frontend.
    """
    threat_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        threatData=threat_json,
        height=height,
        key=key,
    )
