# ============================================================
#  MÓDULO DE LICENCIAS — Ellit Shield (Enterprise SaaS)
# ============================================================

import streamlit as st
import stripe

stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY")
APP_URL = st.secrets.get("APP_URL")


def render_licencias_tab():

    st.markdown("## Licencias Ellit Shield")

    st.markdown("""
    <p style="font-size:15px;color:#475569;max-width:820px;">
    Ellit Shield se licencia como plataforma <strong>Enterprise</strong>,
    con un módulo avanzado <strong>Prime — Predictive Intelligence</strong>
    para organizaciones que necesitan anticipación estratégica.
    </p>
    """, unsafe_allow_html=True)

    # ============================
    # CSS
    # ============================
    st.markdown("""
    <style>
    .license-grid {
        display: flex;
        gap: 32px;
        margin-top: 32px;
    }
    .license-card {
        flex: 1;
        background: #0F2F57;
        border-radius: 20px;
        padding: 36px;
        color: white;
        box-shadow: 0 20px 45px rgba(0,0,0,0.25);
    }
    .license-card.prime {
        background: #0B2545;
        border: 2px solid #9D2B6B;
    }
    .license-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .license-subtitle {
        font-size: 14px;
        color: #CBD5E1;
        margin-bottom: 20px;
    }
    .license-features {
        font-size: 14px;
        line-height: 1.9;
        margin-bottom: 28px;
    }
    .license-price {
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ============================
    # CARDS
    # ============================

    col1, col2 = st.columns(2)

    # -------- ENTERPRISE --------
    with col1:
        st.markdown("""
        <div class="license-card">
            <div class="license-title">Enterprise</div>
            <div class="license-subtitle">
                Gobierno, cumplimiento y resiliencia operacional
            </div>
            <div class="license-features">
                • Radar IA completo<br>
                • SGSI & ENS<br>
                • Continuidad de negocio & crisis<br>
                • Políticas IA<br>
                • Acceso multiusuario<br>
            </div>
            <div class="license-price">
                4.900 € <span style="font-size:16px;font-weight:500;">/ año</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Activar Enterprise", key="pay_enterprise"):
            session = stripe.checkout.Session.create(
                mode="subscription",
                line_items=[{
                    "price": st.secrets["STRIPE_PRICE_ENTERPRISE_ID"],
                    "quantity": 1
                }],
                success_url=f"{APP_URL}?success=enterprise",
                cancel_url=f"{APP_URL}?canceled=true",
            )
            st.markdown(f"[Continuar pago seguro →]({session.url})")


    # -------- PRIME --------
    with col2:
        st.markdown("""
        <div class="license-card prime">
            <div class="license-title">Prime — Predictive Intelligence</div>
            <div class="license-subtitle">
                Anticipación estratégica y simulación avanzada
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

        if st.button("Añadir Prime", key="pay_prime"):
            session = stripe.checkout.Session.create(
                mode="subscription",
                line_items=[{
                    "price": st.secrets["STRIPE_PRICE_PREDICTIVE_ID"],
                    "quantity": 1
                }],
                success_url=f"{APP_URL}?success=prime",
                cancel_url=f"{APP_URL}?canceled=true",
            )
            st.markdown(f"[Añadir Prime ahora →]({session.url})")

