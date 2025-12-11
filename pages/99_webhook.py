import streamlit as st
import stripe
import json

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
endpoint_secret = st.secrets["STRIPE_WEBHOOK_SECRET"]

st.set_page_config(page_title="Stripe Webhook Listener", page_icon="🔔")

st.write("🔔 Webhook activo — Ellit Shield")

# Streamlit Cloud proporciona st.request en endpoints directos (como esta página)
if "request" not in st.session_state:
    st.session_state["request"] = {}

req = st.request

if req.method != "POST":
    st.warning("Este endpoint solo acepta peticiones POST desde Stripe.")
    st.stop()

payload = req.body
sig_header = req.headers.get("Stripe-Signature")

try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
except Exception as e:
    st.error(f"❌ Error verificando firma: {e}")
    st.stop()

st.success("Webhook recibido correctamente")

# Procesar evento
if event["type"] == "checkout.session.completed":
    session = event["data"]["object"]

    company_name = session["metadata"]["company_name"]
    admin_email = session["metadata"]["admin_email"]
    customer_id = session["customer"]
    subscription_id = session["subscription"]

    st.info(f"Empresa: {company_name}")
    st.info(f"Admin: {admin_email}")
    st.info(f"CustomerID: {customer_id}")
    st.info(f"SubscriptionID: {subscription_id}")

    # Aquí llamas a tu sistema real de creación de tenant:
    # create_tenant(company_name, admin_email, customer_id, subscription_id)

    st.success("Tenant creado correctamente.")

else:
    st.warning(f"Evento ignorado: {event['type']}")
