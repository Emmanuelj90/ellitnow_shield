import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json

# ==========================================================
# DECLARACIÓN DEL COMPONENTE ELLIT MAP
# ==========================================================

# Ruta absoluta a la carpeta frontend
_component_path = Path(__file__).parent / "frontend"

ellit_map_component = components.declare_component(
    name="ellitmap",  # nombre interno del componente
    path=str(_component_path)  # carpeta donde está index.html
)

# ==========================================================
# FUNCIÓN PARA MOSTRAR EL MAPA
# ==========================================================
def show_map(data: dict, key: str = None):
    """
    Envía un diccionario JSON al componente frontend.
    """
    return ellit_map_component(
        data=data,
        key=key
    )
