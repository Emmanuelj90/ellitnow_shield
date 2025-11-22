from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
import datetime as _dt
import streamlit as st

def generate_corporate_pdf(title: str, tenant_name: str, content: str, filename: str = "EllitNow_Report.pdf"):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    fuchsia = Color(1, 0, 0.5)
    blue = Color(0, 0.7, 1)

    # Fondo degradado
    for i in range(100):
        c = Color(1 - i/120, 0 + i/150, 0.5 + i/200)
        pdf.setFillColor(c)
        pdf.rect(0, (i/100)*height, width, height/100, stroke=0, fill=1)

    # Logo
    logo_url = "https://i.imgur.com/b8U3pAL.png"
    try:
        logo = ImageReader(logo_url)
        pdf.drawImage(logo, 40, height - 100, width=80, preserveAspectRatio=True)
    except:
        pdf.setFillColor(fuchsia)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(40, height - 100, "EllitNow Shield")

    # Cabecera
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(140, height - 60, "EllitNow Shield")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(140, height - 80, "AI Executive Security Platform")

    # Título
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(fuchsia)
    pdf.drawString(40, height - 150, title)
    pdf.setFont("Helvetica", 11)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(40, height - 170, f"Cliente: {tenant_name}")
    pdf.drawString(40, height - 185, f"Fecha: {_dt.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Contenido
    pdf.setFont("Helvetica", 11)
    text_obj = pdf.beginText(40, height - 220)
    text_obj.setFillColorRGB(1, 1, 1)
    text_obj.setLeading(16)

    for line in content.split("\n"):
        text_obj.textLine(line)

    pdf.drawText(text_obj)

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(blue)
    pdf.drawString(40, 40, "© 2025 EllitNow Cognitive Core — Confidential Document")
    pdf.drawRightString(width - 40, 40, "Página 1 de 1")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer


def download_pdf_button(title, tenant_name, content, filename):
    pdf_buffer = generate_corporate_pdf(title, tenant_name, content, filename)
    st.download_button(
        label=f"Descargar {title}",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf",
    )
