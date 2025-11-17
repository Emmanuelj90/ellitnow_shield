from pathlib import Path
import streamlit.components.v1 as components

# Ruta absoluta correcta al frontend
FRONTEND_DIR = Path(__file__).parent / "frontend"

ellitmap_component = components.declare_component(
    "ellitmap",
    path=str(FRONTEND_DIR)
)

def show_map(data: dict, key=None):
    return ellitmap_component(data=data, key=key)
