import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Configuración y Estética
st.set_page_config(page_title="Gestión Inteligente Otormín", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        .card {
            background-color: #1E2329;
            padding: 20px;
            border-radius: 10px;
            border-top: 4px solid #55acee;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Datos con "Poder de Análisis"
data = {
    "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
    "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
    "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
    "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
    "Cuota (USD)": [450, 600, 300, 320, 800],
    "Días de Atraso": [10, 0, 0, 15, 0]
}
df = pd.DataFrame(data)

# Calculamos Mora Automática (Algo que Excel no hace solo tan fácil)
tasa_mora = 0.02 # 2% por atraso
df["Intereses Mora"] = df.apply(lambda x: x["Cuota (USD)"] * tasa_mora if x["Estado"] == "VENCIDO" else 0, axis=1)
df["Total a Cobrar"] = df["Cuota (USD)"] + df["Intereses Mora"]

# 3. Sidebar
with st.sidebar:
    st.image("logo.png")
    opcion = st.radio("Módulos:", ["📊 Inteligencia de Negocio", "💰 Gestión de Cobros", "📄 Generador de Contratos"])

# 4. Lo que lo hace POTENTE: Inteligencia de Negocio
if opcion == "📊 Inteligencia de Negocio":
    st.title("🚀 Panel de Control Estratégico")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><h3>Efectividad de Cobro</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    with col2:
        total_mora = df["Intereses Mora"].sum()
        st.markdown(f'<div class="card"><h3>Intereses Ganados</h3><h2 style="color:#55acee">${total_mora}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><h3>Riesgo de Cartera</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📈 Proyección de Ingresos Semanales")
    # Simulación de flujo de caja
    chart_data = pd.DataFrame({"Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "Ingresos Esperados (USD)": [2400, 3100, 1800, 4200]})
    st.line_chart(chart_data.set_index("Semana"))

elif opcion == "💰 Gestión de Cobros":
    st.subheader("💸 Liquidación de Deuda en Tiempo Real")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.info("💡 Este sistema calcula automáticamente el interés por mora y actualiza el saldo sin intervención humana.")

elif opcion == "📄 Generador de Contratos":
    st.subheader("📄 Automatización Documental")
    cliente_sel = st.selectbox("Seleccionar Cliente para generar documento:", df["Cliente"])
    tipo_doc = st.selectbox("Tipo de documento:", ["Recibo de Pago", "Convenio de Refinanciación", "Notificación Judicial"])
    
    if st.button("Generar Documento"):
        st.success(f"Generando {tipo_doc} para {cliente_sel}...")
        st.download_button("Descargar PDF", "Contenido del PDF simulado", file_name=f"{cliente_sel}.pdf")
