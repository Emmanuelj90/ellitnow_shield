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



# ------------------------
# Motor: Generador BCP
# ------------------------
def generate_bcp_plan(client, data: dict):
    """
    Genera un plan completo ISO 22301 + ENS OP.BCP.
    Devuelve texto listo para PDF.
    """

    prompt = f"""
Eres Ellit Cognitive Core, experto en continuidad de negocio.

Genera un documento formal y completo de Plan de Continuidad basado en:
- ISO 22301
- ENS OP.BCP (España)
- Mejores prácticas europeas

### DATOS ###
{json.dumps(data, indent=2)}

### ESTRUCTURA QUE DEBES ENTREGAR ###
1. Introducción y contexto
2. Alcance del BCP
3. Procesos críticos
4. Análisis BIA (Impacto, RTO, RPO)
5. Infraestructura y dependencias
6. Estrategias de continuidad
7. Procedimientos de recuperación
8. Roles y responsabilidades
9. Comunicación en crisis
10. Pruebas y ejercicios
11. Mapa de riesgos
12. Conclusiones ejecutivas

Devuelve solo el documento en texto, sin JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Ellit Cognitive Core, auditor experto ISO 22301 y ENS OP.BCP."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()


# ------------------------
# Motor: Análisis cognitivo BCP
# ------------------------
def analyze_bcp_context(client, contexto: str):
    """
    Analiza un problema, riesgo o situación compleja de continuidad.
    Devuelve un análisis experto y recomendaciones.
    """

    prompt = f"""
Eres Ellit Cognitive Core, analista experto en continuidad de negocio.

Analiza el siguiente contexto crítico:
\"\"\"{contexto}\"\"\"

### Debes generar ###
- Diagnóstico experto (alto nivel)
- Riesgos asociados
- Debilidades existentes
- Impacto potencial
- Recomendaciones de mitigación
- Acciones inmediatas (0–24h)
- Acciones a 72h
- Medidas de resiliencia a largo plazo

Extensión máxima: 20 líneas.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analista experto en continuidad ISO 22301, ENS y NIS2."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=900
    )

    return response.choices[0].message.content.strip()


# ------------------------
# Motor: Simulador de Crisis
# ------------------------
def analyze_bcp_scenario(client, data: dict):
    """
    Simula un escenario de crisis y produce una narrativa completa.
    Devuelve texto normal (no JSON).
    """

    prompt = f"""
Eres Ellit Cognitive Core, simulador de crisis críticas.

Simula el siguiente escenario:
{json.dumps(data, indent=2)}

### Debe incluir ###
- Resumen del incidente
- Línea temporal (minuto 0 / 30 / 60 / 120 / 240)
- Efectos sobre procesos críticos
- Decisiones clave que debe tomar el CISO
- Impacto previsto según duración
- Estrategia óptima de continuidad
- Acciones recomendadas (prioridad A/B/C)

Debe ser detallado pero claro.
Devuelve solo texto, sin JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Ellit Cognitive Core, simulador avanzado de crisis operativas."},
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
