# ============================================================
#  MÓDULO DE POLÍTICAS — Ellit Cognitive Core
#  Política única · Multinormativa · PDF · Estilo corporativo
# ============================================================

import streamlit as st
from core.utils import download_pdf_button


# ============================================================
# CONFIGURACIÓN
# ============================================================

POLITICAS = [
    "Política de Seguridad de la Información",
    "Política de Control de Accesos",
    "Política de Clasificación de la Información",
    "Política de Gestión de Incidentes",
    "Política de Continuidad de Negocio",
    "Política de Privacidad y Protección de Datos",
    "Política de Backup y Recuperación",
    "Política de Gestión de Proveedores",
    "Política de Administración de Sistemas",
    "Política de Cifrado",
]

NORMATIVAS = [
    "ISO 27001",
    "ENS",
    "NIST CSF",
    "NIS2",
    "GDPR",
    "DORA",
    "SOC 2",
    "PCI DSS"
]


# ============================================================
#   MÓDULO PRINCIPAL
# ============================================================

def render_policies_generator():

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#0048FF 0%, #FF0080 100%);
            padding:20px;border-radius:16px;color:white;text-align:center;
            margin-bottom:25px;">
            <h2 style="margin:0;font-weight:700;">Generador Multinormativo de Políticas</h2>
            <p style="margin:0;opacity:0.9;">Ellit Cognitive Core — Versión Corporativa</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # FORMULARIO
    # ---------------------------

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.selectbox("Tipo de política", POLITICAS)
        normativa = st.selectbox("Normativa principal", NORMATIVAS)

    with col2:
        organizacion = st.text_input("Nombre de la organización", "Fraudfense")
        detalle = st.slider("Nivel de detalle", 1, 5, 3)

    st.markdown("### 📝 Generar Política")

    if st.button("Generar política con Ellit Cognitive Core"):

        if not organizacion:
            st.warning("Introduce el nombre de la organización.")
            return

        with st.spinner("Generando documento corporativo…"):
            try:
                policy = st.session_state.client.generate_policy(
                    tipo,
                    normativa,
                    organizacion,
                    detalle
                )
            except Exception as e:
                st.error(f"Error: {e}")
                return

        st.success("Política generada correctamente.")

        st.markdown("### Vista previa")
        st.text_area("Contenido generado", policy, height=500)

        filename = f"Politica_{tipo.replace(' ', '_')}.pdf"
        download_pdf_button(f"Política — {tipo}", organizacion, policy, filename)

