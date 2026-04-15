import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime, timedelta
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM SENNA 2026",
    page_icon="🏎️",
    layout="wide"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        st.write("#")
        try:
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA</h1>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center;'>🔐 Acceso al Sistema</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("INGRESAR AL PANEL DE CONTROL")
            
            if btn_login:
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")

# --- PANTALLA PRINCIPAL (TODO EL CONTENIDO PROFESIONAL) ---
else:
    # CSS para Estética Senna
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

    # Datos Inteligentes
    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Cuota (USD)": [450, 600, 300, 320, 800],
            "Score": [2, 5, 4, 1, 5],
            "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
        df["Total"] = df["Cuota (USD)"] + df["Mora"]
        
        def link_wa(fila):
            msg = f"CRM Senna Informa: {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Total: ${fila['Total']}. Saludos."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    # --- BARRA LATERAL (AQUÍ ESTÁN TUS OPCIONES) ---
    with st.sidebar:
        try:
            logo_side = Image.open("logo.png")
            st.image(logo_side, use_container_width=True)
        except:
            pass
        
        st.markdown(f"### 👤 Usuario: **Leo**")
        st.write("---")
        
        opcion = st.radio("MÓDULOS DE GESTIÓN:", [
            "📊 Dashboard Inteligente", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador y Archivo",
            "📄 Contratos y Simulador",
            "📍 Mapa de Cartera"
        ])
        
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        
        st.markdown("<p style='color: #55acee;'>CRM SENNA v2.2 | 2026</p>", unsafe_allow_html=True)

    # Encabezado Central
    st.markdown('<div class="titulo-central">CRM SENNA 2026</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899A6;'>Plataforma Inteligente de Control Total Automotriz</p>", unsafe_allow_html=True)

    # --- LÓGICA DE LOS MÓDULOS ---
    if opcion == "📊 Dashboard Inteligente":
        st.write("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><h3>Mora Generada</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        c4.markdown('<div class="card"><h3>Cartera</h3><h2>20 Clientes</h2></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Rendimiento de Cobranza")
        st.line_chart({"Proyectado": [4000, 5000, 4500, 6000], "Real": [3800, 4200, 4450, 2000]})

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Control de Deuda")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            if val == "AL DÍA": return 'background-color: #155123; color: white'
            return ''
        
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 Enviar"),
                "Score": st.column_config.ProgressColumn("Score", min_value=1, max_value=5, format="%d ⭐")
            }
        )

    elif opcion == "🔍 Buscador y Archivo":
        st.title("🔍 Archivo Digital")
        search = st.text_input("Buscar cliente...")
        if search:
            res = df[df["Cliente"].str.contains(search, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 {r['Cliente']}"):
                    st.write(f"Auto: {r['Vehículo']} | Score: {r['Score']}/5")
                    st.file_uploader(f"Subir documento para {r['Cliente']}")

    elif opcion == "📄 Contratos y Simulador":
        st.title("📄 Documentación y Cierre")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Generar PDF")
            sel = st.selectbox("Cliente:", df["Cliente"])
            if st.button("Generar Recibo"):
                st.success("PDF generado con éxito (Demo).")
        with col2:
            st.subheader("Simulador")
            monto = st.number_input("Deuda USD", value=1000)
            meses = st.slider("Plazo", 1, 12, 3)
            st.metric("Cuota", f"USD {round((monto*1.1)/meses, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("📍 Mapa de Morosidad")
        df_map = df.copy()
        df_map["color"] = df_map["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
        st.map(df_map, color="color", size=40)
        st.info("🔴 Rojo: Vencidos | 🔵 Azul: Al día")
