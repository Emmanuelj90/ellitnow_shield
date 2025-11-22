# ============================================================
#  MÓDULO DE LICENCIAS — Ellit Platform
#  Gestión de Suscripciones · Features · Niveles · Estado Actual
# ============================================================

import streamlit as st
from datetime import datetime

# ============================================================
# CONFIGURACIÓN DE PLANES
# ============================================================

PLANES = {
    "FREE": {
        "color": "#A3A3A3",
        "features": [
            "Acceso limitado al Cognitive Core",
            "Generación básica de documentos",
            "Sin historial",
            "Sin radar IA",
            "1 usuario",
        ],
    },
    "PRO": {
        "color": "#0048FF",
        "features": [
            "Radar IA estándar",
            "Generación multinormativa",
            "Políticas corporativas",
            "Historial SGSI",
            "2 usuarios",
        ],
    },
    "ENTERPRISE": {
        "color": "#FF0080",
        "features": [
            "Radar IA avanzado (ENS, ISO, NIST, NIS2, DORA)",
            "Motor BCP avanzado",
            "Simulador de crisis",
            "Evidencias SGSI + auditoría",
            "10 usuarios",
        ],
    },
    "PRIME": {
        "color": "#D8278A",
        "features": [
            "Alert Tree PRIME",
            "Predictive Intelligence Engine",
            "GeoRisk + Sector Intelligence",
            "Correlation Matrix PRIME",
            "Usuarios ilimitados",
        ],
    },
}


# ============================================================
# UTIL
# ============================================================

def get_current_plan():
    """
    Se toma desde session_state el plan actual del tenant.
    """
    return st.session_state.get("tenant_plan", "FREE")

def get_next_renewal():
    """
    Fecha de renovación real o placeholder.
    """
    return st.session_state.get("tenant_renewal", "2025-12-31")


# ============================================================
# MÓDULO PRINCIPAL
# ============================================================

def render_licencias_tab():

    plan_actual = get_current_plan()
    renewal = get_next_renewal()
    plan_conf = PLANES[plan_actual]

    # Encabezado
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,{plan_conf['color']} 0%, #00000020 100%);
            padding:22px; border-radius:16px; color:white;
            text-align:center; margin-bottom:20px;">
            <h2 style="margin:0;">Licencias y Suscripciones</h2>
            <p style="margin:0;opacity:0.85;">Gestión del plan y funcionalidades activas</p>
        </div>
    """, unsafe_allow_html=True)

    # ============================
    # BLOQUE 1 — Estado actual
    # ============================

    st.subheader("📌 Estado de la suscripción")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Plan actual", plan_actual)

    with col2:
        st.metric("Próxima renovación", renewal)

    st.markdown("---")

    # ============================
    # BLOQUE 2 — Features activas
    # ============================

    st.subheader("🎛 Funcionalidades activas")

    for f in plan_conf["features"]:
        st.markdown(f"- ✅ **{f}**")

    st.markdown("---")

    # ============================
    # BLOQUE 3 — Comparativa completa
    # ============================

    st.subheader("📊 Comparativa de planes")

    comp_cols = st.columns(len(PLANES))

    for i, (plan, info) in enumerate(PLANES.items()):
        with comp_cols[i]:
            st.markdown(f"""
                <div style="
                    border-radius:12px;
                    border:1px solid #E5E7EB;
                    padding:15px;
                    background-color:white;
                    box-shadow:0 2px 10px rgba(0,0,0,0.05);
                    text-align:center;">
                    <h4 style='color:{info["color"]};margin:0;'>{plan}</h4>
                </div>
            """, unsafe_allow_html=True)

            for f in info["features"]:
                st.markdown(f"- {f}")

    st.markdown("---")

    # ============================
    # BLOQUE 4 — Upgrade
    # ============================

    st.subheader("🚀 Cambiar de plan")

    nuevo_plan = st.selectbox(
        "Selecciona un plan superior",
        ["PRO", "ENTERPRISE", "PRIME"],
        index=1 if plan_actual == "FREE" else 0
    )

    if st.button("Aplicar cambio de plan"):
        if nuevo_plan == plan_actual:
            st.warning("Ya estás en este plan.")
        else:
            st.session_state["tenant_plan"] = nuevo_plan
            st.success(f"Plan actualizado a **{nuevo_plan}**.")
            st.experimental_rerun()
