import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Inteligente Otormín", layout="wide")

# 2. CSS Maestro (Estética de Alto Impacto)
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        [data-testid="stSidebar"] * { color: white !important; }
        .card {
            background-color: #1E2329;
            padding: 20px;
            border-radius: 10px;
            border-top: 4px solid #55acee;
            text-align: center;
            margin-bottom: 20px;
        }
        .titulo-central {
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: bold;
            margin-top: -20px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Datos y Lógica de Negocio
@st.cache_data
def cargar_datos():
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Cuota (USD)": [450, 600, 300, 320, 800]
    }
    df = pd.DataFrame(data)
    # Cálculo de mora promediado
    df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
    df["Total"] = df["Cuota (USD)"] + df["Mora"]
    
    # Link de WhatsApp con deuda detallada
    def link_wa(fila):
        msg = f"Hola {fila['Cliente']}, le informamos que su cuota de {fila['Vehículo']} está vencida. Cuota: ${fila['Cuota (USD)']} + Mora: ${fila['Mora']}. Total: ${fila['Total']}. Atte: Otormín Automóviles."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["WhatsApp"] = df.apply(link_wa, axis=1)
    return df

df = cargar_datos()

# 4. Función para generar PDF Profesional
def generar_recibo(cliente, vehiculo, monto, tipo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AUTOMOTORA OTORMÍN", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Documento: {tipo}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Detalles para: {cliente}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Vehículo: {vehiculo}", ln=True)
    pdf.cell(200, 10, txt=f"Monto Total: USD {monto}", ln=True)
    pdf.ln(20)
    pdf.cell(200, 10, txt="_______________________", ln=True, align='C')
    pdf.cell(200, 10, txt="Firma Autorizada", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 5. Sidebar
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: pass
    st.markdown("### NAVEGACIÓN")
    opcion = st.radio("Módulos:", ["📊 Inteligencia de Negocio", "💰 Gestión de Cobros", "📄 Generador de Contratos"])
    st.write("---")
    st.markdown("<p style='color: #55acee;'>Sistema v1.3 | Paysandú 2026</p>", unsafe_allow_html=True)

# 6. Encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 7. Módulos
if opcion == "📊 Inteligencia de Negocio":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card"><h3>Intereses Ganados</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><h3>Riesgo Cartera</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
    
    st.subheader("📈 Proyección de Cobros Semanales")
    st.line_chart({"Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "Ingresos (USD)": [2400, 3100, 1800, 4200]})

elif opcion == "💰 Gestión de Cobros":
    st.title("💸 Liquidación y Cobranza")
    
    def color_estado(val):
        if val == "VENCIDO": return 'background-color: #701010; color: white'
        if val == "AL DÍA": return 'background-color: #155123; color: white'
        return ''

    st.dataframe(
        df.style.map(color_estado, subset=['Estado']),
        use_container_width=True,
        hide_index=True,
        column_config={
            "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
            "Cuota (USD)": st.column_config.NumberColumn(format="$ %d"),
            "Mora": st.column_config.NumberColumn(format="$ %.2f"),
            "Total": st.column_config.NumberColumn(format="$ %.2f")
        }
    )
    st.info("💡 La columna 'Mora' se calcula en tiempo real según el estado del cliente.")

elif opcion == "📄 Generador de Contratos":
    st.title("📄 Automatización de Documentos")
    c_sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
    datos = df[df["Cliente"] == c_sel].iloc[0]
    t_doc = st.selectbox("Tipo de Documento:", ["Recibo de Pago", "Convenio de Pago", "Notificación Judicial"])
    
    pdf_bytes = generar_recibo(c_sel, datos["Vehículo"], datos["Total"], t_doc)
    
    st.download_button(
        label="📥 Descargar PDF Oficial",
        data=pdf_bytes,
        file_name=f"{t_doc}_{c_sel}.pdf",
        mime="application/pdf"
    )
    st.success("✅ Documento generado correctamente con formato profesional.")
