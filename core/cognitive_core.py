# ==========================================================
# ELLIT COGNITIVE CORE — ENTERPRISE SECURITY INTELLIGENCE BRAIN
# CCISO · GRC · RISK · COMPLIANCE · RESILIENCE · STRATEGY
# ==========================================================

import json
import re
import openai
from typing import Dict, Any

# ==========================================================
# OPENAI INIT (SAFE & CLOUD READY)
# ==========================================================

def init_openai(api_key: str):
    openai.api_key = api_key
    return openai


# ==========================================================
# JSON EXTRACTOR (HARDENED)
# ==========================================================

def extract_json(text: str):
    """
    Extracts first valid JSON object from LLM output.
    """
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return None


# ==========================================================
# 🧠 CCISO RADAR ENGINE (CORE OF THE PLATFORM)
# ==========================================================

def cciso_radar_engine(client, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executive Security Radar aligned with CCISO Domains.
    """

    prompt = f"""
You are **Ellit Cognitive Core**, an enterprise-grade security intelligence engine,
designed to assist Chief Information Security Officers (CISOs).

You operate using the **CCISO Domain Model**, aligned with:
- ENS
- ISO/IEC 27001
- ISO/IEC 22301
- NIST CSF
- NIS2
- DORA
- TISAX
- Third-Party & Supply Chain Risk

Analyze the following organization context:

{json.dumps(context, indent=2)}

### OUTPUT — RETURN ONLY VALID JSON

{{
  "cciso_domains": {{
    "Governance & Risk Management (CCISO D1)": 0-100,
    "Controls & Compliance (CCISO D2)": 0-100,
    "Security Operations & Resilience (CCISO D3)": 0-100,
    "Security Program Capability (CCISO D4)": 0-100,
    "Strategy, Finance & Leadership (CCISO D5)": 0-100
  }},
  "top_risks": [
    "Executive-level risk description 1",
    "Executive-level risk description 2",
    "Executive-level risk description 3"
  ],
  "priority_actions": [
    "Board-level action within 30 days",
    "Strategic action within 90 days",
    "Structural action within 12 months"
  ],
  "executive_readout": "5–6 lines written for CEO / Board, summarizing posture, exposure and priorities."
}}
"""

    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — CCISO Radar Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.20,
        max_tokens=1600
    )

    return extract_json(response.choices[0].message["content"])


# ==========================================================
# 🛡 SGSI MATURITY & GAP ANALYSIS ENGINE
# ==========================================================

def sgsi_maturity_engine(client, evidences: str, controls: str) -> Dict[str, Any]:
    prompt = f"""
You are **Ellit Cognitive Core — SGSI Auditor**.

Evaluate the REAL maturity of an Information Security Management System
based on ISO/IEC 27001 and ENS.

Evidences:
{evidences}

Controls:
{controls}

### OUTPUT — ONLY JSON

{{
  "maturity_level": "Initial | Managed | Defined | Quantitatively Controlled | Optimized",
  "maturity_score": 0-100,
  "domain_gaps": {{
    "Governance": 0-100,
    "Risk Management": 0-100,
    "Controls Implementation": 0-100,
    "Operations & Monitoring": 0-100,
    "Continuous Improvement": 0-100
  }},
  "strengths": [
    "Key strength 1",
    "Key strength 2"
  ],
  "weaknesses": [
    "Key weakness 1",
    "Key weakness 2"
  ],
  "action_plan": {{
    "30_days": ["Action 1"],
    "90_days": ["Action 1"],
    "180_days": ["Action 1"]
  }}
}}
"""

    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — SGSI Maturity Engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1200
    )

    return extract_json(response.choices[0].message["content"])


# ==========================================================
# 📚 NORMATIVE / REGULATORY INTELLIGENCE ENGINE
# ==========================================================

def normative_intelligence_engine(client, payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
You are **Ellit Cognitive Core — Regulatory Intelligence Engine**.

Assess the organization against:
ENS, ISO 27001, NIST CSF, NIS2, DORA, TISAX.

Input:
{json.dumps(payload, indent=2)}

### OUTPUT — ONLY JSON

{{
  "primary_framework": "Recommended primary framework",
  "secondary_frameworks": ["Framework 1", "Framework 2"],
  "regulatory_exposure": "LOW | MEDIUM | HIGH",
  "roadmap": {{
    "30_days": ["Action 1"],
    "90_days": ["Action 1"],
    "12_months": ["Action 1"]
  }}
}}
"""

    response = client.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Cognitive Core — Normative Intelligence"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1400
    )

    return extract_json(response.choices[0].message["content"])


# ==========================================================
# 🔁 BCP & RESILIENCE ENGINE (ISO 22301)
# ==========================================================

def bcp_engine(client, data: Dict[str, Any]) -> str:
    prompt = f"""
You are **Ellit Cognitive Core — Business Continuity & Resilience Expert**.

Generate an executive-grade BCP aligned with ISO 22301 and ENS.

Data:
{json.dumps(data, indent=2)}
"""

    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "BCP & Resilience Intelligence"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=2000
    )

    return response.choices[0].message["content"].strip()


# ==========================================================
# 🔮 PREDICTIVE INTELLIGENCE ENGINES
# ==========================================================

def predictive_standard_engine(client, query: str) -> str:
    prompt = f"""
Generate executive predictive intelligence for a CISO.

Query:
{query}

Deliver:
- Executive summary
- Probable risks
- Business impacts
- Recommendations (30/90 days)
"""

    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ellit Predictive — Standard"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=900
    )

    return response.choices[0].message["content"].strip()


def predictive_prime_engine(client, query: str, horizon="90 days") -> str:
    prompt = f"""
You are Ellit Cognitive Core — Predictive PRIME.

Horizon: {horizon}
Query:
{query}

Deliver strategic, board-level foresight, correlations and alerts.
"""

    response = client.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Ellit Predictive — PRIME"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1600
    )

    return response.choices[0].message["content"].strip()


# ==========================================================
# ⭐ MAIN ENTERPRISE WRAPPER (STABLE API)
# ==========================================================

class EllitCognitiveCore:
    """
    Enterprise-grade cognitive brain for Ellit Shield.
    """

    def __init__(self, api_key: str):
        self.client = init_openai(api_key)

    # === CCISO RADAR ===
    def analyze_radar(self, profile: Dict[str, Any]):
        return cciso_radar_engine(self.client, profile)

    # === SGSI ===
    def compute_maturity(self, evidences: str, controls: str):
        return sgsi_maturity_engine(self.client, evidences, controls)

    # === REGULATORY INTELLIGENCE ===
    def analyze_normativa(self, profile, radar, evidences, controls):
        payload = {
            "profile": profile,
            "radar": radar,
            "evidences": evidences,
            "controls": controls
        }
        return normative_intelligence_engine(self.client, payload)

    # === BCP ===
    def generate_bcp(self, data: Dict[str, Any]):
        return bcp_engine(self.client, data)

    # === PREDICTIVE ===
    def predict_standard(self, query: str):
        return predictive_standard_engine(self.client, query)

    def predict_prime(self, query: str, horizon="90 days"):
        return predictive_prime_engine(self.client, query, horizon)

