# ============================================================
#  MÓDULO DE LICENCIAS — Ellit Shield (Enterprise SaaS)
# ============================================================

import streamlit as st
import stripe

# ============================================================
# CONFIG STRIPE
# ============================================================

stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY")
APP_URL = st.secrets.get("APP_URL")

# ============================================================
# CORE
# ============================================================

def render_licencias_tab():

    st.markdown("## Licencias Ellit Shield")

    st.markdown("""
    <p style="font-size:15px;color:#475569;max-width:820px;">
    Ellit Shield se licencia como plataforma <strong>Enterprise</strong>, con un módulo
    avanzado <strong>Prime — Predictive Intelligence</strong> para organizaciones que
    necesitan anticipación estratégica y simulación avanzada.
    </p>
    """, unsafe_allow_html=True)

    # ============================
    # ESTILOS
    # ============================

    st.markdown("""
    <style>
    .license-grid {
        display: flex;
        gap: 32px;
        margin-top: 30px;
    }

    .license-card {
        flex: 1;
        background: #0F2F57;
        border-radius: 20px;
        padding: 34px;
        color: white;
        box-shadow: 0 20px 45px rgba(0,0,0,0.25);
        position: relative;
        min-height: 520px;
    }

    .license-card.prime {
        background: #0B2545;
        border: 2px solid #9D2B6B;
    }

    .license-badge {
        position: absolute;
        top: 22px;
        right: 22px;
        background: #9D2B6B;
        padding: 6px 14px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .3px;
    }

    .license-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .license-subtitle {
        font-size: 15px;
        color: #CBD5E1;
        margin-bottom: 22px;
    }

    .license-features {
        font-size: 14px;
        line-height: 1.9;
        margin-bottom: 28px;
    }

    .license-features strong {
        color: #E879B8;
    }

    .license-price {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 22px;
    }

    div.stButton > button.ellit-cta {
        width: 100%;
        height: 52px;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 700;
        border: none;
        background: #9D2B6B;
        color: white;
        transition: all .15s ease;
    }

    div.stButton > button.ellit-cta:hover {
        background: #7F2358;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # =====================================================
    # ENTERPRISE
    # =====================================================
    with col1:
        st.markdown("""
        <div class="license-card">
            <div class="license-title">Enterprise</div>
            <div class="license-subtitle">
                Gobierno, cumplimiento y resiliencia operacional
            </div>

            <div class="license-features">
                • Radar IA completo (ENS, ISO, NIS2, DORA)<br>
                • SGSI & gestión de evidencias<br>
                • Continuidad de negocio & crisis<br>
                • Políticas IA corporativas<br>
                • Acceso multiusuario<br>
            </div>

            <div class="license-price">
                4.900 € <span style="font-size:16px;font-weight:500;">/ año</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Activar Enterprise", key="enterprise_pay", help="Activar licencia Enterprise"):
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[{
                        "price": st.secrets["STRIPE_PRICE_ENTERPRISE_ID"],
                        "quantity": 1
                    }],
                    success_url=f"{APP_URL}?success=enterprise",
                    cancel_url=f"{APP_URL}?canceled=true",
                )
                st.markdown(f"[Continuar pago seguro →]({session.url})")
            except Exception as e:
                st.error(f"Stripe error: {e}")

    # =====================================================
    # PRIME
    # =====================================================
    with col2:
        st.markdown("""
        <div class="license-card prime">
            <div class="license-badge">ADVANCED</div>

            <div class="license-title">Prime — Predictive Intelligence</div>
            <div class="license-subtitle">
                Anticipación estratégica basada en IA
            </div>

            <div class="license-features">
                • Predicción cognitiva avanzada<br>
                • Simulaciones estratégicas<br>
                • Roadmaps predictivos<br>
                • Scoring dinámico por riesgo<br>
                • <strong>Ellit Alert Tree</strong><br>
            </div>

            <div class="license-price">
                699 € <span style="font-size:16px;font-weight:500;">/ mes</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Añadir Prime", key="prime_pay", help="Añadir Prime Predictive Intelligence"):
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[{
                        "price": st.secrets["STRIPE_PRICE_PREDICTIVE_ID"],
                        "quantity": 1
                    }],
                    success_url=f"{APP_URL}?success=prime",
                    cancel_url=f"{APP_URL}?canceled=true",
                )
                st.markdown(f"[Añadir Prime ahora →]({session.url})")
            except Exception as e:
                st.error(f"Stripe error: {e}")
