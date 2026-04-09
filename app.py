import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF # Importamos la librería para PDFs reales

# 1. Configuración y Estética
st.set_page_config(page_title="Gestión Inteligente Otormín", layout="wide")

# 2. Función para generar el PDF Real
def generar_pdf_real(cliente, vehiculo, monto, tipo):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AUTOMOTORA OTORMÍN - PAYSANDÚ", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Documento: {tipo}", ln=True, align='C')
    pdf.ln(10)
    
    # Contenido
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"DETALLES DEL CLIENTE:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Nombre: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Vehículo: {vehiculo}", ln=True)
    pdf.cell(200, 10, txt=f"Monto Total: USD {monto}", ln=True)
    pdf.ln(10)
    
    # Texto Legal / Pie
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, txt="Este documento es una notificación oficial generada por el sistema de gestión de Automotora Otormín. Para más información, diríjase a nuestras oficinas.")
    
    return pdf.output(dest='S').encode('latin-1')

# 3. Datos (Simulados como veníamos haciendo)
data = {
    "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
    "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
    "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
    "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
    "Cuota (USD)": [450, 600, 300, 320, 800]
}
df = pd.DataFrame(data)

# 4. Sidebar
with st.sidebar:
    try: st.image("logo.png")
    except: pass
    opcion = st.radio("Módulos:", ["💰 Gestión de Cobros", "📄 Generador de Contratos"])

# 5. Módulo: Gestión de Cobros (Con WhatsApp)
if opcion == "💰 Gestión de Cobros":
    st.title("💸 Cobranza Activa")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("💡 Haz clic en 'Generador de Contratos' para crear el PDF legal.")

# 6. Módulo: Generador de Contratos (LA PARTE QUE FALLABA)
elif opcion == "📄 Generador de Contratos":
    st.title("📄 Automatización de Documentos")
    
    # Buscamos los datos del cliente seleccionado
    cliente_sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
    datos_c = df[df["Cliente"] == cliente_sel].iloc[0]
    
    tipo_doc = st.selectbox("Tipo de Documento:", ["Recibo de Pago", "Convenio de Pago", "Notificación Judicial"])
    
    # Creamos el PDF en memoria
    pdf_bytes = generar_pdf_real(cliente_sel, datos_c["Vehículo"], datos_c["Cuota (USD)"], tipo_doc)
    
    st.write(f"Preparando {tipo_doc} para {cliente_sel}...")
    
    # Botón de descarga real
    st.download_button(
        label="📥 Descargar Documento Oficial",
        data=pdf_bytes,
        file_name=f"{tipo_doc}_{cliente_sel}.pdf",
        mime="application/pdf"
    )
    
    st.success("✅ ¡PDF generado con éxito! Ahora puedes abrirlo sin errores.")
