import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Path al frontend (index.html)
_component_path = Path(__file__).parent / "frontend"

# Declarar componente con nombre único
ellit_map_component = components.declare_component(
    "ellitmap",
    path=str(Path(__file__).parent / "frontend")
)

# Función pública para usar en app.py
def show_map(data: dict, key=None):
    return ellitmap_component(data=data, key=key)
