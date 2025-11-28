# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
# CCISO + BCP + PREDICTIVE · BACKWARD COMPATIBLE
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
            "resumen_ejecutivo": "Evaluación preliminar.",
            "riesgos_clave": [],
            "gaps_detectados": [],
            "acciones_recomendadas": []
        }

    return parsed

# ==========================================================
# ✅ BCP ENGINES (RESTORED)
# ==========================================================
def generate_bcp_plan(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — experto ISO 22301 & ENS BCP.

Genera un plan BCP estructurado:

{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"BCP Expert Engine"},
            {"role":"user","content":prompt}
        ],
        temperature=0.25,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

def analyze_bcp_context(client, contexto):
    prompt = f"""
Eres Ellit Cognitive Core — Crisis Analyst.
Analiza el contexto:

\"\"\"{contexto}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"BCP Crisis Analyst"},
            {"role":"user","content":prompt}
        ],
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()

def analyze_bcp_scenario(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — Crisis Simulator.

Escenario:
{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"BCP Crisis Simulator"},
            {"role":"user","content":prompt}
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
            {"role":"system","content":"SGSI Auditor"},
            {"role":"user","content":prompt}
        ],
        temperature=0.2,
        max_tokens=1200
    )

    parsed = extract_json(response.choices[0].message.content)
    return parsed if parsed else {
        "nivel": "No determinado",
        "madurez": 0,
        "fortalezas": [],
        "debilidades": [],
        "plan_accion": []
    }

# ==========================================================
# ✅ WRAPPER PRINCIPAL (NO ROMPE IMPORTS)
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

    # BCP
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)

    def analyze_bcp_context(self, contexto):
        return analyze_bcp_context(self.client, contexto)

    def analyze_bcp_scenario(self, data):
        return analyze_bcp_scenario(self.client, data)

