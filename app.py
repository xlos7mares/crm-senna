import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime, timedelta
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
st.set_page_config(
    page_title="AutoGestion Pro URU v2.0 - Login",
    page_icon="🔐",
    layout="wide"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    # Estética para el Login
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            .login-box {
                background-color: #161B22;
                padding: 30px;
                border-radius: 15px;
                border: 1px solid #55acee;
            }
        </style>
    """, unsafe_allow_html=True)

    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        st.write("#")
        try:
            # Intenta cargar el logo
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            st.info("🚗 **AutoGestion Pro URU**")
        
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
                    st.error("❌ Usuario o contraseña incorrectos.")

# --- PANTALLA PRINCIPAL (Solo visible tras el Login) ---
else:
    # Estética Profesional CRM (Modo Oscuro SaaS)
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
            .titulo-central {
                text-align: center;
                color: white;
                font-size: 2.2rem;
                font-weight: bold;
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
            "Score": [2, 5, 4, 1, 5],
            "latitude": [-32.31, -32.32, -32.30, -32.33, -32.31],
            "longitude": [-58.08, -58.07, -58.09, -58.08, -58.10]
        }
        df = pd.DataFrame(data)
        df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
        df["Total"] = df["Cuota (USD)"] + df["Mora"]
        
        def link_wa(fila):
            msg = f"Aviso de Gestión de Cobranza Automotriz: Estimado {fila['Cliente']}, le informamos que su cuota por el {fila['Vehículo']} se encuentra en estado {fila['Estado']}. El saldo total liquidado es de ${fila['Total']}. Saludos cordiales."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos_completos()

    # 4. Sidebar con Logo y Navegación
    with st.sidebar:
        try:
            logo_side = Image.open("logo.png")
            st.image(logo_side, use_container_width=True)
        except:
            pass
        
        st.markdown(f"### 👤 Usuario: **Leo**")
        st.write("---")
        
        opcion = st.radio("Módulos:", [
            "📊 Inteligencia de Negocio", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador y Archivo",
            "📄 Contratos y Simulador",
            "📍 Mapa de Cartera"
        ])
        
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        
        st.markdown("**v2.0 | AutoGestion Pro URU**")

    # 5. TÍTULO CENTRAL
    st.markdown('<div class="titulo-central">SISTEMA INTELIGENTE AUTOMOTRIZ URUGUAY</div>', unsafe_allow_html=True)

    # 6. Lógica de Módulos
    if opcion == "📊 Inteligencia de Negocio":
        st.write("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><h3>Intereses</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>Riesgo</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        c4.markdown('<div class="card"><h3>Cartera</h3><h2>20</h2></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Proyección de Caja (SaaS Reporting)")
        chart_data = pd.DataFrame({
            "Semana": ["S1", "S2", "S3", "S4"],
            "Esperado": [4000, 5000, 4500, 6000],
            "Real": [3800, 4200, 4450, 2000]
        }).set_index("Semana")
        st.line_chart(chart_data)

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Operaciones de Cobranza")
        tab_list, tab_agenda = st.tabs(["📋 Lista General", "📅 Agenda Proactiva"])
        
        with tab_list:
            def color_estado(val):
                if val == "VENCIDO": return 'background-color: #701010; color: white'
                if val == "AL DÍA": return 'background-color: #155123; color: white'
                return ''
            
            st.dataframe(
                df.style.map(color_estado, subset=['Estado']),
                use_container_width=True, hide_index=True,
                column_config={
                    "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
                    "Score": st.column_config.ProgressColumn("Confianza", min_value=1, max_value=5, format="%d ⭐")
                }
            )
        
        with tab_agenda:
            st.subheader("📅 Tareas Críticas de Cobranza")
            hoy = df[df["Estado"] == "VENCIDO"]
            for _, r in hoy.iterrows():
                with st.expander(f"🔴 CONTACTAR A: {r['Cliente']}"):
                    st.write(f"**Auto:** {r['Vehículo']} | **Deuda Liquidada:** ${r['Total']}")
                    st.text_area(f"Bitácora de gestión para {r['Cliente']}:", placeholder="Escribe el compromiso de pago aquí...", key=r['Cliente'])
                    if st.button(f"Guardar nota para {r['Cliente']}"):
                        st.success("Nota guardada en el historial corporativo.")

    elif opcion == "🔍 Buscador y Archivo":
        st.title("🔍 Archivo Digital Automotriz")
        search = st.text_input("Buscar cliente o vehículo...")
        if search:
            res = df[df["Cliente"].str.contains(search, case=False) | df["Vehículo"].str.contains(search, case=False)]
            for _, r in res.iterrows():
                st.markdown(f"### 👤 {r['Cliente']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Vehículo:** {r['Vehículo']}")
                    st.write(f"**Score Crediticio:** {r['Score']} / 5")
                with col_b:
                    st.file_uploader(f"Subir Contrato/DNI de {r['Cliente']}", type=["jpg", "png", "pdf"], key=f"file_{r['Cliente']}")

    elif opcion == "📄 Contratos y Simulador":
        st.title("📄 Generación de Documentos Formales")
        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("📄 Generador de PDF")
            c_sel = st.selectbox("Cliente:", df["Cliente"])
            if st.button("Generar Recibo Oficial"):
                st.success(f"PDF de Cobranza para {c_sel} generado.")
        with col_r:
            st.subheader("🧮 Simulador de Refinanciación")
            monto = st.number_input("Deuda Total USD", value=1000)
            cuotas = st.slider("Meses", 1, 12, 3)
            st.metric("Cuota Mensual", f"USD {round((monto*1.1)/cuotas, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("🗺️ Mapa Inteligente de Cartera")
        df_map = df.copy()
        df_map["color"] = df_map["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
        st.map(df_map, color="color", size=40)
        st.info("🔴 Rojo: Clientes Vencidos | 🔵 Azul: Clientes al día.")
