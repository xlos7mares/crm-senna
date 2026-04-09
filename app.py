import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Inteligente Otormín", layout="wide")

# 2. CSS Maestro (Estética Pro)
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

# 3. Datos y Lógica
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
    df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
    df["Total"] = df["Cuota (USD)"] + df["Mora"]
    
    def link_wa(fila):
        msg = f"Hola {fila['Cliente']}, cuota de {fila['Vehículo']} vencida. Total con mora: ${fila['Total']}. Atte: Otormín Automóviles."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["WhatsApp"] = df.apply(link_wa, axis=1)
    return df

df = cargar_datos()

# 4. Función PDF
def generar_recibo(cliente, vehiculo, monto, tipo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AUTOMOTORA OTORMÍN", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Documento: {tipo}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Monto: USD {monto}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 5. Sidebar
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: pass
    st.markdown("### NAVEGACIÓN")
    opcion = st.radio("Módulos:", ["📊 Inteligencia de Negocio", "💰 Gestión de Cobros", "📄 Contratos y Simulador"])
    st.write("---")
    st.markdown("<p style='color: #55acee;'>Sistema v1.4 | Paysandú 2026</p>", unsafe_allow_html=True)

# 6. Título Central
st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 7. Módulos
if opcion == "📊 Inteligencia de Negocio":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h3>Intereses Mora</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
    st.subheader("📈 Proyección Semanal")
    st.line_chart({"Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "Ingresos (USD)": [2400, 3100, 1800, 4200]})

elif opcion == "💰 Gestión de Cobros":
    st.title("💸 Liquidación de Deuda")
    def color_estado(val):
        if val == "VENCIDO": return 'background-color: #701010; color: white'
        if val == "AL DÍA": return 'background-color: #155123; color: white'
        return ''
    st.dataframe(df.style.map(color_estado, subset=['Estado']), use_container_width=True, hide_index=True)

elif opcion == "📄 Contratos y Simulador":
    st.title("📄 Herramientas de Cierre")
    
    tab1, tab2 = st.tabs(["📄 Generar PDF", "🧮 Simulador de Cuotas"])
    
    with tab1:
        c_sel = st.selectbox("Cliente:", df["Cliente"])
        datos = df[df["Cliente"] == c_sel].iloc[0]
        pdf_bytes = generar_recibo(c_sel, datos["Vehículo"], datos["Total"], "Recibo")
        st.download_button("📥 Descargar PDF Oficial", data=pdf_bytes, file_name="recibo.pdf", mime="application/pdf")

    with tab2:
        st.subheader("Simulador para negociación")
        monto_ref = st.number_input("Deuda a refinanciar (USD):", value=500)
        cuotas_ref = st.slider("Plazo (meses):", 1, 12, 3)
        interes_ref = st.number_input("Interés mensual (%):", value=2.0)
        total_ref = monto_ref * (1 + (interes_ref/100 * cuotas_ref))
        st.metric("Cuota Mensual", f"USD {round(total_ref/cuotas_ref, 2)}")
        st.write(f"**Total final a cobrar:** USD {round(total_ref, 2)}")
