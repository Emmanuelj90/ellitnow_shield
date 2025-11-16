import os
import json
import streamlit.components.v1 as components

# Ruta al frontend
COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

# Declaración del componente (SOLO AQUÍ)
ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH
)

def ellit_leaflet_map(threat_data, height=600, key=None):
    threat_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        threatData=threat_json,
        height=height,
        key=key
    )
