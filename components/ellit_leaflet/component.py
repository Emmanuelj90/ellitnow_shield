import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Ruta del frontend (carpeta con index.html)
_frontend = Path(__file__).parent / "frontend"

# Registrar componente con nombre correcto
ellitmap_component = components.declare_component(
    "ellitmap",
    path=str(_frontend)
)

# Función pública
def show_map(data: dict, key=None):
    return ellitmap_component(data=data, key=key)
