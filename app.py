import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# 1. Configuración de la interfaz (se adapta a celulares)
st.set_page_config(page_title="CRM Otormín", page_icon="🚗", layout="centered")

# 2. Conexión a la Base de Datos (SQLite)
# Esto crea un archivo llamado otormin_data.db donde se guarda todo
conn = sqlite3.connect('otormin_data.db', check_same_thread=False)
c = conn.cursor()

def crear_tabla():
    c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                 (nombre TEXT, telefono TEXT, vehiculo TEXT, cuota REAL, vencimiento DATE)''')
    conn.commit()

crear_tabla()

# 3. Diseño de la Aplicación
st.title("🚗 Automotora Otormín")
st.markdown("### Sistema de Gestión de Cuotas")

# Menú lateral para navegar
menu = ["🔔 Tablero de Vencimientos", "➕ Registrar Cliente", "📊 Base de Datos Completa"]
choice = st.sidebar.selectbox("Seleccione una opción", menu)

# --- OPCIÓN: REGISTRAR NUEVO CLIENTE ---
if choice == "➕ Registrar Cliente":
    st.subheader("Registrar Nuevo Vencimiento")
    with st.form("nuevo_registro"):
        nombre = st.text_input("Nombre Completo del Cliente")
        tel = st.text_input("Teléfono (Ej: 59899123456)")
        vehiculo = st.text_input("Vehículo / Modelo")
        cuota = st.number_input("Monto de la Cuota (USD / $)", min_value=0.0)
        fecha = st.date_input("Fecha de Vencimiento")
        
        boton_guardar = st.form_submit_button("Guardar en el Sistema")
        
        if boton_guardar:
            if nombre and tel:
                c.execute("INSERT INTO clientes VALUES (?,?,?,?,?)", (nombre, tel, vehiculo, cuota, fecha))
                conn.commit()
                st.success(f"¡Excelente! El vencimiento de {nombre} ha sido guardado.")
            else:
                st.error("Por favor, completa el nombre y el teléfono.")

# --- OPCIÓN: TABLERO DE VENCIMIENTOS (ALERTAS) ---
elif choice == "🔔 Tablero de Vencimientos":
    st.subheader("⚠️ Próximos Vencimientos (7 días)")
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    
    if not df.empty:
        df['vencimiento'] = pd.to_datetime(df['vencimiento'])
        hoy = datetime.now()
        
        # Filtramos los que vencen pronto (en los próximos 7 días o ya vencidos)
        proximos = df[df['vencimiento'] <= (hoy + pd.Timedelta(days=7))]
        
        if not proximos.empty:
            for i, r in proximos.iterrows():
                with st.expander(f"📌 {r['nombre']} - Vence: {r['vencimiento'].date()}"):
                    st.write(f"**Vehículo:** {r['vehiculo']}")
                    st.write(f"**Cuota:** ${r['cuota']}")
                    
                    # Lógica de WhatsApp
                    mensaje_wa = f"Hola {r['nombre']}, te recordamos el vencimiento de tu cuota del {r['vehiculo']} por un valor de ${r['cuota']}. Saludos, Automotora Otormín."
                    url_wa = f"https://wa.me/{r['tel']}?text={mensaje_wa.replace(' ', '%20')}"
                    
                    st.markdown(f"**[📲 Enviar Recordatorio por WhatsApp]({url_wa})**")
        else:
            st.info("No hay vencimientos críticos para esta semana. ¡Todo al día!")
    else:
        st.warning("Aún no hay clientes registrados en la base de datos.")

# --- OPCIÓN: VER TODO ---
elif choice == "📊 Base de Datos Completa":
    st.subheader("Listado General de Clientes")
    df_completo = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df_completo.empty:
        st.dataframe(df_completo)
    else:
        st.info("No hay datos para mostrar.")
