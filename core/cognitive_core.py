# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
# CCISO-DRIVEN ENTERPRISE INTELLIGENCE ENGINE
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# INIT OPENAI CLIENT
# ==========================================================
def init_openai(api_key: str):
    return OpenAI(api_key=api_key)

# ==========================================================
# JSON NORMALIZER (ROBUSTO)
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
# ⭐ CCISO RADAR ENGINE (CORE)
# ==========================================================
def analyze_radar_ia(client, context: dict):
    """
    Radar IA basado en dominios CCISO.
    Devuelve SIEMPRE una estructura estable para UI Enterprise.
    """

    prompt = f"""
Eres **Ellit Cognitive Core**, motor ejecutivo basado en CCISO.

Analiza el contexto siguiente y devuelve EXCLUSIVAMENTE JSON VÁLIDO.

Contexto:
{json.dumps(context, indent=2)}

### Dominios CCISO a evaluar (obligatorio):
1. Governance & Risk
2. Security Controls
3. Security Operations & Resilience
4. Compliance & Assurance
5. Leadership & Security Culture

### Formato EXACTO de salida:
{{
  "indicadores": {{
    "Governance & Risk": 0-100,
    "Security Controls": 0-100,
    "Operations & Resilience": 0-100,
    "Compliance & Assurance": 0-100,
    "Culture & Leadership": 0-100
  }},
  "resumen_ejecutivo": "texto corto para CISO",
  "riesgos_clave": ["", "", ""],
  "gaps_detectados": ["", "", ""],
  "acciones_recomendadas": ["", "", "", "", ""]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — CCISO Radar Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15,
        max_tokens=1800,
    )

    parsed = extract_json(response.choices[0].message.content)

    # Fallback de seguridad (NUNCA rompe la UI)
    if not parsed:
        return {
            "indicadores": {
                "Governance & Risk": 50,
                "Security Controls": 50,
                "Operations & Resilience": 50,
                "Compliance & Assurance": 50,
                "Culture & Leadership": 50,
            },
            "resumen_ejecutivo": "Evaluación preliminar generada sin suficiente evidencia.",
            "riesgos_clave": [],
            "gaps_detectados": [],
            "acciones_recomendadas": []
        }

    return parsed

# ==========================================================
# ⭐ MADUREZ SGSI (GAP ANALYSIS REAL)
# ==========================================================
def compute_sgsi_maturity(client, evidencias, controles):
    prompt = f"""
Eres Ellit Cognitive Core — Auditor SGSI Senior.

Evalúa la madurez del SGSI según ISO 27001 / ENS.

Devuelve SOLO JSON válido en este formato:

{{
  "nivel": "Inicial | Gestionado | Definido | Optimizado",
  "madurez": 0-100,
  "fortalezas": ["", ""],
  "debilidades": ["", ""],
  "plan_accion": ["", "", ""]
}}

Evidencias:
{evidencias}

Controles:
{controles}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Auditor SGSI Ejecutivo"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    parsed = extract_json(response.choices[0].message.content)

    if not parsed:
        return {
            "nivel": "No determinado",
            "madurez": 0,
            "fortalezas": [],
            "debilidades": [],
            "plan_accion": []
        }

    return parsed

# ==========================================================
# ⭐ CLASE PRINCIPAL — API ESTABLE
# ==========================================================
class EllitCognitiveCore:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    # Radar CCISO
    def analyze_radar(self, profile):
        return analyze_radar_ia(self.client, profile)

    # Madurez SGSI
    def compute_maturity(self, evidencias, controles):
        return compute_sgsi_maturity(self.client, evidencias, controles)

    # Normativa inteligente
    def analyze_normativa(self, perfil, radar, evidencias, controles):
        payload = {
            "perfil": perfil,
            "radar": radar,
            "evidencias": evidencias,
            "controles": controles
        }
        return payload  # mantenemos compatibilidad

    # Políticas
    def generate_policy(self, tipo, normativa, organizacion, detalle=3):
        return generate_policy(self.client, tipo, normativa, organizacion, detalle)

    # BCP
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)
