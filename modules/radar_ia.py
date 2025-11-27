# ============================================================
# RADAR IA — Ellit Cognitive Core
# Workflow Ejecutivo · SaaS Enterprise Grade
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
from math import pi

# ============================================================
# WORKFLOW STATE INIT
# ============================================================

if "radar_stage" not in st.session_state:
    st.session_state["radar_stage"] = {
        "profile_ready": False,
        "analysis_ready": False,
        "maturity_ready": False,
    }

# ============================================================
# GLOBAL STYLES
# ============================================================

st.markdown("""
<style>
.ellit-card {
    background:#FFFFFF;
    border-radius:16px;
    padding:26px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
    margin-bottom:24px;
}
.ellit-step {
    font-size:13px;
    letter-spacing:.12em;
    color:#64748B;
    font-weight:700;
}
.ellit-title {
    font-size:22px;
    font-weight:800;
    color:#0F172A;
}
.ellit-sub {
    font-size:14px;
    color:#475569;
    margin-top:6px;
    margin-bottom:20px;
}
.ellit-cta button {
    width:100%;
    height:46px;
    border-radius:12px;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FASE 1 — PERFIL ORGANIZACIONAL
# ============================================================

def render_radar_profile():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-step'>PASO 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Contexto de la organización</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Este perfil define cómo Ellit evalúa el riesgo y la madurez de tu organización.</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        org = st.text_input("Organización")
    with c2:
        sector = st.selectbox("Sector", [
            "Banca y Finanzas","Seguros","Salud",
            "Tecnología","Energía","Educación",
            "Industrial","Sector Público","Otro"
        ])
    with c3:
        ens = st.selectbox("Nivel ENS", ["No aplica","Básico","Medio","Alto"])

    c4, c5, c6 = st.columns(3)
    with c4:
        size = st.selectbox("Tamaño", ["Pequeña","Mediana","Grande","Multinacional"])
    with c5:
        region = st.text_input("Región")
    with c6:
        owner = st.text_input("Responsable")

    riesgos = st.text_area("Riesgos principales")
    certs = st.text_area("Certificaciones / marcos")

    if st.button("Guardar perfil organizacional", type="primary"):
        if not org:
            st.error("El nombre de la organización es obligatorio.")
        else:
            st.session_state["radar_profile"] = {
                "organizacion": org,
                "sector": sector,
                "nivel_ens": ens,
                "tamano": size,
                "region": region,
                "responsable": owner,
                "riesgos_detectados": riesgos,
                "certificaciones": certs
            }
            st.session_state["radar_stage"]["profile_ready"] = True
            st.success("Perfil guardado correctamente.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FASE 2 — RADAR COGNITIVO
# ============================================================

def render_radar_cognitivo():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-step'>PASO 2</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Evaluación cognitiva</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Ellit ejecuta un análisis cognitivo avanzado basado en tu contexto organizacional.</div>",
        unsafe_allow_html=True
    )

    if not st.session_state["radar_stage"]["profile_ready"]:
        st.warning("Completa primero el perfil organizacional.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Ejecutar análisis con Ellit AI", type="primary"):
        with st.spinner("Analizando contexto global…"):
            data = st.session_state["client"].analyze_radar(
                st.session_state["radar_profile"]
            )
            st.session_state["radar_data"] = data
            st.session_state["radar_stage"]["analysis_ready"] = True

        st.success("Análisis cognitivo completado.")

    data = st.session_state.get("radar_data")
    if data:
        indicadores = data.get("indicadores", {})
        labels = list(indicadores.keys())
        values = list(indicadores.values())

        angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color="#9D2B6B", alpha=0.25)
        ax.plot(angles, values, color="#9D2B6B", linewidth=2)
        ax.set_ylim(0,100)
        ax.set_yticks([20,40,60,80,100])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)

        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FASE 3 — KPIs + MADUREZ
# ============================================================

def render_radar_kpis():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-step'>PASO 3</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Diagnóstico ejecutivo</div>", unsafe_allow_html=True)

    if not st.session_state["radar_stage"]["analysis_ready"]:
        st.warning("Ejecuta primero el análisis cognitivo.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    indicadores = st.session_state["radar_data"]["indicadores"]

    col = st.columns(len(indicadores))
    for i, (k, v) in enumerate(indicadores.items()):
        with col[i]:
            st.metric(k, f"{int(v)}%")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FASE 4 — MADUREZ SGSI
# ============================================================

def render_radar_madurez():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-step'>PASO 4</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Madurez del SGSI</div>", unsafe_allow_html=True)

    evidencias = st.text_area("Evidencias")
    controles = st.text_area("Controles")

    if st.button("Evaluar madurez SGSI"):
        result = st.session_state["client"].compute_maturity(
            evidencias, controles
        )
        st.session_state["radar_maturity"] = result
        st.session_state["radar_stage"]["maturity_ready"] = True

    result = st.session_state.get("radar_maturity")
    if result:
        st.metric("Nivel de madurez", f"{result['nivel']} ({result['madurez']}%)")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FASE 5 — INFORME EJECUTIVO
# ============================================================

def render_radar_pdf():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-step'>PASO FINAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Informe ejecutivo</div>", unsafe_allow_html=True)

    if not st.session_state["radar_stage"]["analysis_ready"]:
        st.warning("No hay análisis disponible para documentar.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Generar informe ejecutivo PDF", type="primary"):
        st.success("Informe generado correctamente.")

    st.markdown("</div>", unsafe_allow_html=True)
