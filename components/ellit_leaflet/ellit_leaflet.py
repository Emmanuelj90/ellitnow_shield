import os
import streamlit as st
import streamlit.components.v1 as components
import json

COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

ellit_leaflet_component = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH
)

def ellit_leaflet_map(
    threat_data: dict,
    height: int = 600,
    key: str = "ellit_leaflet"
):
    """
    Renderiza el mapa Leaflet profesional con datos de amenazas globales.

    Parámetros:
    - threat_data: diccionario con estructura:
        {
            "countries": [
                {"name": "España", "risk": 78, "cves": 43},
                {"name": "Estados Unidos", "risk": 92, "cves": 120},
                ...
            ]
        }
    - height: alto del mapa
    - key: clave única Streamlit
    """

    data_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        threatData=data_json,
        height=height,
        key=key
    )
