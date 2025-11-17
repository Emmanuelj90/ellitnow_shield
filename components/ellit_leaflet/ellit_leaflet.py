import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json

# ==========================================================
# DECLARACIÓN DEL COMPONENTE ELLIT MAP
# ==========================================================

# Ruta a la carpeta donde está index.html
_component_path = Path(__file__).parent / "frontend"

ellit_map_component = components.declare_component(
    name="ellitmap",      # nombre interno del componente
    path=str(_component_path)   # carpeta frontend
)

# ==========================================================
# FUNCIÓN PARA MOSTRAR EL MAPA (ÚNICA)
# ==========================================================
def show_map(data: dict, key: str = None):
    """
    Envía datos JSON al componente frontend.
    """
    return ellit_map_component(
        data=data,
        key=key
    )
