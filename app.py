import streamlit as st
from components.ellit_leaflet.component import show_map

st.title("TEST SIMPLE DEL COMPONENTE")

st.write("Si lees esto, la app NO está congelada.")

st.subheader("Test con el componente")
show_map({"msg": "hola"}, key="test1")
