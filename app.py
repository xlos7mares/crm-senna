import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Configuración Pro 2026
st.set_page_config(page_title="Otormín Control & Gestión", page_icon="📈", layout="wide")

# Estilo CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Conexión y Lógica de Datos (Cambiamos el nombre de la DB para forzar el reinicio de datos)
conn = sqlite3.connect('otormin_final_v1.db', check_same_thread=False)
c = conn.cursor()

def inicializar_db():
    c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT, 
                  vehiculo TEXT, cuota REAL, vencimiento DATE)''')
    
    c.execute("SELECT COUNT(*) FROM clientes")
    if c.fetchone()[0] == 0:
        hoy = datetime.now().date()
        # 20 Ejemplos con nombres y apellidos comunes
        ejemplos = [
            ('Ricardo Méndez', '59899123456', 'Toyota Hilux SRV', 480, (hoy - timedelta(days=4))),
            ('Silvia Rodríguez', '59898765432', 'VW Gol Trend 1.6', 220, (hoy - timedelta(days=1))),
            ('Guzmán Pereira', '59891111111', 'Fiat Toro Freedom', 350, hoy),
            ('Esteban Martínez', '59892222222', 'Ford Ranger XLS', 510, (hoy + timedelta(days=1))),
            ('Valentina Gómez', '59893333333', 'Chevrolet Onix LTZ', 240, (hoy + timedelta(days=2))),
            ('Andrés Fernández', '59894444444', 'Peugeot 208 Active', 210, (hoy + timedelta(days=3))),
            ('Marcelo Paz', '59895555555', 'Jeep Renegade Sport', 330, (hoy + timedelta(days=4))),
            ('Ana Laura Silva', '59896666666', 'Renault Oroch', 290, (hoy + timedelta(days=10))),
            ('Roberto Ledesma', '59897777777', 'Hyundai HB20 S', 260, (hoy + timedelta(days=15))),
            ('Sofía González', '59898888888', 'Suzuki Swift Hybrid', 190, (hoy - timedelta(days=8))),
            ('Daniel Morales', '59899999999', 'Nissan Kicks Prime', 340, (hoy + timedelta(days=5))),
            ('Beatriz López', '59891212121', 'Citroen C3 Feel', 185, (hoy + timedelta(days=2))),
            ('Oscar Sosa', '59892323232', 'Nissan Frontier XE', 470, (hoy - timedelta(days=3))),
            ('Jorge Díaz', '59893434343', 'Honda Civic EXL', 390, (hoy + timedelta(days=8))),
            ('Patricia Olivera', '59894545454', 'Toyota Corolla XEI', 410, (hoy + timedelta(days=12))),
            ('Ignacio Santos', '59895656565', 'Ford Territory', 580, (hoy + timedelta(days=1))),
            ('Lucía Cabrera', '59896767676', 'VW Amarok V6', 750, (hoy + timedelta(days=20))),
            ('Federico Rossi', '59897878787', 'Mercedes Benz A200', 820, (hoy - timedelta(days=10))),
            ('Tabaré Cardozo', '59898989898', 'Fiat Cronos Drive', 215, (hoy + timedelta(days=4))),
            ('Mónica Duarte', '59899090909', 'Kia Niro Hybrid', 440, (hoy + timedelta(days=6)))
        ]
        c.executemany("INSERT INTO clientes (nombre, telefono, vehiculo, cuota, vencimiento) VALUES (?,?,?,?,?)", ejemplos)
        conn.commit()

inicializar_db()

# --- INTERFAZ ---
st.title("🚀 Otormín Control & Gestión v2.6")
st.sidebar.markdown("### Menú Principal")
menu = st.sidebar.radio("Ir a:", ["📊 Tablero de Control", "🔍 Buscador", "➕ Nuevo Registro"])

df = pd.read_sql_query("SELECT * FROM clientes", conn)
df['vencimiento'] = pd.to_datetime(df['vencimiento'])
hoy = datetime.now()

if menu == "📊 Tablero de Control":
    atrasados = df[df['vencimiento'] < hoy]
    esta_semana = df[(df['vencimiento'] >= hoy) & (df['vencimiento'] <= hoy + timedelta(days=7))]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 EN MORA", f"{len(atrasados)} Clientes", f"${atrasados['cuota'].sum():,.0f}")
    col2.metric("🟠 A COBRAR (7 días)", f"{len(esta_semana)} Clientes", f"${esta_semana['cuota'].sum():,.0f}")
    col3.metric("🟢 TOTAL CARTERA", f"{len(df)} Registros", f"${df['cuota'].sum():,.0f}")

    st.divider()
    st.subheader("⚠️ Acciones Prioritarias (Vencimientos Próximos)")
    
    prioridad = df[df['vencimiento'] <= (hoy + timedelta(days=7))].sort_values(by='vencimiento')
    
    for _, r in prioridad.iterrows():
        dias = (r['vencimiento'] - hoy).days + 1
        estado = "VENCIDO" if dias < 0 else f"Vence en {dias} días"
        
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.markdown(f"**{r['nombre']}** \n*{r['vehiculo']}*")
            c2.markdown(f"**Monto:** ${r['cuota']}  \n**Fecha:** {r['vencimiento'].date()}")
            
            msg = f"Hola {r['nombre']}, te escribimos de Automotora Otormín por la cuota de la {r['vehiculo']} (${r['cuota']}). ¿Cuándo podrías pasar? Saludos."
            url = f"https://wa.me/{r['telefono']}?text={msg.replace(' ', '%20')}"
            c3.markdown(f"[📲 Avisar por WhatsApp]({url})")
            st.divider()

elif menu == "🔍 Buscador":
    search = st.text_input("Buscar por nombre o vehículo...")
    if search:
        res = df[df['nombre'].str.contains(search, case=False) | df['vehiculo'].str.contains(search, case=False)]
        st.table(res[['nombre', 'vehiculo', 'cuota', 'vencimiento']])
    else:
        st.dataframe(df[['nombre', 'vehiculo', 'cuota', 'vencimiento']].sort_values(by='vencimiento'), use_container_width=True)

elif menu == "➕ Nuevo Registro":
    with st.form("nuevo"):
        st.subheader("Cargar Venta/Cuota")
        n = st.text_input("Nombre")
        t = st.text_input("Celular")
        v = st.text_input("Auto")
        m = st.number_input("Monto", min_value=0.0)
        f = st.date_input("Vencimiento")
        if st.form_submit_button("Confirmar"):
            c.execute("INSERT INTO clientes (nombre, telefono, vehiculo, cuota, vencimiento) VALUES (?,?,?,?,?)", (n, t, v, m, f))
            conn.commit()
            st.success("Registrado correctamente.")
