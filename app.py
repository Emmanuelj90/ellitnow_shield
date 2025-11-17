from components.ellit_leaflet.component import show_map

st.title("Test Componente")

show_map({"test": "hola"}, key="prueba01")

st.write("Si ves esto, la app NO está congelada.")
