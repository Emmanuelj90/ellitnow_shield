import streamlit as st
import stripe
import json

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
endpoint_secret = st.secrets["STRIPE_WEBHOOK_SECRET"]

# Este archivo se ejecuta como endpoint independiente
def run():
    st.set_page_config(page_title="Stripe Webhook")

    payload = st.request.body
    sig_header = st.request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        st.write("⚠️ Webhook signature invalid:", str(e))
        st.stop()

    event_type = event["type"]
    session = event["data"]["object"]

    st.write(f"📩 Webhook recibido: {event_type}")

    if event_type == "checkout.session.completed":
        company_name = session["metadata"].get("company_name")
        admin_email = session["metadata"].get("admin_email")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        # === Aquí creas tu tenant automático ===
        st.write("🎉 Pago completado. Crear tenant:")
        st.write(company_name, admin_email, customer_id, subscription_id)

        # Aquí debes llamar a tu función real
        # create_tenant(company_name, admin_email, customer_id, subscription_id)

    st.write("OK")

