import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Ruta al frontend
_frontend = Path(__file__).parent / "frontend"

# Declaración del componente (seguro)
ellit_test_component = components.declare_component(
    "ellit_test",
    path=str(_frontend)
)

def show_map(data: dict, key=None):
    return ellit_test_component(data=data, key=key)
