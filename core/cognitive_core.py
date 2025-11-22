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
# Este archivo es SOLO BACKEND (sin Streamlit).
# ==========================================================

import json
import re
from openai import OpenAI


# ==========================================================
#  INIT OPENAI CLIENT
# ==========================================================
def init_openai(api_key: str):
    return OpenAI(api_key=api_key)



# ==========================================================
# JSON NORMALIZER
# ==========================================================
def extract_json(text: str):
    """
    Extrae el primer bloque JSON válido incluso si viene mezclado.
    """
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        return None
    except:
        return None



# ==========================================================
# 1. RADAR IA — ENS / ISO / NIST / DORA / 22301
# ==========================================================
def analyze_radar_ia(client, context: dict):

    prompt = f"""
Eres **Ellit Cognitive Core**, motor experto en ENS, ISO 27001, NIST CSF,
DORA, ISO 22301 y seguridad corporativa.

Analiza el siguiente contexto:

{json.dumps(context, indent=2)}

### FORMATO JSON ###
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
  "analisis": "Resumen ejecutivo...",
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
            {"role":"system", "content":"Eres Ellit Cognitive Core, evaluador experto en GRC."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1500
    )

    raw = response.choices[0].message.content
    return extract_json(raw)



# ==========================================================
# 2. MOTOR DE POLÍTICAS CORPORATIVAS
# ==========================================================
def generate_policy(client, tipo: str, normativa: str, organizacion: str, detalle: int = 3):

    prompt = f"""
Eres Ellit Cognitive Core. Redacta una política corporativa completa.

### DATOS ###
Tipo: {tipo}
Normativa base: {normativa}
Organización: {organizacion}
Nivel de detalle: {detalle}

### REQUISITOS ###
- Extensión 900–1300 palabras
- Listo para auditoría
- Estilo corporativo
- Español neutro

### FORMATO ###
Devuelve SOLO el texto completo.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"Eres un generador experto de políticas ISO/ENS."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1800
    )

    return response.choices[0].message.content.strip()



# ==========================================================
# 3. BCP ENGINE — ISO 22301 + ENS
# ==========================================================
def generate_bcp_plan(client, data: dict):

    prompt = f"""
Eres Ellit Cognitive Core. Genera un plan BCP basado en:

{json.dumps(data, indent=2)}

Requisitos:
- ISO 22301 + ENS OP.BCP
- Con RTO, RPO, dependencias, impacto, estrategias
- Devolver SOLO texto
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"Experto en continuidad de negocio."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()



# ==========================================================
# 4. PREDICTIVE INTELLIGENCE ENGINE
# ==========================================================
def generate_predictive_analysis(client, data: dict):

    prompt = f"""
Eres Ellit Cognitive Core. Genera inteligencia predictiva.

Entrada:
{json.dumps(data, indent=2)}

### FORMATO JSON ###
{{
  "riesgo_sectorial": "...",
  "amenazas_emergentes": ["..."],
  "tendencias": ["..."],
  "impacto_estimado": "...",
  "recomendaciones": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"Motor predictivo avanzado para CISOs."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=900
    )

    raw = response.choices[0].message.content
    return extract_json(raw)



# ==========================================================
# 5. MOTOR DE MADUREZ SGSI
# ==========================================================
def compute_sgsi_maturity(client, evidencias: str, controles: str):

    prompt = f"""
Eres Ellit Cognitive Core, auditor de madurez SGSI.

### Evidencias ###
{evidencias}

### Controles ###
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
            {"role":"system", "content":"Auditor experto ISO/ENS/NIST."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=900
    )

    raw = response.choices[0].message.content
    return extract_json(raw)



# ==========================================================
# 🔥 CLASE PRINCIPAL — ELLIT COGNITIVE CORE WRAPPER
# ==========================================================
# Esta clase es LO QUE TU APLICACIÓN necesita en session_state["client"]
# Para poder llamar:
#   client.analyze_radar()
#   client.compute_maturity()
#   client.analyze_normativa()
# ==========================================================

class EllitCognitiveCore:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    # --- Radar IA
    def analyze_radar(self, profile):
        return analyze_radar_ia(self.client, profile)

    # --- Madurez SGSI
    def compute_maturity(self, evidencias, controles):
        return compute_sgsi_maturity(self.client, evidencias, controles)

    # --- Normativa inteligente (usa motor predictivo)
    def analyze_normativa(self, perfil, radar, evidencias, controles):
        payload = {
            "perfil": perfil,
            "radar": radar,
            "evidencias": evidencias,
            "controles": controles
        }
        return generate_predictive_analysis(self.client, payload)

    # --- Políticas
    def generate_policy(self, tipo, normativa, organizacion, detalle=3):
        return generate_policy(self.client, tipo, normativa, organizacion, detalle)

    # --- BCP
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)

    # --- Predictive Intelligence
    def predictive(self, data):
        return generate_predictive_analysis(self.client, data)


# ==========================================================
# FIN DEL ARCHIVO
# ==========================================================
