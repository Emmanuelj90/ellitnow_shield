# ============================================================
# RADAR IA — Ellit Cognitive Core
# Enterprise SaaS · Unified Cognitive Radar
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import json

# ============================================================
# STATE INIT (ROBUSTO · NO SE ROMPE)
# ============================================================

def ensure_radar_state():
    defaults = {
        "radar_profile": None,
        "radar_result": None,
        "radar_indicators": None,
        "radar_recommendations": None,
        "radar_maturity": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

ensure_radar_state()

# ============================================================
# GLOBAL STYLE (ENTERPRISE)
# ============================================================

st.markdown("""
<style>
.ellit-card {
    background:#FFFFFF;
    border-radius:16px;
    padding:28px;
    border:1px solid #E5E7EB;
    box-shadow:0 8px 24px rgba(0,0,0,0.06);
    margin-bottom:26px;
}
.ellit-title {
    font-size:22px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:6px;
}
.ellit-sub {
    font-size:14px;
    color:#475569;
    margin-bottom:22px;
}
.ellit-kpi {
    background:#F8FAFC;
    border-radius:12px;
    padding:18px;
    text-align:center;
    border:1px solid #E5E7EB;
}
.ellit-kpi h3 {
    margin:0;
    font-size:24px;
}
.ellit-kpi span {
    font-size:13px;
    color:#64748B;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PERFIL CONTEXTUAL (INTEGRADO EN RADAR)
# ============================================================

def _render_profile_context():
    with st.expander(
        "Contexto de la organización",
        expanded=st.session_state["radar_profile"] is None
    ):
        c1, c2, c3 = st.columns(3)
        with c1:
            org = st.text_input(
                "Organización",
                st.session_state.get("radar_profile", {}).get("organizacion", "")
            )
        with c2:
            sector = st.selectbox(
                "Sector",
                ["Banca", "Seguros", "Salud", "Tecnología",
                 "Energía", "Industrial", "Sector Público", "Otro"]
            )
        with c3:
            ens = st.selectbox("Nivel ENS", ["No aplica", "Básico", "Medio", "Alto"])

        c4, c5, c6 = st.columns(3)
        with c4:
            size = st.selectbox(
                "Tamaño", ["Pequeña", "Mediana", "Grande", "Multinacional"]
            )
        with c5:
            region = st.text_input("Región / País")
        with c6:
            owner = st.text_input("Responsable / CISO")

        riesgos = st.text_area("Riesgos principales")
        certs = st.text_area("Certificaciones / Marcos")

        if st.button("Guardar contexto"):
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
                    "certificaciones": certs,
                }
                st.success("Contexto guardado correctamente.")

# ============================================================
# RADAR COGNITIVO CENTRAL (VISTA PRINCIPAL)
# ============================================================

def render_radar_cognitivo():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-title'>Radar Cognitivo de Seguridad</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='ellit-sub'>"
        "Evaluación 360° del estado de seguridad, cumplimiento y resiliencia "
        "basada en inteligencia cognitiva."
        "</div>",
        unsafe_allow_html=True
    )

    # ---------- CONTEXTO ----------
    _render_profile_context()

    profile = st.session_state.get("radar_profile")
    if not profile:
        st.info("Completa el contexto para ejecutar el radar cognitivo.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ---------- EJECUCIÓN ----------
    if st.button("Ejecutar análisis cognitivo", type="primary"):
        with st.spinner("Ejecutando análisis cognitivo avanzado…"):
            raw = st.session_state["client"].analyze_radar(profile)

        if not raw:
            st.error("El motor cognitivo no devolvió resultados.")
            st.markdown("**Contexto enviado al motor:**")
            st.json(profile)
            st.markdown("</div>", unsafe_allow_html=True)
            return

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                st.warning("Respuesta del motor no estructurada.")
                st.text_area("Salida del motor", raw, height=280)
                st.markdown("</div>", unsafe_allow_html=True)
                return

        # Guardado único y consistente
        st.session_state["radar_result"] = raw
        st.session_state["radar_indicators"] = raw.get("indicadores", {})
        st.session_state["radar_recommendations"] = raw.get(
            "acciones_recomendadas", []
        )

        st.success("Análisis cognitivo completado.")

    # ---------- VISUALIZACIÓN ----------
    indicators = st.session_state.get("radar_indicators")
    if not indicators:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # KPIs
    st.markdown("### Indicadores clave")
    cols = st.columns(len(indicators))
    for i, (k, v) in enumerate(indicators.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div class="ellit-kpi">
                    <h3>{int(v)}%</h3>
                    <span>{k}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Radar gráfico
    labels = list(indicators.keys())
    values = list(indicators.values())

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            line_color="#7C1F5E"
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=420,
        margin=dict(l=30, r=30, t=30, b=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Recomendaciones
    st.markdown("### Recomendaciones prioritarias")
    for r in st.session_state.get("radar_recommendations", [])[:5]:
        st.markdown(f"- {r}")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# MADUREZ SGSI (MÓDULO SEPARADO)
# ============================================================

def render_radar_madurez():

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-title'>Madurez del SGSI</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='ellit-sub'>Evaluación basada en evidencias y controles reales.</div>",
        unsafe_allow_html=True
    )

    evidencias = st.text_area("Evidencias")
    controles = st.text_area("Controles")

    if st.button("Evaluar madurez SGSI"):
        with st.spinner("Analizando madurez SGSI…"):
            raw = st.session_state["client"].compute_maturity(
                evidencias, controles
            )

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                st.error("Respuesta del motor no estructurada.")
                st.text_area("Salida del motor", raw, height=260)
                st.markdown("</div>", unsafe_allow_html=True)
                return

        st.session_state["radar_maturity"] = raw

    result = st.session_state.get("radar_maturity")
    if result:
        st.metric(
            "Nivel de madurez",
            f"{result.get('nivel', '-')}"
            f" ({result.get('madurez', 0)}%)"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PDF (HOOK)
# ============================================================

def render_radar_pdf():
    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-title'>Informe ejecutivo</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.get("radar_result"):
        st.warning("Ejecuta primero el radar cognitivo.")
    else:
        st.button("Generar informe ejecutivo PDF", type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# COMPATIBILIDAD CON ROUTER (APP.PY)
# ============================================================

def render_radar_profile():
    render_radar_cognitivo()

def render_radar_kpis():
    render_radar_cognitivo()


