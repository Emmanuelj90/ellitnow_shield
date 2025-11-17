from pathlib import Path
import streamlit.components.v1 as components

# Ruta al frontend
frontend_dir = str(Path(__file__).parent / "frontend")

# Declaración del componente real
ellitmap_component = components.declare_component(
    "ellitmap",
    path=frontend_dir
)

def show_map(data: dict, key=None):
    return ellitmap_component(data=data, key=key)
