# ==========================================================
# ELLIT COGNITIVE CORE — ENTERPRISE / CCISO ENGINE (2025)
# Compatible con OpenAI SDK v1+
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# JSON NORMALIZER (ROBUSTO)
# ==========================================================

def extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        return json.loads(match.group(0)) if match else None
    except Exception:
        return None


# ==========================================================
# CCISO RADAR ENGINE
# ==========================================================

def cciso_radar_engine(client, context: dict):
    prompt = f"""
Eres Ellit Cognitive Core — Chief Information Security Officer (CCISO).

Analiza la organización según estas dimensiones:
- Gobierno y liderazgo
- Gestión del riesgo
- Controles de seguridad
- Cumplimiento normativo (ENS, ISO 27001, NIST, DORA, TISAX)
- Continuidad y resiliencia
- Cultura de seguridad

Contexto:
{json.dumps(context, indent=2)}

Devuelve SOLO JSON con esta estructura:
{{
  "indicadores": {{
    "Gobierno": 0-100,
    "Riesgo": 0-100,
    "Controles": 0-100,
    "Cumplimiento": 0-100,
    "Resiliencia": 0-100,
    "Cultura": 0-100
  }},
  "riesgos_clave": ["..."],
  "acciones_recomendadas": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit CCISO Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1200
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# SGSI MATURITY ENGINE
# ==========================================================

def sgsi_maturity_engine(client, evidencias, controles):
    prompt = f"""
Eres un auditor SGSI senior.

Evalúa la madurez del SGSI en base a:
Evidencias:
{evidencias}

Controles:
{controles}

Devuelve SOLO JSON:
{{
  "nivel": "Inicial | Gestionado | Definido | Optimizado",
  "madurez": 0-100,
  "fortalezas": ["..."],
  "debilidades": ["..."],
  "plan_accion": ["..."]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit SGSI Auditor"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=900
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# PREDICTIVE ENGINES
# ==========================================================

def predictive_standard_engine(client, query: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine"},
            {"role": "user", "content": query}
        ],
        temperature=0.3,
        max_tokens=900
    )
    return response.choices[0].message.content.strip()


def predictive_prime_engine(client, query: str):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit PRIME Engine"},
            {"role": "user", "content": query}
        ],
        temperature=0.25,
        max_tokens=1600
    )
    return response.choices[0].message.content.strip()


# ==========================================================
# BCP ENGINE
# ==========================================================

def bcp_engine(client, data):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP & Crisis Engine"},
            {"role": "user", "content": json.dumps(data)}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content.strip()


# ==========================================================
# MAIN WRAPPER CLASS (ESTABLE)
# ==========================================================

class EllitCognitiveCore:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def analyze_radar(self, profile):
        return cciso_radar_engine(self.client, profile)

    def compute_maturity(self, evidencias, controles):
        return sgsi_maturity_engine(self.client, evidencias, controles)

    def predict_standard(self, query):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query):
        return predictive_prime_engine(self.client, query)

    def generate_bcp(self, data):
        return bcp_engine(self.client, data)
