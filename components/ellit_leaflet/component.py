from pathlib import Path
import streamlit.components.v1 as components

# Ruta al frontend
parent_path = str(Path(__file__).parent / "frontend")

# Declaramos el componente
ellitmap_component = components.declare_component("ellitmap", path=parent_path)

# Función pública
def show_map(data: dict, key=None):
    return ellitmap_component(data=data, key=key)
