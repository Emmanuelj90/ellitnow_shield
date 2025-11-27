# ============================================================
#   MÓDULO RADAR IA — ELLIT COGNITIVE CORE (Workflow estable)
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
from math import pi


# ============================================================
# HELPERS DE ESTADO
# ============================================================

def ensure_radar_state():
    """
    Garantiza que la estructura de estado del Radar existe
    y está alineada con lo que haya ya en sesión.
    """
    stage = st.session_state.get("radar_stage", {}) or {}

    stage.setdefault("profile_ready", "radar_profile" in st.session_state)
    stage.setdefault("analysis_ready", "radar_data" in st.session_state)
    stage.setdefault("maturity_ready", "radar_maturity" in st.session_state)

    st.session_state["radar_stage"] = stage


def get_indicadores():
    """
    Devuelve un diccionario de indicadores, aunque no exista el radar.
    Sirve para mostrar KPIs sin romper nada.
    """
    radar = st.session_state.get("radar_data", {}) or {}
    indicadores = radar.get("indicadores", {}) or {}

    # Defaults elegantes si todavía no hay análisis
    defaults = {
        "Nivel de Protección": 99.8,
        "Cumplimiento Normativo": 92,
        "Resiliencia BCP": 88,
        "Cultura de Seguridad": 74,
    }

    # Mezclamos lo que venga del motor con defaults
    merged = defaults.copy()
    merged.update(indicadores)
    return merged


# ============================================================
# ESTILOS GLOBALES DEL MÓDULO
# ============================================================

st.markdown("""
<style>
.ellit-card {
    background:#FFFFFF;
    border-radius:16px;
    padding:24px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(15,23,42,0.06);
    margin-bottom:24px;
}
.ellit-title {
    font-size:20px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:4px;
}
.ellit-sub {
    font-size:13px;
    color:#64748B;
    margin-bottom:18px;
}
.ellit-kpi-card {
    background-color:#FFFFFF;
    border:1px solid #E2E8F0;
    border-radius:14px;
    padding:18px;
    text-align:center;
    box-shadow:0 3px 10px rgba(15,23,42,0.04);
}
.ellit-kpi-value {
    font-size:28px;
    font-weight:800;
    color:#123A6A;
}
.ellit-kpi-label {
    font-size:12px;
    font-weight:600;
    color:#6B7280;
    margin-top:4px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# BLOQUE 1 — PERFIL DE LA ORGANIZACIÓN (PASO 1)
# ============================================================

def render_radar_profile():
    ensure_radar_state()

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>🧩 Perfil de la organización</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Define el contexto sobre el que Ellit ejecutará el Radar IA.</div>",
        unsafe_allow_html=True
    )

    profile = st.session_state.get("radar_profile", {})

    c1, c2, c3 = st.columns(3)
    with c1:
        org = st.text_input("Nombre de la organización", profile.get("organizacion", ""))
    with c2:
        sector = st.selectbox(
            "Sector",
            [
                "Banca y Finanzas", "Seguros", "Salud y Farmacéutica",
                "Tecnología e I+D", "Energía", "Educación", "Retail",
                "Industrial", "Defensa", "Sector Público", "Startup", "Otro"
            ],
            index=(
                [
                    "Banca y Finanzas", "Seguros", "Salud y Farmacéutica",
                    "Tecnología e I+D", "Energía", "Educación", "Retail",
                    "Industrial", "Defensa", "Sector Público", "Startup", "Otro"
                ].index(profile.get("sector"))
                if profile.get("sector") in [
                    "Banca y Finanzas", "Seguros", "Salud y Farmacéutica",
                    "Tecnología e I+D", "Energía", "Educación", "Retail",
                    "Industrial", "Defensa", "Sector Público", "Startup", "Otro"
                ]
                else 0
            )
        )
    with c3:
        nivel_ens = st.selectbox(
            "Nivel ENS actual",
            ["No aplica", "Básico", "Medio", "Alto"],
            index=(
                ["No aplica", "Básico", "Medio", "Alto"].index(profile.get("nivel_ens"))
                if profile.get("nivel_ens") in ["No aplica", "Básico", "Medio", "Alto"]
                else 0
            )
        )

    c4, c5, c6 = st.columns(3)
    with c4:
        tamano = st.selectbox(
            "Tamaño",
            ["Pequeña", "Mediana", "Grande", "Multinacional"],
            index=(
                ["Pequeña", "Mediana", "Grande", "Multinacional"].index(profile.get("tamano"))
                if profile.get("tamano") in ["Pequeña", "Mediana", "Grande", "Multinacional"]
                else 0
            )
        )
    with c5:
        region = st.text_input("Región / País principal", profile.get("region", ""))
    with c6:
        responsable = st.text_input("CISO / Responsable de seguridad", profile.get("responsable", ""))

    riesgos = st.text_area("Riesgos principales detectados", profile.get("riesgos_detectados", ""))
    certificaciones = st.text_area("Certificaciones y marcos aplicables", profile.get("certificaciones", ""))

    if st.button("Guardar perfil organizacional", type="primary"):
        if not org:
            st.error("El nombre de la organización es obligatorio.")
        else:
            st.session_state["radar_profile"] = {
                "organizacion": org,
                "sector": sector,
                "nivel_ens": nivel_ens,
                "tamano": tamano,
                "region": region,
                "responsable": responsable,
                "riesgos_detectados": riesgos,
                "certificaciones": certificaciones,
            }
            st.session_state["radar_stage"]["profile_ready"] = True
            st.success("Perfil guardado. Ya puedes ejecutar el Radar IA.")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BLOQUE 2 — RADAR COGNITIVO (PASO 2)
# ============================================================

def render_radar_cognitivo():
    ensure_radar_state()

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>🧠 Ellit Cognitive Radar</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Ejecuta el análisis cognitivo sobre tu perfil organizacional.</div>",
        unsafe_allow_html=True
    )

    if not st.session_state["radar_stage"]["profile_ready"]:
        st.warning("Primero completa y guarda el perfil de la organización en la pestaña anterior.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Analizar con Ellit Cognitive Core", key="radar_core", type="primary"):
        profile = st.session_state.get("radar_profile", {})
        if not profile:
            st.error("No se encontró el perfil en sesión. Vuelve a guardarlo.")
        else:
            with st.spinner("Analizando contexto global y riesgos…"):
                data = st.session_state["client"].analyze_radar(profile)

            st.session_state["radar_data"] = data or {}
            st.session_state["radar_stage"]["analysis_ready"] = True
            st.success("Análisis completado. Revisa KPIs y diagnósticos en las siguientes pestañas.")

    data = st.session_state.get("radar_data")
    indicadores = (data or {}).get("indicadores", {}) if data else {}

    if indicadores:
        labels = list(indicadores.keys())
        values = list(indicadores.values())
        num_vars = len(labels)

        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color="#9D2B6B", alpha=0.25)
        ax.plot(angles, values, color="#9D2B6B", linewidth=2)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_ylim(0, 100)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)

        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BLOQUE 3 — CUADRO DE MANDO KPIs (PASO 3 / EXEC SUMMARY)
# ============================================================

def render_radar_kpis():
    ensure_radar_state()

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>📊 Cuadro de mando — KPIs de seguridad</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Visión ejecutiva de tu postura de seguridad basada en el último Radar IA.</div>",
        unsafe_allow_html=True
    )

    if not st.session_state["radar_stage"]["analysis_ready"]:
        st.info("Cuando ejecutes el Radar Cognitivo, verás aquí los KPIs actualizados.")
        indicadores = get_indicadores()  # Defaults visuales
    else:
        indicadores = get_indicadores()

    # Tarjetas
    keys = list(indicadores.keys())
    values = [indicadores[k] for k in keys]

    cols = st.columns(len(keys) if len(keys) <= 4 else 4)

    for i, k in enumerate(keys[:4]):
        v = values[i]
        with cols[i]:
            st.markdown(
                f"""
                <div class="ellit-kpi-card">
                    <div class="ellit-kpi-value">{int(float(v))}%</div>
                    <div class="ellit-kpi-label">{k}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BLOQUE 4 — MADUREZ SGSI (PASO 4)
# ============================================================

def render_radar_madurez():
    ensure_radar_state()

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>📈 Madurez SGSI</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Evalúa la madurez de tu SGSI a partir de evidencias y controles existentes.</div>",
        unsafe_allow_html=True
    )

    evidencias = st.text_area("Evidencias disponibles", st.session_state.get("radar_maturity_evidencias", ""))
    controles = st.text_area("Controles implementados", st.session_state.get("radar_maturity_controles", ""))

    if st.button("Calcular Madurez SGSI"):
        with st.spinner("Analizando madurez…"):
            result = st.session_state["client"].compute_maturity(evidencias, controles)

        if not result:
            st.error("No se pudo interpretar la respuesta del motor cognitivo.")
        else:
            st.session_state["radar_maturity"] = result
            st.session_state["radar_maturity_evidencias"] = evidencias
            st.session_state["radar_maturity_controles"] = controles
            st.session_state["radar_stage"]["maturity_ready"] = True
            st.success("Evaluación de madurez completada.")

    result = st.session_state.get("radar_maturity")
    if result:
        nivel = result.get("nivel", "-")
        valor = result.get("madurez", 0)

        st.metric("Madurez SGSI", f"{nivel} ({valor}%)")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Fortalezas")
            for f in result.get("fortalezas", []):
                st.markdown(f"- {f}")

        with c2:
            st.markdown("### Debilidades")
            for d in result.get("debilidades", []):
                st.markdown(f"- {d}")

        st.markdown("### Acciones recomendadas")
        for a in result.get("acciones_requeridas", []):
            st.markdown(f"- {a}")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BLOQUE 5 — PDF REPORT (PASO FINAL)
# ============================================================

def render_radar_pdf():
    ensure_radar_state()

    st.markdown("<div class='ellit-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ellit-title'>📄 Informe PDF del Radar IA</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='ellit-sub'>Genera un informe ejecutivo para comité, auditoría o consejo.</div>",
        unsafe_allow_html=True
    )

    radar = st.session_state.get("radar_data", {})
    profile = st.session_state.get("radar_profile", {})

    if not radar:
        st.warning("Primero ejecuta el Radar Cognitivo para generar un informe.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.button("Generar informe PDF"):
        resumen = radar.get("analisis", "")
        indicadores = radar.get("indicadores", {})

        texto = [f"Informe Radar IA — {profile.get('organizacion','')}", ""]
        texto.append("Indicadores:")
        for k, v in indicadores.items():
            try:
                texto.append(f"- {k}: {float(v):.1f}%")
            except Exception:
                texto.append(f"- {k}: {v}")

        texto.append("\nResumen ejecutivo:")
        texto.append(resumen or "No se proporcionó resumen desde el motor cognitivo.")

        contenido = "\n".join(texto)

        # Import local para evitar problemas de import circular
        try:
            from app import download_pdf_button
            download_pdf_button(
                "Informe Radar IA",
                profile.get("organizacion", ""),
                contenido,
                f"RadarIA_{profile.get('organizacion','')}.pdf"
            )
            st.success("PDF generado correctamente.")
        except Exception as e:
            st.error(f"No se pudo generar el PDF: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

