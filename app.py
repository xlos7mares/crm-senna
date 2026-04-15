import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime, timedelta
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
# Volvemos a CRM Senna 2026
st.set_page_config(
    page_title="CRM Senna 2026 - Control Total",
    page_icon="🏎️",
    layout="wide"
)

# 2. INICIALIZACIÓN DEL ESTADO DE SESIÓN (Control de acceso)
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    # Estética profesional para el Login (Modo Oscuro)
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

    # Centramos el formulario de login
    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        st.write("#") # Espacio superior
        try:
            # Intentamos cargar el logo (asegúrate de que esté en GitHub)
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            # Fallback si no hay logo
            st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA</h1>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center;'>🔐 Acceso al Panel de Control</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8899A6;'>Plataforma Inteligente Automotriz - Nivel 2026</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            btn_login = st.form_submit_button("INGRESAR AL SISTEMA")
            
            if btn_login:
                # Credenciales unificadas
                if user == "Leo" and password == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos. Intenta de nuevo.")

# --- PANTALLA PRINCIPAL (Solo visible tras el Login exitoso) ---
else:
    # Estética Profesional CRM (Modo Oscuro Senna)
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
                font-size: 2.5rem;
                font-weight: bold;
                margin-top: -20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. Datos y Lógica de Inteligencia (Ejemplo para Demo)
    @st.cache_data
    def cargar_datos_demo():
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
        # Cálculo de mora (2% simulado)
        df["Mora"] = df.apply(lambda x: round(x["Cuota (USD)"] * 0.02, 2) if x["Estado"] == "VENCIDO" else 0, axis=1)
        df["Total"] = df["Cuota (USD)"] + df["Mora"]
        
        # WhatsApp firmado por CRM Senna
        def link_wa(fila):
            msg = f"CRM Senna Informa: Estimado {fila['Cliente']}, le recordamos que su cuota por el {fila['Vehículo']} se encuentra {fila['Estado']}. Saldo total liquidado: ${fila['Total']}. Saludos."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos_demo()

    # 4. Sidebar con Logo y Navegación
    with st.sidebar:
        try:
            logo_side = Image.open("logo.png")
            st.image(logo_side, use_container_width=True)
        except:
            # Fallback si no hay logo
            st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA</h1>", unsafe_allow_html=True)
        
        st.markdown(f"### 👤 Usuario: **Leo**")
        st.write("---")
        
        # Opciones de Navegación Unificadas
        opcion = st.radio("Módulos de Control:", [
            "📊 Dashboard Inteligente", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador y Archivo Digital",
            "📄 Documentos y Simulador",
            "📍 Mapa de Cartera"
        ])
        
        st.write("---")
        # Botón para cerrar sesión
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        
        st.markdown("<p style='color: #8899A6; font-size: 0.8rem;'>v2.2 | CRM Senna © 2026</p>", unsafe_allow_html=True)

    # 5. TÍTULO CENTRAL (Branding Restablecido)
    st.markdown('<div class="titulo-central">CRM SENNA 2026</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899A6; margin-top: -10px;'>Plataforma Inteligente de Control Total Automotriz</p>", unsafe_allow_html=True)
    st.write("---")

    # 6. Lógica de Módulos (Exactamente igual, 10 funciones inteligentes)

    if opcion == "📊 Dashboard Inteligente":
        st.subheader("Estado del Negocio en Tiempo Real")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown('<div class="card"><h3>Efectividad</h3><h2 style="color:#00ff00">84%</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><h3>Intereses Mora</h3><h2 style="color:#55acee">${df["Mora"].sum()}</h2></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>Riesgo Cartera</h3><h2 style="color:#ff4b4b">BAJO</h2></div>', unsafe_allow_html=True)
        c4.markdown('<div class="card"><h3>Unidades</h3><h2>20</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📈 Proyección de Caja vs. Cobros Reales")
        # Datos simulados para gráfico
        chart_data = pd.DataFrame({
            "Semana": ["S1", "S2", "S3", "S4"],
            "Proyección": [4000, 5000, 4500, 6000],
            "Cobrado": [3800, 4200, 4450, 2000] # El bajón de la S4 simula morosidad
        }).set_index("Semana")
        st.line_chart(chart_data)

    elif opcion == "💰 Gestión de Cobros":
        st.title("💸 Operaciones de Cobranza Directa")
        
        # Pestañas internas para organización
        tab_list, tab_agenda = st.tabs(["📋 Lista General", "📅 Agenda Proactiva (IA)"])
        
        with tab_list:
            # Función para dar color a las celdas de Estado
            def color_estado(val):
                if val == "VENCIDO": return 'background-color: #701010; color: white'
                if val == "AL DÍA": return 'background-color: #155123; color: white'
                return ''
            
            # Mostramos la tabla principal con estilos y configuración de columnas
            st.dataframe(
                df.style.map(color_estado, subset=['Estado']),
                use_container_width=True, hide_index=True,
                column_config={
                    "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
                    "Score": st.column_config.ProgressColumn("Confianza", min_value=1, max_value=5, format="%d ⭐")
                }
            )
            st.info("💡 Haz clic en 'WhatsApp' para enviar un recordatorio automático con el monto adeudado.")
        
        with tab_agenda:
            st.subheader("📅 Tareas Críticas de Cobranza para Hoy")
            hoy = df[df["Estado"] == "VENCIDO"]
            if not hoy.empty:
                st.warning(f"🔔 Alerta IA: {len(hoy)} Clientes requieren contacto inmediato.")
                for _, r in hoy.iterrows():
                    with st.expander(f"🔴 CONTACTAR A: {r['Cliente']}"):
                        st.write(f"**Vehículo:** {r['Vehículo']} | **Deuda Liquidada:** ${r['Total']}")
                        # Bitácora de gestión (Simulada, no guarda persistentemente en esta demo)
                        st.text_area(f"Bitácora de gestión para {r['Cliente']}:", placeholder="Escribe el compromiso de pago aquí...", key=f"nota_{r['Cliente']}")
                        if st.button(f"Guardar nota para {r['Cliente']}", key=f"btn_{r['Cliente']}"):
                            st.success("Nota guardada en el historial corporativo (Simulación).")
            else:
                st.success("✅ No hay cobros críticos pendientes para hoy.")

    elif opcion == "🔍 Buscador y Archivo Digital":
        st.title("🔍 Archivo Digital Automotriz (Digital Vault)")
        search = st.text_input("Buscar cliente o vehículo...", placeholder="Ej: Federico Rossi")
        
        if search:
            # Filtramos los datos
            res = df[df["Cliente"].str.contains(search, case=False) | df["Vehículo"].str.contains(search, case=False)]
            
            if not res.empty:
                for _, r in res.iterrows():
                    with st.expander(f"👤 Ficha Completa: {r['Cliente']}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Vehículo:** {r['Vehículo']}")
                            st.write(f"**Estado de Cuenta:** {r['Estado']}")
                            st.write(f"**Saldo Total:** ${r['Total']}")
                        with col_b:
                            st.write(f"**Score Crediticio:** {r['Score']} / 5")
                            # Función de Archivo Digital (Simulada)
                            st.file_uploader(f"Digitalizar documento para {r['Cliente']} (Contrato/DNI)", type=["jpg", "png", "pdf"], key=f"file_{r['Cliente']}")
            else:
                st.warning("No se encontraron coincidencias.")

    elif opcion == "📄 Documentos y Simulador":
        st.title("📄 Herramientas de Cierre y Legal")
        
        tab_pdf, tab_sim = st.tabs(["📄 Generar PDF Oficial", "🧮 Simulador de Cuotas"])
        
        with tab_pdf:
            st.subheader("📄 Generador de PDF Profesional")
            c_sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
            # Función de PDF (Simulada en esta demo)
            if st.button("Generar y Descargar Recibo Oficial (Demo)"):
                st.success(f"PDF Profesional de Cobranza para {c_sel} generado correctamente. (Simulación)")
        
        with tab_sim:
            st.subheader("🧮 Simulador de Refinanciación Crediticia (IA Assisted)")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                monto = st.number_input("Deuda Total a Financiar (USD)", min_value=100.0, value=1000.0)
                cuotas = st.slider("Plazo (Meses)", 1, 12, 3)
            with col_s2:
                tasa = st.number_input("Tasa mensual (%) - Sugerida IA: 2.0%", value=2.0)
                # Cálculo simulado
                total_con_interes = monto * (1 + (tasa/100 * cuotas))
                cuota_mensual = total_con_interes / cuotas
                
                st.metric("Cuota Mensual", f"USD {round(cuota_mensual, 2)}")
                st.write(f"**Total final a cobrar:** USD {round(total_con_interes, 2)}")

    elif opcion == "📍 Mapa de Cartera":
        st.title("🗺️ Mapa Inteligente de Cartera y Deuda")
        st.write("Visualiza la ubicación geográfica de tus deudores activos en Paysandú.")
        
        # Preparamos los datos para que el mapa los entienda
        df_map = df.copy()
        
        # Creamos una columna de color: Rojo para Vencidos, Azul para Al Día
        df_map["color"] = df_map["Estado"].apply(lambda x: "#FF0000" if x == "VENCIDO" else "#0000FF")
        
        # Mostramos el mapa con los colores personalizados
        # Nota: En una app real, 'latitude' y 'longitude' vendrían de una API de geolocalización real
        st.map(df_map, color="color", size=40)
        st.info("🔴 Rojo: Clientes con deuda vencida. | 🔵 Azul: Clientes al día.")
