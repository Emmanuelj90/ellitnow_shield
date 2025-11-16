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


# ==========================================================
# FIN DEL MÓDULO
# ==========================================================
