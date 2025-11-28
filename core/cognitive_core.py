# ==========================================================
# ELLIT COGNITIVE CORE — ENTERPRISE BRAIN (2025)
# CCISO · ENS · ISO 27001 · ISO 22301 · NIST · DORA · TPRM
# ==========================================================

import json
import re
from openai import OpenAI

# ==========================================================
# INIT CLIENT (V1 SAFE)
# ==========================================================

class EllitCognitiveCore:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    # ======================================================
    # PUBLIC API — DO NOT BREAK (USED BY ALL MODULES)
    # ======================================================

    def analyze_radar(self, profile: dict):
        """
        Main Radar Entry — used by Radar IA
        """
        base = _llm_radar_analysis(self.client, profile)
        enriched = _cciso_enrichment_engine(profile, base)
        return enriched

    def compute_maturity(self, evidencias: str, controles: str):
        """
        SGSI Maturity Engine
        """
        raw = _llm_sgsi_engine(self.client, evidencias, controles)
        return _sgsi_gap_engine(raw)

    def analyze_normativa(self, perfil, radar, evidencias, controles):
        payload = {
            "perfil": perfil,
            "radar": radar,
            "evidencias": evidencias,
            "controles": controles,
        }
        return _llm_json_engine(
            self.client,
            system="Normative Intelligence Engine",
            user=payload,
            model="gpt-4.1"
        )

    def generate_policy(self, tipo, normativa, organizacion, detalle=3):
        return _llm_text_engine(
            self.client,
            f"Redacta política {tipo} alineada con {normativa} para {organizacion}",
            max_tokens=1800
        )

    def generate_bcp(self, data):
        return _llm_text_engine(
            self.client,
            f"Genera BCP ISO 22301 + ENS:\n{json.dumps(data, indent=2)}",
            max_tokens=2000
        )

    def predict_standard(self, query):
        return _llm_text_engine(self.client, query)

    def predict_prime(self, query, benchmark=True, alerts=True, horizon="90 días"):
        prompt = f"""
        Consulta: {query}
        Benchmark: {benchmark}
        Alertas: {alerts}
        Horizonte: {horizon}
        """
        return _llm_text_engine(
            self.client,
            prompt,
            model="gpt-4.1",
            max_tokens=1600
        )


# ==========================================================
# LLM HELPERS (SAFE)
# ==========================================================

def _llm_text_engine(client, prompt, model="gpt-4o-mini", max_tokens=1200):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def _llm_json_engine(client, system, user, model="gpt-4o-mini", max_tokens=1500):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, indent=2)},
        ],
        temperature=0.25,
        max_tokens=max_tokens,
    )
    return _extract_json(response.choices[0].message.content)


def _extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        return json.loads(match.group(0)) if match else None
    except:
        return None


# ==========================================================
# RADAR — LLM RAW
# ==========================================================

def _llm_radar_analysis(client, profile: dict):
    prompt = f"""
    Evalúa postura de seguridad GRC según CCISO:
    Governance, Risk, Controls, Resilience, Culture.

    Contexto:
    {json.dumps(profile, indent=2)}

    Devuelve JSON con:
    - indicadores
    - riesgos_clave
    - acciones_recomendadas
    """
    return _llm_json_engine(client, "CCISO Radar Engine", profile)


# ==========================================================
# CCISO ENRICHMENT ENGINE (THE BRAIN)
# ==========================================================

def _cciso_enrichment_engine(profile: dict, base: dict):
    """
    THIS IS THE DIFFERENCE BETWEEN A TOY AND A PRODUCT
    """

    if not base:
        return {}

    indicators = base.get("indicadores", {})

    # ---- CCISO NORMALIZATION ----
    domains = {
        "Gobierno": indicators.get("Gobierno", 65),
        "Gestión de Riesgos": indicators.get("Gestión de Riesgos", 60),
        "Controles": indicators.get("Controles", 58),
        "Resiliencia": indicators.get("Resiliencia", 55),
        "Cultura": indicators.get("Cultura", 62),
    }

    # Penalización realista
    if profile.get("nivel_ens") == "Alto" and domains["Controles"] < 60:
        domains["Controles"] -= 10

    roadmap = []
    if domains["Gobierno"] < 70:
        roadmap.append("Formalizar comité de seguridad y reporting al board")
    if domains["Riesgos"] if "Riesgos" in domains else domains["Gestión de Riesgos"] < 65:
        roadmap.append("Implantar ERM alineado a ISO 27005")
    if domains["Controles"] < 70:
        roadmap.append("Cerrar gaps ISO 27001 Anexo A")
    if domains["Resiliencia"] < 65:
        roadmap.append("Actualizar BIA y DRP")
    if domains["Cultura"] < 70:
        roadmap.append("Programa de concienciación ejecutiva")

    return {
        "indicadores": domains,
        "riesgos_clave": base.get("riesgos_clave", []),
        "acciones_recomendadas": roadmap,
        "roadmap_90_dias": roadmap[:3],
        "roadmap_12_meses": roadmap,
        "modelo": "CCISO",
    }


# ==========================================================
# SGSI — GAP ANALYSIS REAL
# ==========================================================

def _llm_sgsi_engine(client, evidencias, controles):
    payload = {
        "evidencias": evidencias,
        "controles": controles,
        "framework": "ISO 27001 + ENS"
    }
    return _llm_json_engine(client, "SGSI Audit Engine", payload)


def _sgsi_gap_engine(raw: dict):
    if not raw:
        return None

    madurez = raw.get("madurez", 55)
    nivel = (
        "Inicial" if madurez < 40 else
        "Gestionado" if madurez < 60 else
        "Definido" if madurez < 75 else
        "Optimizado"
    )

    return {
        "madurez": madurez,
        "nivel": nivel,
        "fortalezas": raw.get("fortalezas", []),
        "debilidades": raw.get("debilidades", []),
        "plan_accion": raw.get("acciones_recomendadas", []),
    }
# ==========================================================
# BACKWARD COMPATIBILITY — DO NOT REMOVE
# Required by modules/bcp.py and legacy code
# ==========================================================

def generate_bcp_plan(client, data):
    """
    Legacy BCP entry point
    """
    core = EllitCognitiveCore(client.api_key if hasattr(client, "api_key") else None)
    return core.generate_bcp(data)


def analyze_bcp_context(client, contexto):
    prompt = f"""
    Eres Ellit Cognitive Core — Crisis Analyst.
    Analiza el siguiente contexto de continuidad:

    {contexto}

    Devuelve:
    - Riesgos
    - Impactos
    - Recomendaciones
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP Context Analyzer"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()


def analyze_bcp_scenario(client, data):
    prompt = f"""
    Eres Ellit Cognitive Core — Crisis Simulator.
    Evalúa el siguiente escenario:

    {json.dumps(data, indent=2)}

    Devuelve:
    - Impacto operativo
    - Impacto reputacional
    - Tiempo de recuperación
    - Recomendaciones ejecutivas
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP Scenario Simulator"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()
# ==========================================================
# BACKWARD COMPATIBILITY — PREDICTIVE MODULE
# Required by modules/predictive.py
# ==========================================================

def predictive_standard_engine(client, query: str):
    """
    Legacy entry point — Predictive Standard
    """
    core = EllitCognitiveCore(client.api_key if hasattr(client, "api_key") else None)
    return core.predict_standard(query)


def predictive_prime_engine(client, query: str, benchmark=True, alerts=True, horizon="90 días"):
    """
    Legacy entry point — Predictive PRIME
    """
    core = EllitCognitiveCore(client.api_key if hasattr(client, "api_key") else None)
    return core.predict_prime(
        query=query,
        benchmark=benchmark,
        alerts=alerts,
        horizon=horizon
    )
