import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Otormín Smart CRM v1.6", layout="wide")

# 2. Estética Profesional (Modo Oscuro Otormín)
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        [data-testid="stSidebar"] * { color: white !important; }
        .card {
            background-color: #1E2329;
            padding: 15px;
            border-radius: 10px;
            border-top: 4px solid #55acee;
            text-align: center;
            margin-bottom: 10px;
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

# 3. Datos con Inteligencia y Geolocalización
@st.cache_data
def cargar_todo():
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Cuota (USD)": [450, 600, 300, 320, 800],
        "Confianza": [2, 5, 4, 1, 5],
        "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
        "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
    }
    df = pd.DataFrame(data)
    df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
    df["Total"] = df["Cuota (USD)"] + df["Mora"]
    
    def link_wa(fila):
        msg = f"Otormín Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Total: ${fila['Total']}. Saludos."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["WhatsApp"] = df.apply(link_wa, axis=1)
    return df

df = cargar_todo()

# 4. Función PDF Real
def generar_pdf(cliente, vehiculo, monto, tipo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AUTOMOTORA OTORMÍN", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Vehículo: {vehiculo}", ln=True)
    pdf.cell(200, 10, txt=f"Total Liquidado: USD {monto}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 5. Sidebar (Navegación Unificada)
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: pass
    st.markdown("### 🔐 ACCESO: ADMIN")
    opcion = st.radio("Módulos:", [
        "📊 Inteligencia de Negocio", 
        "💰 Gestión de Cobros", 
        "🔍 Buscador y Archivo",
        "📄 Contratos y Simulador",
        "📍 Mapa de Cartera"
    ])
    st.write("---")
    st.markdown("v1.6 | **Premium Edition**")

# 6. Cabecera
st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 7. Lógica de Módulos (Sin errores de identación)
if opcion == "📊 Inteligencia de Negocio":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card"><h3>Cobranza</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h3>Intereses</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
    st.subheader("📈 Proyección Semanal")
    st.line_chart({"Semana": ["S1", "S2", "S3", "S4"], "Ingresos (USD)": [2400, 3100, 1800, 4200]})

elif opcion == "💰 Gestión de Cobros":
    st.title("💸 Operaciones de Cobranza")
    def color_estado(val):
        if val == "VENCIDO": return 'background-color: #701010; color: white'
        if val == "AL DÍA": return 'background-color: #155123; color: white'
        return ''
    st.dataframe(
        df.style.map(color_estado, subset=['Estado']),
        use_container_width=True, hide_index=True,
        column_config={
            "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
            "Confianza": st.column_config.ProgressColumn("Confianza", min_value=1, max_value=5, format="%d ⭐")
        }
    )

elif opcion == "🔍 Buscador y Archivo":
    st.title("🔍 Archivo Digital")
    search = st.text_input("Buscar cliente...")
    if search:
        res = df[df["Cliente"].str.contains(search, case=False)]
        for _, r in res.iterrows():
            with st.expander(f"👤 {r['Cliente']} - Ficha"):
                st.write(f"Auto: {r['Vehículo']} | Score: {r['Confianza']}/5")
                st.file_uploader(f"Adjuntar documento para {r['Cliente']}")

elif opcion == "📄 Contratos y Simulador":
    st.title("📄 Herramientas de Cierre")
    tab1, tab2 = st.tabs(["📄 Generar Recibo", "🧮 Simulador"])
    with tab1:
        sel = st.selectbox("Cliente:", df["Cliente"])
        row = df[df["Cliente"] == sel].iloc[0]
        pdf = generar_pdf(sel, row["Vehículo"], row["Total"], "Recibo Oficial")
        st.download_button("📥 Descargar PDF", data=pdf, file_name="recibo.pdf")
    with tab2:
        monto = st.number_input("Deuda USD", value=500)
        cuotas = st.slider("Meses", 1, 12, 3)
        st.metric("Cuota", f"USD {round((monto*1.1)/cuotas, 2)}")

elif opcion == "📍 Mapa de Cartera":
    st.title("🗺️ Mapa de Cobranza")
    df_map = df.copy()
    df_map["color"] = df_map["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
    st.map(df_map, color="color", size=40)
    st.info("🔴 Rojo: Vencidos | 🔵 Azul: Al día")
