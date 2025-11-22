# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
# ==========================================================
# Este módulo contiene TODA la inteligencia del Cognitive Core:
# - Radar IA (ENS + ISO 27001 + NIST CSF + DORA + ISO 22301)
# - Motor de políticas corporativas
# - Engine de continuidad BCP
# - Predictive Intelligence Engine
# - Normalización de respuestas
# - Gestión de errores
#
# Totalmente plug & play con tu app principal.
# ==========================================================

import json
import re
from openai import OpenAI

# Cliente OpenAI (se importa desde la app con st.secrets)
def init_openai(api_key: str):
    return OpenAI(api_key=api_key)


# ==========================================================
# JSON NORMALIZER — extrae JSON incluso si el modelo devuelve texto mezclado
# ==========================================================
def extract_json(text: str):
    """
    Extrae el primer bloque JSON válido dentro de una respuesta.
    """
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        return None
    except Exception:
        return None


# ==========================================================
# 1. RADAR IA — MADUREZ ENS/ISO/NIST/DORA/22301
# ==========================================================
def analyze_radar_ia(client, context: dict):
    """
    Analiza madurez organizacional ENS/ISO/NIST/DORA para Radar IA.
    Devuelve JSON compatible con tu app.
    """

    prompt = f"""
Eres **Ellit Cognitive Core**, motor experto en ENS, ISO 27001, NIST CSF, DORA,
ISO 22301, SGSI y marcos europeos de seguridad.

Analiza el siguiente contexto organizacional y genera un informe técnico completo:

### CONTEXTO ###
{json.dumps(context, indent=2)}

### FORMATO DE RESPUESTA (JSON ESTRICTO) ###
{{
  "indicadores": {{
    "Madurez SGSI": 0-100,
    "Nivel de Protección": 0-100,
    "Cumplimiento Normativo": 0-100,
    "Probabilidad de Materialización": 0-100,
    "Resiliencia BCP": 0-100,
    "Cultura de Seguridad": 0-100,
    "Brecha ENS (%)": 0-100
  }},
  "analisis": "Resumen ejecutivo técnico con interpretación ENS/ISO/NIST/DORA.",
  "acciones": {{
    "0-3 meses": ["..."],
    "3-6 meses": ["..."],
    "6-12 meses": ["..."]
  }},
  "recomendaciones": ["..."],
  "alertas": ["..."]
}}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Ellit Cognitive Core, evaluador experto en GRC y marcos ENS/ISO/NIST."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.2,
        max_tokens = 1600
    )

    raw = response.choices[0].message.content
    data = extract_json(raw)
    return data


# ==========================================================
# 2. MOTOR DE POLÍTICAS CORPORATIVAS
# ==========================================================
def generate_policy(client, tipo: str, normativa: str, organizacion: str, detalle: int = 3):
    """
    Generador de políticas corporativas multinormativas.
    """

    prompt = f"""
Eres Ellit Cognitive Core. Redacta una política corporativa formal y completa.

### DATOS ###
- Tipo de política: {tipo}
- Normativa base: {normativa}
- Organización: {organizacion}
- Nivel de detalle: {detalle}/5

### REQUISITOS ###
- Extensión 900–1300 palabras
- Estilo corporativo y listo para auditoría
- Español neutro
- Incluir referencias explícitas a {normativa}
- Estructura:
  1. Propósito
  2. Alcance
  3. Roles y responsabilidades
  4. Principios
  5. Procedimientos detallados
  6. Cumplimiento y revisión
  7. Referencias normativas
  8. Recomendaciones del Cognitive Core

### FORMATO ###
Devuelve SOLO el texto completo, sin JSON.
    """

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "Eres un generador experto de políticas GRC multinormativas."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.35,
        max_tokens = 1800
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# 3. BCP ENGINE — CONTINUIDAD ISO 22301 + ENS OP.BCP
# ==========================================================
def generate_bcp_plan(client, data: dict):
    """
    Genera un plan de continuidad completo basado en ISO 22301 + ENS.
    """

    prompt = f"""
Eres el motor Ellit Cognitive Core. Genera un plan de continuidad
ISO 22301 + ENS OP.BCP basado en los siguientes datos:

{json.dumps(data, indent=2)}

### REQUISITOS ###
- Lenguaje corporativo
- Incluir análisis de impacto, dependencias, RTO/RPO, estrategias
- Conclusiones claras de recuperación
- Devolver SOLO el documento en texto

"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres experto en continuidad ISO 22301 y ENS."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1600
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# 4. PREDICTIVE INTELLIGENCE ENGINE
# ==========================================================
def generate_predictive_analysis(client, data: dict):
    """
    Inteligencia predictiva basada en sector, región, madurez y tendencias.
    """

    prompt = f"""
Eres Ellit Cognitive Core, motor predictivo para CISOs.

Genera un análisis predictivo a partir de:
{json.dumps(data, indent=2)}

### DEVUELVE SOLO JSON ###
{{
  "riesgo_sectorial": "...",
  "amenazas_emergentes": ["...", "..."],
  "tendencias": ["...", "..."],
  "impacto_estimado": "...",
  "recomendaciones": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un motor de inteligencia predictiva avanzada."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    raw = response.choices[0].message.content
    data = extract_json(raw)
    return data


# ==========================================================
# 5. MOTOR DE MADUREZ SGSI — ENS + ISO + NIST
# ==========================================================
def compute_sgsi_maturity(client, evidencias: str, controles: str):
    """
    Evalúa nivel de madurez del SGSI en base a:
    - ISO 27001:2022
    - ENS (actualizado 2023)
    - NIST CSF 2.0
    """

    prompt = f"""
Eres Ellit Cognitive Core, auditor de madurez SGSI.

Evalúa basándote en evidencias:

### Evidencias aportadas ###
{evidencias}

### Controles existentes ###
{controles}

### FORMATO JSON ###
{{
  "madurez": 0-100,
  "nivel": "Inicial | Gestionado | Definido | Optimizado",
  "fortalezas": ["..."],
  "debilidades": ["..."],
  "acciones_requeridas": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres auditor experto ISO/ENS/NIST."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content
    data = extract_json(raw)
    return data
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

        from app import download_pdf_button
        download_pdf_button(
            "Informe Radar IA",
            profile.get("organizacion", ""),
            contenido,
            f"RadarIA_{profile.get('organizacion','')}.pdf"
        )

        st.success("PDF generado correctamente.")


# ==========================================================
# FIN DEL MÓDULO
# ==========================================================
