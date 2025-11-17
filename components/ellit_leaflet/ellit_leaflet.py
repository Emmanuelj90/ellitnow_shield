import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json

# Declaración CORRECTA del componente
ellit_map_component = components.declare_component(
    "ellitmap",  # 🔥 nombre único, NO igual al archivo ni carpeta
    path=str(Path(__file__).parent / "frontend")  # ruta al index.html
)

def show_map(data: dict):
    return ellit_map_component(data=data)
