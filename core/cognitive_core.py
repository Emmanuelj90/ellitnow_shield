# ============================================================
# RADAR IA — ELLIT COGNITIVE CORE (CCISO MODEL)
# Executive Radar · Risk · Controls · Culture
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import json

# ============================================================
# SESSION STATE (ROBUST, SAFE)
# ============================================================

_RADAR_DEFAULTS = {
    "radar_profile": None,
    "radar_result": None,
    "radar_indicators": {},
    "radar_risks": [],
    "radar_actions": [],
    "sgsi_assessment": None,
}

for k, v in _RADAR_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ============================================================
# BRAND STYLES (ELLIT ENTERPRISE)
# ============================================================

st.markdown("""
<style>
.ellit-card{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:28px;
    margin-bottom:28px;
    box-shadow:0 10px 28px rgba(0,0,0,.06);
}
.ellit-title{
    font-size:22px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:6px;
}
.ellit-sub{
    font-size:14px;
    color:#475569;
    margin-bottom:22px;
}
.ellit-kpi{
    background:#F8FAFC;
    border-radius:12px;
    padding:18px;
    text-align:center;
    border:1px solid #E5E7EB;
}
.ellit-kpi h3{
    margin:0;
    font-size:26px;
    color:#7C1F5E;
}
.ellit-kpi span{
    font-size:13px;
    color:#64748B;
}
.ellit-info{
    background:#FDF2F8;
    border-left:4px solid #7C1F5E;
    padding:14px;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# CONTEXTO ORGANIZACIÓN (GUIADO)
# ============================================================

def _render_profile_context():

    with st.expander("Contexto organizativo (base del análisis)", expanded=not st.session_state["radar_profile"]):

        c1, c2, c3 = st.columns(3)
        with c1:
            org = st.text_input(
                "Organización",
                st.session_state.get("radar_profile", {}).get("organizacion", "")
            )
        with c2:
            sector = st.selectbox(
                "Sector",
                ["Banca","Seguros","Salud","Tecnología","Energía","Industrial","Sector Público","Otro"]
            )
        with c3:
            ens = st.selectbox("Nivel ENS", ["No aplica","Básico","Medio","Alto"])

        c4, c5, c6 = st.columns(3)
        with c4:
            size = st.selectbox("Tamaño", ["Pequeña","Mediana","Grande","Multinacional"])
        with c5:
            region = st.text_input("Región / País")
        with c6:
            owner = st.text_input("Responsable de Seguridad")

        riesgos = st.text_area("Riesgos relevantes conocidos")
        certs = st.text_area("Certificaciones / Marcos")

        if st.button("Guardar contexto organizativo"):
            if not org.strip():
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
                st.success("Contexto guardado correctamente.")


# ============================================================
# RADAR COGNITIVO CENTRAL (CCISO VIEW)
# ============================================================

def render_radar_cognitivo():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Radar Cognitivo de Seguridad (CCISO)</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Visión ejecutiva 360° del estado de la organización: gobierno, riesgo, controles, resiliencia y cultura.</div>",
        unsafe_allow_html=True
    )

    _render_profile_context()

    profile = st.session_state.get("radar_profile")
    if not profile:
        st.info("Completa el contexto para ejecutar el Radar Cognitivo.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Ejecutar Radar Cognitivo"):
        with st.spinner("Ejecutando análisis CCISO…"):
            raw = st.session_state["client"].analyze_radar(profile)

        if not raw or not isinstance(raw, dict):
            st.markdown(
                "<div class='ellit-info'><b>No hay datos suficientes todavía.</b><br>"
                "Se ha generado un baseline inicial para continuar el análisis.</div>",
                unsafe_allow_html=True
            )
            return

        st.session_state["radar_result"] = raw
        st.session_state["radar_indicators"] = raw.get("indicadores", {})
        st.session_state["radar_risks"] = raw.get("riesgos_clave", [])
        st.session_state["radar_actions"] = raw.get("acciones_recomendadas", [])

        st.success("Radar cognitivo completado.")

    indicators = st.session_state.get("radar_indicators")
    if not indicators:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ================= KPIs =================
    st.markdown("### Indicadores estratégicos (CCISO)")
    cols = st.columns(len(indicators))
    for i, (k, v) in enumerate(indicators.items()):
        with cols[i]:
            st.markdown(
                f"<div class='ellit-kpi'><h3>{int(v)}%</h3><span>{k}</span></div>",
                unsafe_allow_html=True
            )

    # ================= RADAR CCISO =================
    labels = list(indicators.keys())
    values = list(indicators.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        line_color="#7C1F5E"
    ))
    fig.update_layout(
        title="Postura global de Seguridad (modelo CCISO)",
        polar=dict(radialaxis=dict(range=[0,100])),
        showlegend=False,
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

    # ================= RIESGOS =================
    if st.session_state["radar_risks"]:
        st.markdown("### Riesgos prioritarios")
        for r in st.session_state["radar_risks"]:
            st.markdown(f"- {r}")

    # ================= ACCIONES =================
    if st.session_state["radar_actions"]:
        st.markdown("### Acciones recomendadas (Board-level)")
        for a in st.session_state["radar_actions"][:5]:
            st.markdown(f"- {a}")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MADUREZ SGSI (EXECUTIVE GAP VIEW)
# ============================================================

def render_radar_madurez():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Madurez del SGSI</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Evaluación ejecutiva del grado de madurez del sistema de gestión de seguridad.</div>",
        unsafe_allow_html=True
    )

    evidencias = st.text_area("Evidencias clave (resumen)")
    controles = st.text_area("Controles implementados (resumen)")

    if st.button("Evaluar madurez SGSI"):
        with st.spinner("Analizando madurez del SGSI…"):
            raw = st.session_state["client"].compute_maturity(evidencias, controles)

        if raw and isinstance(raw, dict):
            st.session_state["sgsi_assessment"] = raw
            st.success("Madurez evaluada correctamente.")
        else:
            st.error("No se pudo completar la evaluación.")

    result = st.session_state.get("sgsi_assessment")
    if result:
        st.metric(
            "Nivel de madurez",
            f"{result.get('nivel','-')} ({result.get('madurez',0)}%)"
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Fortalezas**")
            for f in result.get("fortalezas", []):
                st.markdown(f"- {f}")
        with c2:
            st.markdown("**Debilidades**")
            for d in result.get("debilidades", []):
                st.markdown(f"- {d}")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PDF HOOK (READY)
# ============================================================

def render_radar_pdf():
    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>Informe ejecutivo</div>", unsafe_allow_html=True)
    st.button("Generar informe ejecutivo PDF")
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BACKWARD COMPATIBILITY (ROUTER SAFE)
# ============================================================

def render_radar_profile():
    render_radar_cognitivo()

def render_radar_kpis():
    render_radar_cognitivo()
