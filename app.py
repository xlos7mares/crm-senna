import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime, timedelta

# 1. Configuración de la página
st.set_page_config(page_title="Otormín Smart CRM v1.5", layout="wide")

# 2. Estética Profesional
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
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #1E2329;
            border-radius: 5px 5px 0px 0px;
            padding: 10px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Datos y Lógica de Inteligencia
@st.cache_data
def cargar_datos_completos():
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Cuota (USD)": [450, 600, 300, 320, 800],
        "Score": [2, 5, 4, 1, 5], # 1 a 5 estrellas
        "Lat": [-32.31, -32.32, -32.30, -32.33, -32.31], # Simulación Mapa Paysandú
        "Lon": [-58.08, -58.07, -58.09, -58.08, -58.10]
    }
    df = pd.DataFrame(data)
    df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
    df["Total"] = df["Cuota (USD)"] + df["Mora"]
    
    def link_wa(fila):
        msg = f"Otormín Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Total: ${fila['Total']}. Saludos."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    
    df["WhatsApp"] = df.apply(link_wa, axis=1)
    return df

df = cargar_datos_completos()

# 4. Sidebar con Niveles de Acceso (Simulado)
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: pass
    st.markdown("### 🔐 ACCESO: ADMINISTRADOR")
    opcion = st.radio("Módulos:", [
        "📊 Inteligencia de Negocio", 
        "💰 Gestión de Cobros", 
        "🔍 Buscador y Archivo",
        "📄 Contratos y Simulador",
        "📍 Mapa de Cartera"
    ])
    st.write("---")
    st.markdown("v1.5 | **Premium Edition**")

# 5. MÓDULOS DE LA APLICACIÓN

if opcion == "📊 Inteligencia de Negocio":
    st.title("🚀 Tablero de Decisiones Estratégicas")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="card"><h3>Cobranza</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h3>Intereses</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
    c4.markdown('<div class="card"><h3>Clientes</h3><h2>20</h2></div>', unsafe_allow_html=True)
    
    st.subheader("📈 Proyección de Caja (Ingresos Reales vs Esperados)")
    chart_data = pd.DataFrame({
        "Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"],
        "Esperado": [4000, 5000, 4500, 6000],
        "Real": [3800, 4200, 4450, 2000]
    }).set_index("Semana")
    st.line_chart(chart_data)

elif opcion == "💰 Gestión de Cobros":
    st.title("💸 Operaciones de Cobranza")
    
    tab_list, tab_agenda = st.tabs(["📋 Lista General", "📅 Agenda del Día"])
    
    with tab_list:
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
        
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 Enviar"),
                "Score": st.column_config.ProgressColumn("Confianza", min_value=1, max_value=5, format="%d ⭐")
            }
        )
    
    with tab_agenda:
        st.subheader("📅 Tareas Críticas para Hoy")
        hoy = df[df["Estado"] == "VENCIDO"]
        for _, r in hoy.iterrows():
            with st.expander(f"🔴 LLAMAR A: {r['Cliente']}"):
                st.write(f"**Vehículo:** {r['Vehículo']} | **Deuda:** ${r['Total']}")
                st.text_area(f"Bitácora de gestión para {r['Cliente']}:", placeholder="Escribe aquí el compromiso de pago...")
                if st.button(f"Guardar nota para {r['Cliente']}"):
                    st.success("Nota guardada en el historial.")

elif opcion == "🔍 Buscador y Archivo":
    st.title("🔍 Archivo Digital de Clientes")
    search = st.text_input("Buscar por nombre o auto...")
    if search:
        res = df[df["Cliente"].str.contains(search, case=False)]
        for _, r in res.iterrows():
            st.markdown(f"### 👤 {r['Cliente']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Auto:** {r['Vehículo']}")
                st.write(f"**Score de Pago:** {r['Score']} / 5")
            with col_b:
                st.file_uploader(f"Subir Contrato/DNI de {r['Cliente']}", type=["jpg", "png", "pdf"])

elif opcion == "📄 Contratos y Simulador":
    st.title("📄 Herramientas de Cierre")
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Generador de PDF")
        c_sel = st.selectbox("Cliente:", df["Cliente"])
        if st.button("Generar Recibo Oficial"):
            st.success("PDF Listo para descarga.")
    with col_r:
        st.subheader("Simulador de Refinanciación")
        monto = st.number_input("Monto USD", value=1000)
        cuotas = st.slider("Cuotas", 1, 12, 3)
        st.metric("Cuota Mensual", f"USD {round((monto*1.1)/cuotas, 2)}")

elif opcion == "📍 Mapa de Cartera":
    st.title("🗺️ Mapa de Cobranza en Paysandú")
    st.write("Visualiza la ubicación de tus activos y deudores.")
    st.map(df[["Lat", "Lon"]])
