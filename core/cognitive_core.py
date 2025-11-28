# ==========================================================
# ELLIT COGNITIVE CORE — CENTRAL INTELLIGENCE ENGINE (2025)
# Radar · CCISO · Predictive · GRC · BCP · Normativa
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# JSON NORMALIZER (COMPATIBILIDAD GLOBAL)
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
# PREDICTIVE — STANDARD ENGINE
# ==========================================================

def predictive_standard_engine(client, query: str):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive Standard Engine.

Consulta:
\"\"\"{query}\"\"\"

Entrega:
- Resumen ejecutivo
- 3 riesgos probables
- 3 impactos probables
- Recomendaciones a 30 días
- Recomendaciones a 90 días
- Texto claro, sin JSON
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine — Standard"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=900,
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# PREDICTIVE — PRIME ENGINE
# ==========================================================

def predictive_prime_engine(client, query: str, benchmark=True, alerts=True, horizon="12 meses"):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive PRIME Engine.

Consulta:
\"\"\"{query}\"\"\"

Benchmark sectorial: {"Sí" if benchmark else "No"}
Alertas globales: {"Sí" if alerts else "No"}
Horizonte temporal: {horizon}

Entrega:
- Executive briefing
- Riesgos correlacionados
- Tendencias emergentes
- Benchmark sectorial (si aplica)
- Alertas globales (si aplica)
- Recomendaciones estratégicas
- Texto claro, sin JSON
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine — PRIME"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1600,
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# NORMATIVA / INTELIGENCIA REGULATORIA (JSON)
# ==========================================================

def generate_predictive_analysis(client, data: dict):
    prompt = f"""
Eres Ellit Cognitive Core — Intelligence Engine.

Analiza y devuelve JSON estructurado para:
ENS, ISO 27001, NIS2, DORA, NIST CSF, ISO 22301

Contexto:
{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Normative Intelligence Engine"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1600,
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# RADAR IA (BASE + CCISO)
# ==========================================================

def analyze_radar_ia(client, context: dict):
    prompt = f"""
Eres Ellit Cognitive Core — Chief Information Security Officer (CCISO).

Evalúa:
- Gobierno de seguridad
- Gestión de riesgos
- Controles y cumplimiento
- Resiliencia operacional
- Cultura y liderazgo

Contexto:
{json.dumps(context, indent=2)}

Devuelve JSON con:
- indicadores (porcentajes)
- riesgos_clave
- acciones_recomendadas
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit CCISO Radar Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1500,
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# SGSI — MADUREZ (ISO 27001 / ENS)
# ==========================================================

def compute_sgsi_maturity(client, evidencias, controles):
    prompt = f"""
Eres Ellit Cognitive Core — Auditor SGSI Senior.

Evalúa madurez SGSI según ISO 27001 y ENS.

Evidencias:
{evidencias}

Controles:
{controles}

Devuelve JSON con:
- nivel
- madurez (0-100)
- fortalezas
- debilidades
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit SGSI Audit Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=900,
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# CLASE PRINCIPAL — ELLIT COGNITIVE CORE
# ==========================================================

class EllitCognitiveCore:

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    # Radar CCISO
    def analyze_radar(self, profile: dict):
        return analyze_radar_ia(self.client, profile)

    # SGSI
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
        return generate_predictive_analysis(self.client, payload)

    # Predictive
    def predict_standard(self, query: str):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query: str, benchmark=True, alerts=True, horizon="12 meses"):
        return predictive_prime_engine(self.client, query, benchmark, alerts, horizon)
