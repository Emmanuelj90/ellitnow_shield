import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json

# ==========================================================
# DECLARACIÓN DEL COMPONENTE
# ==========================================================

# Ruta donde está el index.html
_component_path = Path(__file__).parent / "frontend"

ellit_map_component = components.declare_component(
    "ellitmap",             # nombre interno del componente
    path=str(_component_path)  # carpeta del frontend
)

# ==========================================================
# FUNCIÓN PARA MOSTRAR EL MAPA DESDE app.py
# ==========================================================
def show_map(data: dict, key: str = None):
    """
    Llama al componente React/JS enviando un diccionario JSON.
    """
    return ellit_map_component(data=data, key=key)
