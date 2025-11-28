# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
# ==========================================================
# GRC · CCISO · ENS · ISO 27001 · NIST · NIS2 · BCP · Predictive
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# JSON NORMALIZER (SEGURO)
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
# POLICIES ENGINE — ISO / ENS / NIST
# ==========================================================
def generate_policy_engine(client, tipo, normativa, organizacion, detalle=3):
    """
    Generador profesional de políticas de seguridad corporativas
    """
    prompt = f"""
Eres Ellit Cognitive Core — Policy Generator.

Genera una política corporativa de seguridad con nivel profesional.

Tipo de política: {tipo}
Normativa / Marco: {normativa}
Organización: {organizacion}
Nivel de detalle (1-5): {detalle}

Requisitos:
- Lenguaje corporativo
- Estructura clara
- Orientada a auditoría
- Lista para revisión de CISO
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Policy Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# PREDICTIVE STANDARD ENGINE
# ==========================================================
def predictive_standard_engine(client, query: str):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive Standard Engine.

Genera una predicción ejecutiva para:

\"\"\"{query}\"\"\"

Entrega:
- Resumen ejecutivo
- Riesgos principales
- Impactos esperados
- Recomendaciones a 30 / 90 días
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive Engine — Standard"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=900
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# PREDICTIVE PRIME ENGINE
# ==========================================================
def predictive_prime_engine(client, query: str, benchmark=True, alerts=True, horizon="90 días"):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive PRIME Engine.

Consulta: {query}
Benchmark sectorial: {"Sí" if benchmark else "No"}
Alertas globales: {"Sí" if alerts else "No"}
Horizonte: {horizon}

Entrega:
- Executive briefing
- Riesgos correlacionados
- Factores emergentes
- Tendencias clave
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
# RADAR IA — CCISO / GRC ENGINE
# ==========================================================
def analyze_radar_ia(client, context: dict):
    prompt = f"""
Eres Ellit Cognitive Core, CISO virtual experto en:

- CCISO domains
- ISO 27001 / 22301
- ENS
- NIST CSF
- NIS2
- Gobierno, Riesgo y Cumplimiento

Analiza este contexto organizativo:

{json.dumps(context, indent=2)}

Entrega EXCLUSIVAMENTE en JSON con:
- indicadores (0–100)
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
        max_tokens=1500
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# MOTOR DE POLÍTICAS CORPORATIVAS
# ==========================================================
def generate_policy(client, tipo, normativa, organizacion, detalle=3):
    prompt = f"""
Eres Ellit Cognitive Core — Policy Generator.

Redacta una política corporativa profesional:

Tipo: {tipo}
Normativa: {normativa}
Organización: {organizacion}
Nivel de detalle: {detalle}/5

Debe incluir:
- Objetivo
- Alcance
- Responsabilidades
- Directrices
- Controles
- Cumplimiento
- Revisión
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Policy Generator — GRC Expert"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1800
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# BCP ENGINE (COMPATIBLE CON modules.bcp)
# ==========================================================
def generate_bcp_plan(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — BCP Expert (ISO 22301 / ENS).

{json.dumps(data, indent=2)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit BCP Engine"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()


def analyze_bcp_context(client, contexto):
    prompt = f"""
Eres Ellit Cognitive Core — Crisis Analyst.

{contexto}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Crisis Analyst"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=900
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
            {"role": "system", "content": "Ellit Crisis Simulator"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1600
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# MADUREZ SGSI ENGINE
# ==========================================================
def compute_sgsi_maturity(client, evidencias, controles):
    prompt = f"""
Eres Ellit Cognitive Core — Auditor SGSI.

Evidencias:
{evidencias}

Controles:
{controles}

Entrega en JSON:
- nivel
- madurez (%)
- fortalezas
- debilidades
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
# CLASE PRINCIPAL — WRAPPER ÚNICO
# ==========================================================
class EllitCognitiveCore:

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    # =============================
    # RADAR IA (CCISO / GRC)
    # =============================
    def analyze_radar(self, profile):
        return analyze_radar_ia(self.client, profile)

    # =============================
    # SGSI — MADUREZ
    # =============================
    def compute_maturity(self, evidencias, controles):
        return compute_sgsi_maturity(self.client, evidencias, controles)

    # =============================
    # POLÍTICAS CORPORATIVAS
    # =============================
    def generate_policy(self, tipo, normativa, organizacion, detalle=3):
        return generate_policy(self.client, tipo, normativa, organizacion, detalle)

    # =============================
    # BCP / CONTINUIDAD
    # =============================
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)

    def analyze_bcp_context(self, contexto):
        return analyze_bcp_context(self.client, contexto)

    def analyze_bcp_scenario(self, data):
        return analyze_bcp_scenario(self.client, data)

    # =============================
    # PREDICTIVE INTELLIGENCE
    # =============================
    def predict_standard(self, query):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query, benchmark=True, alerts=True, horizon="90 días"):
        return predictive_prime_engine(self.client, query, benchmark, alerts, horizon)

    # =============================
    # ANÁLISIS TEXTUAL EJECUTIVO
    # (SGSI, Dashboard, Board-level)
    # =============================
    def analyze_text(self, prompt: str):
        """
        Motor genérico de análisis ejecutivo.
        Usado por:
        - SGSI Monitoring
        - Dashboards
        - Resúmenes ejecutivos
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ellit Cognitive Core — Executive SGSI & Board Analyst"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

