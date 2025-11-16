import os
import json
import streamlit.components.v1 as components

# Ruta del frontend (index.html, script.js, style.css)
COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

# Declaración del componente
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
    Renderiza el mapa Leaflet profesional de inteligencia de amenazas.

    Parámetros:
    - threat_data: dict con estructura:
        {
            "countries": [
                {
                    "country": "España",
                    "lat": 40.4,
                    "lon": -3.7,
                    "risk": 78,
                    "cves": 43,
                    "ransomware": 12,
                    "supply_chain": 8,
                    "critical": 5
                },
                ...
            ]
        }

    - height: alto del contenedor (px)
    - key: clave única streamlit
    """

    threat_json = json.dumps(threat_data)

    return ellit_leaflet_component(
        data=threat_json,
        height=height,
        key=key
    )
