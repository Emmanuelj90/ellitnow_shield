# ==========================================================
# ELLIT COGNITIVE CORE — MOTOR COGNITIVO CENTRAL (2025)
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
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        return None
    except:
        return None

# ==========================================================
# ⭐ NUEVO — Predictive Standard Engine
# ==========================================================
def predictive_standard_engine(client, query: str):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive Standard Engine.

Genera una predicción ejecutiva para la siguiente consulta:

\"\"\"{query}\"\"\"

### Entrega:
- Resumen ejecutivo
- 3 riesgos probables
- 3 impactos posibles
- Recomendaciones a 30 días
- Recomendaciones a 90 días
- Sin formato JSON, solo texto claro
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"Ellit Predictive Engine — Standard"},
            {"role":"user", "content":prompt}
        ],
        temperature=0.3,
        max_tokens=900,
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# ⭐ NUEVO — Predictive PRIME Engine
# ==========================================================
def predictive_prime_engine(client, query: str, benchmark=True, alerts=True, horizon="90 días"):
    prompt = f"""
Eres Ellit Cognitive Core — Predictive PRIME Engine.

Genera inteligencia avanzada con:

Consulta: \"\"\"{query}\"\"\"
Benchmark sectorial: {"Sí" if benchmark else "No"}
Alertas globales: {"Sí" if alerts else "No"}
Horizonte: {horizon}

### Entrega:
- Executive briefing (5–7 líneas)
- Riesgos correlacionados
- Factores emergentes
- Tendencias clave
- Benchmark sectorial (si aplica)
- Alertas globales (si aplica)
- Recomendaciones estratégicas
- Sin JSON
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"system", "content":"Ellit Predictive Engine — PRIME"},
            {"role":"user", "content":prompt}
        ],
        temperature=0.25,
        max_tokens=1600,
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# 1. RADAR IA
# ==========================================================
def analyze_radar_ia(client, context: dict):
    prompt = f"""
Eres **Ellit Cognitive Core**, motor experto en ENS, ISO 27001, NIST CSF,
DORA, ISO 22301 y seguridad corporativa.

Analiza el siguiente contexto:

{json.dumps(context, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Eres Ellit Cognitive Core, evaluador experto en GRC."},
            {"role":"user","content":prompt}
        ],
        temperature=0.25,
        max_tokens=1500
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# 2. MOTOR DE POLÍTICAS
# ==========================================================
def generate_policy(client, tipo, normativa, organizacion, detalle=3):
    prompt = f"""
Eres Ellit Cognitive Core. Redacta una política corporativa completa.
Tipo: {tipo}
Normativa: {normativa}
Organización: {organizacion}
Detalle: {detalle}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Generador experto de políticas ISO/ENS."},
            {"role":"user","content":prompt}
        ],
        temperature=0.3,
        max_tokens=1800
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# 3. BCP ENGINE
# ==========================================================
def generate_bcp_plan(client, data):
    prompt = f"""
Eres Ellit Cognitive Core, experto en continuidad ISO 22301 + ENS OP.BCP.
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
Analiza esto:
\"\"\"{contexto}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Analista de Continuidad"},
            {"role":"user","content":prompt}
        ],
        max_tokens=900
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
            {"role":"system","content":"Crisis Simulator"},
            {"role":"user","content":prompt}
        ],
        max_tokens=1600
    )
    return response.choices[0].message.content.strip()

# ==========================================================
# 4. PREDICTIVE INTELLIGENCE (JSON engines)
# ==========================================================
def generate_predictive_analysis(client, data):
    prompt = f"""
Eres Ellit Cognitive Core — Normativa Inteligente.
{json.dumps(data, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"system","content":"Normative Intelligence Engine"},
            {"role":"user","content":prompt}
        ]
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# 5. MADUREZ SGSI
# ==========================================================
def compute_sgsi_maturity(client, evidencias, controles):
    prompt = f"""
Eres Ellit Cognitive Core — Auditor SGSI.
Evidencias:
{evidencias}
Controles:
{controles}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Auditor SGSI"},
            {"role":"user","content":prompt}
        ],
        temperature=0.25,
        max_tokens=900
    )
    return extract_json(response.choices[0].message.content)

# ==========================================================
# ⭐ CLASE PRINCIPAL — WRAPPER
# ==========================================================
class EllitCognitiveCore:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    # Radar IA
    def analyze_radar(self, profile):
        return analyze_radar_ia(self.client, profile)

    # Madurez SGSI
    def compute_maturity(self, evidencias, controles):
        return compute_sgsi_maturity(self.client, evidencias, controles)

    # Normativa inteligente
    def analyze_normativa(self, perfil, radar, evidencias, controles):
        payload = {"perfil":perfil,"radar":radar,"evidencias":evidencias,"controles":controles}
        return generate_predictive_analysis(self.client, payload)

    # Políticas
    def generate_policy(self, tipo, normativa, organizacion, detalle=3):
        return generate_policy(self.client, tipo, normativa, organizacion, detalle)

    # BCP
    def generate_bcp(self, data):
        return generate_bcp_plan(self.client, data)

    # ⭐ Predictive Standard
    def predict_standard(self, query):
        return predictive_standard_engine(self.client, query)

    # ⭐ Predictive PRIME
    def predict_prime(self, query, benchmark=True, alerts=True, horizon="90 días"):
        return predictive_prime_engine(self.client, query, benchmark, alerts, horizon)

