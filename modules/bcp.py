# ============================================================
#  MÓDULO BCP — Ellit Cognitive Core (Híbrido A/B)
#  Generador BCP • Análisis IA Premium • Simulador de crisis • Alert Tree (PRIME)
# ============================================================

import streamlit as st
from datetime import datetime
from io import BytesIO

from core.cognitive_core import (
    generate_bcp_plan,
    analyze_bcp_context,
    analyze_bcp_scenario
)

from core.database import get_conn
from app import download_pdf_button


# ============================================================================
# UTIL
# ============================================================================
def has_enterprise():
    return st.session_state.get("tenant_enterprise", False)


def has_prime():
    return st.session_state.get("tenant_prime", False)


# ============================================================================
# 1) MÓDULO SIMPLE — GENERADOR BCP
# ============================================================================
def render_bcp_generator():

    if not has_enterprise():
        st.warning("Tu organización necesita el plan Enterprise para acceder al Generador BCP.")
        return

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#0048FF 0%, #00B4FF 100%);
            padding:18px;border-radius:14px;color:white;text-align:center;
            margin-bottom:20px;">
            <h2 style="margin:0;">Generador de Plan de Continuidad</h2>
            <p style="opacity:0.85;margin:0;">ISO 22301 + ENS OP.BCP (modo estándar)</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        org = st.text_input("Nombre de la organización")
        procesos = st.text_area("Procesos críticos")
        infraestructura = st.text_area("Infraestructura disponible")
        dependencias = st.text_area("Dependencias críticas")

    with col2:
        rto = st.slider("RTO (horas)", 1, 72, 6)
        rpo = st.slider("RPO (horas)", 0, 24, 1)
        contexto = st.text_area("Contexto adicional a analizar")

    if st.button("Generar plan BCP con Ellit Cognitive Core"):
        payload = {
            "organizacion": org,
            "procesos_criticos": procesos,
            "infraestructura": infraestructura,
            "dependencias": dependencias,
            "rto_horas": rto,
            "rpo_horas": rpo,
            "contexto_adicional": contexto,
        }

        with st.spinner("Generando plan con Ellit Cognitive Core..."):
            try:
                plan = generate_bcp_plan(st.session_state.client, payload)
                st.success("Plan generado correctamente.")
                st.text_area("Vista previa del plan", plan, height=400)

                filename = f"Plan_BCP_{org.replace(' ', '_')}.pdf"
                download_pdf_button(f"Plan BCP — {org}", org, plan, filename)

            except Exception as e:
                st.error(f"Error generando el plan: {e}")


# ============================================================================
# 2) MÓDULO PREMIUM — ANÁLISIS COGNITIVO BCP (Híbrido con diseño pro)
# ============================================================================
def render_bcp_analisis():

    if not has_enterprise():
        st.warning("Este módulo requiere licencia Enterprise.")
        return

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#D8278A 0%, #0048FF 100%);
            padding:22px;border-radius:16px;color:white;text-align:center;
            margin-bottom:25px;box-shadow:0 4px 20px rgba(0,0,0,0.25);">
            <h2 style="margin:0;font-weight:700;">Análisis Cognitivo de Continuidad</h2>
            <p style="opacity:0.85;margin:0;">Ellit Cognitive Core Premium Engine</p>
        </div>
    """, unsafe_allow_html=True)

    escenario = st.text_area(
        "Describe el contexto o problema de continuidad",
        placeholder="Ejemplo: ambos CPDs están en la misma zona sísmica..."
    )

    if st.button("Analizar con Ellit Cognitive Core"):
        if not escenario:
            st.warning("Introduce un escenario para analizar.")
            return

        with st.spinner("Analizando contexto..."):
            try:
                result = analyze_bcp_context(st.session_state.client, escenario)
            except Exception as e:
                st.error(f"Error durante el análisis: {e}")
                return

        st.success("Análisis completado.")
        st.markdown("### Resultado del análisis")
        st.info(result)


# ============================================================================
# 3) MÓDULO PREMIUM — SIMULADOR DE CRISIS (UI Pro)
# ============================================================================
def render_bcp_simulador():

    if not has_enterprise():
        st.warning("Este módulo requiere licencia Enterprise.")
        return

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#0048FF 0%, #D8278A 100%);
            padding:20px;border-radius:16px;color:white;text-align:center;
            margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.25);">
            <h2 style="margin:0;">Simulador de Crisis Operativa</h2>
            <p style="margin:0;opacity:0.85;">Motor predictivo Ellit</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        escenario = st.text_input(
            "Escenario de crisis",
            placeholder="Ej: caída total de conectividad entre CPDs"
        )
        ubicacion = st.text_input("Ubicación afectada")

    with col2:
        duracion = st.slider("Duración estimada (horas)", 1, 72, 8)
        impacto = st.select_slider("Nivel de impacto", ["Bajo", "Medio", "Alto"], value="Alto")

    if st.button("Simular crisis"):
        if not escenario:
            st.warning("Debes describir un escenario.")
            return

        payload = {
            "escenario": escenario,
            "ubicacion": ubicacion,
            "duracion": duracion,
            "impacto": impacto
        }

        with st.spinner("Simulando..."):
            try:
                sim = analyze_bcp_scenario(st.session_state.client, payload)
            except Exception:
                sim = None

        st.markdown("### Resultado de la simulación")
        if sim:
            st.success(sim)
        else:
            st.warning("No se pudo generar una simulación IA completa. Se generará una recomendación estándar.")

            estrategia = "Aplicar protocolo general de continuidad ajustado al servicio afectado."

            if "CPD" in escenario or "conectividad" in escenario.lower():
                estrategia = "Activar replicación en región secundaria + habilitar VPN temporal."
            elif "ransomware" in escenario.lower():
                estrategia = "Aislar servidores comprometidos + restaurar desde copias inmutables."
            elif "incendio" in escenario.lower() or "inundación" in escenario.lower():
                estrategia = "Mover operaciones al sitio alterno y priorizar procesos críticos."

            sim = f"""
Simulación BCP — Ellit Cognitive Core

Escenario: {escenario}
Ubicación: {ubicacion}
Duración estimada: {duracion} h
Impacto: {impacto}

Estrategia recomendada:
{estrategia}
"""

            st.info(sim)

        pdf_name = f"Simulacion_BCP_{ubicacion.replace(' ','_')}.pdf"
        download_pdf_button("Simulación de crisis BCP", st.session_state.tenant_name, sim, pdf_name)


# ============================================================================
# 4) ALERT TREE — SOLO PRIME (Premium máximo)
# ============================================================================
def render_bcp_alert_tree():

    if not has_prime():
        st.error("Tu organización necesita la licencia PRIME para acceder al Alert Tree.")
        return

    st.markdown("""
        <div style="
            background:linear-gradient(135deg,#D8278A 0%, #FF0080 100%);
            padding:22px;border-radius:16px;color:white;text-align:center;
            margin-bottom:25px;box-shadow:0 4px 25px rgba(0,0,0,0.30);">
            <h2 style="margin:0;font-weight:700;">ELLIT ALERT TREE – Crisis Communication</h2>
            <p style="margin:0;opacity:0.9;">Motor avanzado PRIME</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Generar cadena de comunicación automática")
    incidente = st.text_input("Describe el incidente crítico")
    roles = st.text_area("Roles involucrados (uno por línea)")
    canales = st.multiselect("Canales", ["Email", "SMS", "Teams", "Slack", "Teléfono"], default=["Email"])

    if st.button("Generar Alert Tree"):
        if not incidente or not roles:
            st.warning("Debes introducir incidente y roles.")
            return

        roles_list = [r.strip() for r in roles.split("\n") if r.strip()]

        tree = "⚠ ALERT TREE – Comunicación automática\n\n"
        tree += f"Incidente: {incidente}\n"
        tree += f"Canales: {', '.join(canales)}\n\n"
        for r in roles_list:
            tree += f" → Notificar a {r}\n"

        st.success(tree)

        download_pdf_button("Alert Tree", st.session_state.tenant_name, tree, "alert_tree.pdf")
