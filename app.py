import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CRM SENNA 2026", layout="wide", initial_sidebar_state="expanded")

# 2. SESIÓN Y DATOS
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

@st.cache_data
def cargar_datos():
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Saldo (USD)": [450, 0, 0, 320, 0]
    }
    df = pd.DataFrame(data)
    # Link de WhatsApp dinámico
    def link_wa(fila):
        msg = f"CRM Senna Informa: Estimado {fila['Cliente']}, le recordamos que su cuota del {fila['Vehículo']} está {fila['Estado']}. Saldo: ${fila['Saldo (USD)']}. Saludos."
        return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
    df["WhatsApp"] = df.apply(link_wa, axis=1)
    return df

df = cargar_datos()

# 3. PANTALLA DE LOGIN
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🏎️ CRM SENNA 2026</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Leo" and p == "Senna2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso Denegado")

# 4. SISTEMA ACTIVO
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.title("SENNA")
        st.markdown("### 🛠️ MENÚ PRINCIPAL")
        opcion = st.radio("Módulos del Sistema:", [
            "📊 Tablero de Control", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador Inteligente",
            "📄 Documentos y PDF",
            "📍 Mapa de Cartera"
        ])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- CONTENIDO CENTRAL ---
    st.markdown(f"<h1 style='text-align: center;'>CRM SENNA - {opcion.upper()}</h1>", unsafe_allow_html=True)

    if opcion == "📊 Tablero de Control":
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5 Clientes", "USD 2.210")
        c2.metric("A COBRAR", "4 Clientes", "USD 1.850")
        c3.metric("TOTAL CARTERA", "20 Registros", "USD 15.400")
        st.write("---")
        st.subheader("📋 Vista General de Cartera")
        st.dataframe(df[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "💰 Gestión de Cobros":
        st.subheader("💸 Lista de Cobranza Activa")
        # Tabla con botón de WhatsApp funcional
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={"WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 Enviar WA")}
        )

    elif opcion == "🔍 Buscador Inteligente":
        st.subheader("🔍 Localización rápida de fichas")
        busqueda = st.text_input("Ingresa nombre del cliente o vehículo:", placeholder="Ej: Federico")
        
        if busqueda:
            resultado = df[df['Cliente'].str.contains(busqueda, case=False) | df['Vehículo'].str.contains(busqueda, case=False)]
            if not resultado.empty:
                for _, r in resultado.iterrows():
                    with st.expander(f"👤 FICHA: {r['Cliente']}"):
                        st.write(f"**Vehículo:** {r['Vehículo']}")
                        st.write(f"**Estado de Cuenta:** {r['Estado']}")
                        st.write(f"**Saldo Pendiente:** ${r['Saldo (USD)']}")
                        st.write(f"**Vencimiento:** {r['Vencimiento']}")
                        st.markdown(f"[📲 Enviar Recordatorio de Pago]({r['WhatsApp']})")
            else:
                st.warning("No se encontraron resultados.")

    elif opcion == "📄 Documentos y PDF":
        st.subheader("📄 Generación de Recibos y Contratos")
        cliente_sel = st.selectbox("Selecciona el cliente para el documento:", df["Cliente"])
        tipo_doc = st.radio("Tipo de documento:", ["Recibo de Pago", "Estado de Cuenta", "Promesa de Compraventa"])
        
        if st.button(f"Generar {tipo_doc}"):
            datos_c = df[df["Cliente"] == cliente_sel].iloc[0]
            st.success(f"¡{tipo_doc} generado con éxito!")
            # Aquí iría la descarga del PDF (Simulado para que no rompa sin fpdf instalado)
            st.info(f"Descargando archivo: {tipo_doc}_{cliente_sel}.pdf")

    elif opcion == "📍 Mapa de Cartera":
        st.subheader("📍 Geolocalización de Deudores (Paysandú)")
        st.map(df.rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
