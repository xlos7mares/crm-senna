import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# 1. Configuración de la interfaz
st.set_page_config(page_title="CRM Otormín", page_icon="🚗", layout="centered")

# 2. Conexión a la Base de Datos
conn = sqlite3.connect('otormin_data.db', check_same_thread=False)
c = conn.cursor()

def inicializar_sistema():
    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                 (nombre TEXT, telefono TEXT, vehiculo TEXT, cuota REAL, vencimiento DATE)''')
    conn.commit()
    
    # Cargar DATOS DE EJEMPLO si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM clientes")
    if c.fetchone()[0] == 0:
        hoy = datetime.now().date()
        datos_ejemplo = [
            ('Juan Pérez', '59899123456', 'Toyota Hilux 2022', 450.0, (hoy - timedelta(days=2)).strftime('%Y-%m-%d')),
            ('María Rodríguez', '59898765432', 'VW Gol Trend', 210.0, (hoy + timedelta(days=1)).strftime('%Y-%m-%d')),
            ('Carlos Sosa', '59891111111', 'Fiat Toro Diesel', 380.0, (hoy + timedelta(days=5)).strftime('%Y-%m-%d')),
            ('Elena Martínez', '59892222222', 'Ford Ranger XLT', 520.0, (hoy + timedelta(days=20)).strftime('%Y-%m-%d'))
        ]
        c.executemany("INSERT INTO clientes VALUES (?,?,?,?,?)", datos_ejemplo)
        conn.commit()

inicializar_sistema()

# 3. Diseño de la Aplicación
st.title("🚗 Automotora Otormín")
st.markdown("### Gestión Inteligente de Cobranzas")

menu = ["🔔 Tablero de Vencimientos", "➕ Registrar Nuevo", "📊 Lista Completa"]
choice = st.sidebar.selectbox("Menú de Navegación", menu)

if choice == "🔔 Tablero de Vencimientos":
    st.subheader("⚠️ Alertas de Cobro (Próximos 7 días)")
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    
    if not df.empty:
        df['vencimiento'] = pd.to_datetime(df['vencimiento'])
        hoy = datetime.now()
        
        # Filtro: vencidos o por vencer en 7 días
        alertas = df[df['vencimiento'] <= (hoy + timedelta(days=7))]
        
        if not alertas.empty:
            for i, r in alertas.iterrows():
                # Color rojo si ya pasó, naranja si es futuro
                dias_restantes = (r['vencimiento'] - hoy).days + 1
                estado = "🔴 VENCIDO" if dias_restantes < 0 else f"🟠 Vence en {dias_restantes} días"
                
                with st.expander(f"{estado} | {r['nombre']}"):
                    st.write(f"**Vehículo:** {r['vehiculo']}")
                    st.write(f"**Cuota:** USD {r['cuota']}")
                    st.write(f"**Fecha Límite:** {r['vencimiento'].date()}")
                    
                    # Link de WhatsApp con mensaje pro
                    mensaje = f"Hola {r['nombre']}, te saludamos de Automotora Otormín. Te recordamos el vencimiento de tu cuota del {r['vehiculo']} por USD {r['cuota']}. ¿Podrías confirmarnos el pago? Gracias."
                    url_wa = f"https://wa.me/{r['telefono']}?text={mensaje.replace(' ', '%20')}"
                    
                    st.markdown(f"**[📲 ENVIAR RECORDATORIO WHATSAPP]({url_wa})**")
        else:
            st.success("✅ No hay cobros pendientes para esta semana.")

elif choice == "➕ Registrar Nuevo":
    st.subheader("Cargar nuevo plan de cuotas")
    with st.form("form"):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre Cliente")
        tel = col2.text_input("Celular (Ej: 598...)")
        vehi = col1.text_input("Vehículo")
        monto = col2.number_input("Monto Cuota", min_value=0.0)
        fec = st.date_input("Fecha Vencimiento")
        if st.form_submit_button("Guardar Registro"):
            c.execute("INSERT INTO clientes VALUES (?,?,?,?,?)", (nombre, tel, vehi, monto, fec))
            conn.commit()
            st.success("Guardado correctamente.")

elif choice == "📊 Lista Completa":
    st.subheader("Historial General")
    df_all = pd.read_sql_query("SELECT * FROM clientes ORDER BY vencimiento ASC", conn)
    st.dataframe(df_all, use_container_width=True)
