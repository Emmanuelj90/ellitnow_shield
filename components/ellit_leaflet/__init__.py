import os
import streamlit.components.v1 as components

COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "frontend")

ellit_leaflet = components.declare_component(
    "ellit_leaflet",
    path=COMPONENT_PATH
)

def show_map(threatData):
    return ellit_leaflet(threatData=threatData)
