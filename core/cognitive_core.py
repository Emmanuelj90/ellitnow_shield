# ==========================================================
# ELLIT COGNITIVE CORE — ENTERPRISE SECURITY INTELLIGENCE BRAIN
# CCISO · GRC · RISK · COMPLIANCE · RESILIENCE · STRATEGY
# ==========================================================

import json
import re
from typing import Dict, Any
from openai import OpenAI


# ==========================================================
# OPENAI INIT (NUEVA API ✅)
# ==========================================================

def init_openai(api_key: str):
    return OpenAI(api_key=api_key)


# ==========================================================
# JSON EXTRACTOR (ROBUSTO)
# ==========================================================

def extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return None


# ==========================================================
# CCISO RADAR ENGINE
# ==========================================================

def cciso_radar_engine(client: OpenAI, context: Dict[str, Any]) -> Dict[str, Any]:

    prompt = f"""
You are **Ellit Cognitive Core**, an executive-grade security intelligence engine.

You operate strictly using the **CCISO Domain Model**:
1. Governance & Risk Management
2. Controls & Compliance
3. Security Operations & Resilience
4. Security Program Capability
5. Strategy, Finance & Leadership

Aligned with ENS, ISO 27001, ISO 22301, NIST CSF, NIS2, DORA, TISAX.

Analyze this organization:

{json.dumps(context, indent=2)}

### RETURN ONLY JSON

{{
  "cciso_domains": {{
    "Governance & Risk Management (CCISO D1)": 0-100,
    "Controls & Compliance (CCISO D2)": 0-100,
    "Security Operations & Resilience (CCISO D3)": 0-100,
    "Security Program Capability (CCISO D4)": 0-100,
    "Strategy, Finance & Leadership (CCISO D5)": 0-100
  }},
  "top_risks": [
    "Executive-level risk 1",
    "Executive-level risk 2",
    "Executive-level risk 3"
  ],
  "priority_actions": [
    "Action within 30 days",
    "Action within 90 days",
    "Action within 12 months"
  ],
  "executive_readout": "5-6 lines for CEO / Board"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — CCISO Radar"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1600,
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# SGSI MATURITY ENGINE (ISO 27001 / ENS)
# ==========================================================

def sgsi_maturity_engine(client: OpenAI, evidences: str, controls: str):

    prompt = f"""
You are **Ellit Cognitive Core — SGSI Auditor**.

Evaluate SGSI maturity (ISO 27001 + ENS).

Evidences:
{evidences}

Controls:
{controls}

### RETURN ONLY JSON

{{
  "maturity_level": "Initial | Managed | Defined | Controlled | Optimized",
  "maturity_score": 0-100,
  "strengths": ["Strength 1","Strength 2"],
  "weaknesses": ["Weakness 1","Weakness 2"],
  "action_plan": {{
    "30_days": ["Action"],
    "90_days": ["Action"],
    "180_days": ["Action"]
  }}
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit SGSI Maturity Engine"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
        max_tokens=1200,
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# NORMATIVE / REGULATORY INTELLIGENCE
# ==========================================================

def normative_intelligence_engine(client: OpenAI, payload: Dict[str, Any]):

    prompt = f"""
You are **Ellit Cognitive Core — Regulatory Intelligence Engine**.

Assess against ENS, ISO 27001, NIST, NIS2, DORA, TISAX.

{json.dumps(payload, indent=2)}

### RETURN JSON ONLY
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Normative Intelligence"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1400,
    )

    return extract_json(response.choices[0].message.content)


# ==========================================================
# BCP ENGINE
# ==========================================================

def bcp_engine(client: OpenAI, data: Dict[str, Any]) -> str:

    prompt = f"""
Generate executive BCP aligned with ISO 22301 and ENS.

{json.dumps(data, indent=2)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit BCP Engine"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
        max_tokens=2000,
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# PREDICTIVE ENGINES
# ==========================================================

def predictive_standard_engine(client: OpenAI, query: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive Standard"},
            {"role": "user", "content": query},
        ],
        temperature=0.3,
        max_tokens=900,
    )

    return response.choices[0].message.content.strip()


def predictive_prime_engine(client: OpenAI, query: str, horizon="90 days") -> str:

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Predictive PRIME"},
            {"role": "user", "content": query},
        ],
        temperature=0.25,
        max_tokens=1600,
    )

    return response.choices[0].message.content.strip()


# ==========================================================
# ✅ MAIN ENTERPRISE WRAPPER
# ==========================================================

class EllitCognitiveCore:

    def __init__(self, api_key: str):
        self.client = init_openai(api_key)

    # Radar CCISO
    def analyze_radar(self, profile: Dict[str, Any]):
        return cciso_radar_engine(self.client, profile)

    # SGSI
    def compute_maturity(self, evidences: str, controls: str):
        return sgsi_maturity_engine(self.client, evidences, controls)

    # Normativa
    def analyze_normativa(self, profile, radar, evidences, controls):
        payload = {
            "profile": profile,
            "radar": radar,
            "evidences": evidences,
            "controls": controls,
        }
        return normative_intelligence_engine(self.client, payload)

    # BCP
    def generate_bcp(self, data: Dict[str, Any]):
        return bcp_engine(self.client, data)

    # Predictive
    def predict_standard(self, query: str):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query: str, horizon="90 days"):
        return predictive_prime_engine(self.client, query, horizon)
