# ============================================================
#   MÓDULO RADAR IA — ELLIT COGNITIVE CORE (Versión Final)
#   Estilo SaaS profesional con colores corporativos Ellit
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
from math import pi


# ============================================================
#  BLOQUE 1 — Cuadro de mando KPIs
# ============================================================

def render_radar_kpis():
    indicadores = (
        st.session_state.get("radar_data", {}).get("indicadores", {})
        if st.session_state.get("radar_data")
        else {}
    )

    disp = indicadores.get("Nivel de Protección", 99.8)
    ens = indicadores.get("Cumplimiento Normativo", 92)
    bcp = indicadores.get("Resiliencia BCP", 88)
    cultura = indicadores.get("Cultura de Seguridad", 74)

    def fmt(v):
        try:
            return f"{float(v):.0f}%"
        except:
            return str(v)

    st.markdown("""
    <style>
        .ellit-metric-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        }
        .ellit-value {
            font-size: 30px;
            font-weight: 800;
            color: #0048FF;
        }
        .ellit-label {
            font-size: 13px;
            font-weight: 600;
            color: #6B7280;
            margin-top: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"<div class='ellit-metric-card'>"
            f"<div class='ellit-value'>{fmt(disp)}</div>"
            f"<div class='ellit-label'>Disponibilidad operativa</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"<div class='ellit-metric-card'>"
            f"<div class='ellit-value'>{fmt(ens)}</div>"
            f"<div class='ellit-label'>Cumplimiento ENS</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"<div class='ellit-metric-card'>"
            f"<div class='ellit-value'>{fmt(bcp)}</div>"
            f"<div class='ellit-label'>Resiliencia BCP</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"<div class='ellit-metric-card'>"
            f"<div class='ellit-value'>{fmt(cultura)}</div>"
            f"<div class='ellit-label'>Cultura de seguridad</div>"
            f"</div>",
            unsafe_allow_html=True,
        )



# ============================================================
#  BLOQUE 2 — Perfil de la organización
# ============================================================

def render_radar_profile():
    st.markdown("## 🧩 Perfil de la organización")

    c1, c2, c3 = st.columns(3)

    with c1:
        org = st.text_input("Nombre de la organización", "Fraudfense")

    with c2:
        sector = st.selectbox("Sector", [
            "Banca y Finanzas", "Seguros", "Salud y Farmacéutica",
            "Tecnología e I+D", "Energía", "Educación", "Retail",
            "Industrial", "Defensa", "Sector Público", "Startup", "Otro"
        ])

    with c3:
        nivel_ens = st.selectbox("Nivel ENS actual", ["No aplica", "Básico", "Medio", "Alto"])

    c4, c5, c6 = st.columns(3)

    with c4:
        tamano = st.selectbox("Tamaño", ["Pequeña", "Mediana", "Grande", "Multinacional"])

    with c5:
        region = st.text_input("Región / País principal", "España")

    with c6:
        responsable = st.text_input("CISO / Responsable de seguridad", "Anónimo")

    riesgos = st.text_area("Riesgos principales detectados")
    certificaciones = st.text_area("Certificaciones y marcos aplicables")

    st.session_state["radar_profile"] = {
        "organizacion": org,
        "sector": sector,
        "nivel_ens": nivel_ens,
        "tamano": tamano,
        "region": region,
        "responsable": responsable,
        "riesgos_detectados": riesgos,
        "certificaciones": certificaciones
    }



# ============================================================
#  BLOQUE 3 — Radar Cognitivo (Radar Plot)
# ============================================================

def render_radar_cognitivo():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF0080 0%, #0048FF 100%);
        padding: 24px; border-radius: 18px; color: white;
        text-align:center; margin-bottom:20px;">
        <h2 style="margin:0;">Ellit Cognitive Radar</h2>
    </div>
    """, unsafe_allow_html=True)

    profile = st.session_state.get("radar_profile", None)
    if not profile:
        st.warning("❗ Primero completa el perfil de la organización.")
        return

    if st.button("Analizar con Ellit Cognitive Core", key="radar_core"):
        with st.spinner("Analizando…"):
            data = st.session_state["radar_data"] = st.session_state["client"].analyze_radar(profile)

        st.success("Análisis completado.")

    data = st.session_state.get("radar_data", None)
    if not data:
        return

    indicadores = data.get("indicadores", {})
    if not indicadores:
        st.error("El motor no devolvió indicadores.")
        return

    labels = list(indicadores.keys())
    values = list(indicadores.values())

    num_vars = len(labels)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.fill(angles, values, color="#FF0080", alpha=0.25)
    ax.plot(angles, values, color="#FF0080", linewidth=2)

    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_ylim(0, 100)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)

    st.pyplot(fig)



# ============================================================
#  BLOQUE 4 — Madurez SGSI
# ============================================================

def render_radar_madurez():
    st.markdown("## 📊 Evaluación de Madurez SGSI")

    evidencias = st.text_area("Evidencias disponibles")
    controles = st.text_area("Controles implementados")

    if st.button("Calcular Madurez SGSI"):
        with st.spinner("Analizando madurez…"):
            result = st.session_state["client"].compute_maturity(evidencias, controles)

        if not result:
            st.error("No se pudo interpretar la respuesta.")
            return

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



# ============================================================
#  BLOQUE 5 — Selección inteligente de normativa
# ============================================================

def render_radar_normativa_inteligente():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#FF0080 0%,#0048FF 100%);
        padding:22px; border-radius:14px; color:white; text-align:center;">
        <h3 style="margin:0;">Selección inteligente de normativa</h3>
    </div>
    """, unsafe_allow_html=True)

    perfil = st.session_state.get("radar_profile", {})
    radar = st.session_state.get("radar_data", {})

    evidencias = st.text_area("Evidencias documentales")
    controles = st.text_area("Controles implementados")

    if st.button("Ejecutar análisis inteligente"):
        with st.spinner("Procesando…"):
            result = st.session_state["client"].analyze_normativa(perfil, radar, evidencias, controles)

        st.session_state["normativa_inteligente"] = result
        st.success("Análisis completado.")

    result = st.session_state.get("normativa_inteligente", None)
    if not result:
        return

    st.markdown("### 📌 Normativa principal recomendada")
    st.success(result.get("normativa_principal", "No disponible"))

    st.markdown("### 📎 Normativas secundarias")
    for n in result.get("normativas_secundarias", []):
        st.markdown(f"- {n}")

    st.markdown("### 🗺 Roadmap 3 / 6 / 12 meses")
    for fase, tareas in result.get("roadmap", {}).items():
        with st.expander(fase):
            for t in tareas:
                st.markdown(f"- {t}")



# ============================================================
#  BLOQUE 6 — PDF Report
# ============================================================

def render_radar_pdf():
    st.markdown("## 📄 Generar informe PDF del Radar IA")

    radar = st.session_state.get("radar_data", {})
    profile = st.session_state.get("radar_profile", {})

    if not radar:
        st.warning("Primero ejecuta el Radar IA.")
        return

    if st.button("Generar PDF"):
        resumen = radar.get("analisis", "")
        indicadores = radar.get("indicadores", {})

        texto = [f"Informe Radar IA — {profile.get('organizacion','')}", ""]
        texto.append("Indicadores:")
        for k, v in indicadores.items():
            texto.append(f"- {k}: {v}%")

        texto.append("\nResumen ejecutivo:")
        texto.append(resumen)

        contenido = "\n".join(texto)


        download_pdf_button(
            "Informe Radar IA",
            profile.get("organizacion", ""),
            contenido,
            f"RadarIA_{profile.get('organizacion','')}.pdf"
        )

        st.success("PDF generado correctamente.")
