import os
import json
import streamlit.components.v1 as components

# Ruta del frontend
COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

# Declaración del componente (OBLIGATORIO aquí)
ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH
)

def ellit_leaflet_map(
    threat_data: dict,
    height: int = 600,
    key: str = None
):
    """
    Wrapper limpio para usar el componente desde la app.
    """
    data_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        data=data_json,
        height=height,
        key=key
    )
