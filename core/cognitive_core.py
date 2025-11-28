# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
# CCISO · BCP · PREDICTIVE · FULL BACKWARD COMPATIBLE
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# JSON NORMALIZER
# ==========================================================
def extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        return None
    except Exception:
        return None


# ==========================================================
# ⭐ CCISO RADAR ENGINE
# ==========================================================
def analyze_radar_ia(client, context: dict):

    prompt = f"""
Eres Ellit Cognitive Core basado en CCISO.

Devuelve SOLO JSON válido:

{{
  "indicadores": {{
    "Governance & Risk": 0-100,
    "Security Controls": 0-100,
    "Operations & Resilience": 0-100,
    "Compliance & Assurance": 0-100,
    "Culture & Leadership": 0-100
  }},
  "resumen_ejecutivo": "",
  "riesgos_clave": [],
  "gaps_detectados": [],
  "acciones_recomendadas": []
}}

Contexto:
{json.dumps(context, indent=2)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — CCISO Radar"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15,
        max_tokens=1600
    )

    parsed = extract_json(response.choices[0].message.content)

    if not parsed:
        return {
            "indicadores": {
                "Governance & Risk": 50,
                "Security Controls": 50,
                "Operations & Resilience": 50,
                "Compliance & Assurance": 50,
                "Culture & Leadership": 50,
            },
            "resumen_ejecutivo": "Evaluación preliminar automática.",
            "riesgos_clave": [],
            "gaps_detectados": [],
            "acciones_recomendadas": []
        }

    return parsed


# ==========================================================
# ✅ PREDICTIVE STANDARD ENGINE
# ==========================================================
def predictive_standard_engine(client, query: str):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive Standard Engine.

Consulta:
\"\"\"{query}\"\"\"

Entrega:
- Resumen ejecutivo
- Riesgos probables
- Impactos
- Recomendaciones 30 / 90 días
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine — Standard"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()


# ==========================================================
# ✅ PREDICTIVE PRIME ENGINE
# ==========================================================
def predictive_prime_engine(client, query: str, benchmark=True, alerts=True, horizon="90 días"):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive PRIME Engine.

Consulta: \"\"\"{query}\"\"\"
Benchmark: {"Sí" if benchmark else "No"}
Alertas: {"Sí" if alerts else "No"}
Horizonte: {horizon}

Entrega:
- Executive briefing
- Riesgos correlacionados
- Tendencias
- Alertas
- Recomendaciones estratégicas
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine — PRIME"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1600
    )
    return response.choices[0].message.content.strip()


# ==========================================================
# ✅ BCP ENGINES
# ==========================================================
def generate_bcp_plan(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — experto ISO 22301 & ENS BCP.
{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP Expert Engine"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

def analyze_bcp_context(client, contexto):
    prompt = f"""
Eres Ellit Cognitive Core — Crisis Analyst.
\"\"\"{contexto}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP Crisis Analyst"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()

def analyze_bcp_scenario(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — Crisis Simulator.
{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP Crisis Simulator"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content.strip()


# ==========================================================
# ✅ MADUREZ SGSI
# ==========================================================
def compute_sgsi_maturity(client, evidencias, controles):
    prompt = f"""
Eres Auditor SGSI senior.

Devuelve SOLO JSON:
{{
  "nivel": "",
  "madurez": 0,
  "fortalezas": [],
  "debilidades": [],
  "plan_accion": []
}}

Evidencias:
{evidencias}

Controles:
{controles}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "SGSI Auditor"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200
    )
    return extract_json(response.choices[0].message.content)


# ==========================================================
# ✅ CLASE PRINCIPAL (NO ROMPE NADA)
# ==========================================================
class EllitCognitiveCore:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    # Radar CCISO
    def analyze_radar(self, profile):
        return analyze_radar_ia(self.client, profile)

    # SGSI
    def compute_maturity(self, evidencias, controles):
        return compute_sgsi_maturity(self.client, evidencias, controles)

    # Predictive
    def predict_standard(self, query):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query, benchmark=True, alerts=True, horizon="90 días"):
        return predictive_prime_engine(self.client, query, benchmark, alerts, horizon)

    # BCP
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)

    def analyze_bcp_context(self, contexto):
        return analyze_bcp_context(self.client, contexto)

    def analyze_bcp_scenario(self, data):
        return analyze_bcp_scenario(self.client, data)

# ==========================================================
# 🔁 BACKWARD COMPATIBILITY — PREDICTIVE (NO TOCAR)
# ==========================================================
# Estos alias existen SOLO para no romper imports antiguos

# STANDARD
def generate_predictive_standard(client, query):
    return predictive_standard_engine(client, query)

predictive_standard = generate_predictive_standard


# PRIME
def generate_predictive_prime(client, query, benchmark=True, alerts=True, horizon="90 días"):
    return predictive_prime_engine(client, query, benchmark, alerts, horizon)

predictive_prime = generate_predictive_prime
# ==========================================================
# 🔁 ULTRA BACKWARD COMPATIBILITY LAYER (DO NOT REMOVE)
# ==========================================================
# Este bloque existe SOLO para que NUNCA se rompan imports

# ---- Predictive (Standard) ----
def generate_predictive_standard(client, query):
    return predictive_standard_engine(client, query)

def predictive_standard(client, query):
    return predictive_standard_engine(client, query)

# ---- Predictive (Prime) ----
def generate_predictive_prime(client, query, benchmark=True, alerts=True, horizon="90 días"):
    return predictive_prime_engine(client, query, benchmark, alerts, horizon)

def predictive_prime(client, query, benchmark=True, alerts=True, horizon="90 días"):
    return predictive_prime_engine(client, query, benchmark, alerts, horizon)

# ---- Normativa Inteligente (LEGACY NAME) ----
def generate_predictive_analysis(client, data):
    # Re-usa el radar como motor genérico de análisis
    return analyze_radar_ia(client, data)

# ---- Safe exports (for star imports) ----
__all__ = [
    # Radar
    "analyze_radar_ia",

    # Predictive
    "predictive_standard_engine",
    "predictive_prime_engine",
    "generate_predictive_standard",
    "generate_predictive_prime",
    "predictive_standard",
    "predictive_prime",
    "generate_predictive_analysis",

    # SGSI
    "compute_sgsi_maturity",

    # BCP
    "generate_bcp_plan",
    "analyze_bcp_context",
    "analyze_bcp_scenario",

    # Utils
    "extract_json",
    "EllitCognitiveCore",
]


