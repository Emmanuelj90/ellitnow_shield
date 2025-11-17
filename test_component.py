import streamlit as st
from components.ellit_leaflet.component import show_map

st.title("Test Component")

show_map({"hello": "world"}, key="test01")

st.write("Si ves esto, la app no está congelada.")
