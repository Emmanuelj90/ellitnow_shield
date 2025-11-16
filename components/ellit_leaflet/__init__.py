import os
import json
import streamlit.components.v1 as components

COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH
)

def ellit_leaflet_map(
    threat_data: dict,
    height: int = 600,
    key: str = None
):
    threat_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        threatData=threat_json,
        height=height,
        key=key
    )
