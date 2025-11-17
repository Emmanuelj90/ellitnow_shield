import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Path al frontend
_component_path = Path(__file__).parent / "frontend"

# Declaración del componente
ellit_map_component = components.declare_component(
    "ellitmap",
    path=str(_component_path)
)

# Función pública que usas en app.py
def show_map(data: dict, key=None):
    return ellit_map_component(data=data, key=key)
