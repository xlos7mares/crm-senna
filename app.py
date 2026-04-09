import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Configuración Pro 2026
st.set_page_config(page_title="Otormín Control & Gestión", page_icon="📈", layout="wide")

# Estilo CSS para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Conexión y Lógica de Datos
conn = sqlite3.connect('otormin_pro_2026.db', check_same_thread=False)
c = conn.cursor()

def inicializar_db():
    c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT, 
                  vehiculo TEXT, cuota REAL, vencimiento DATE, estado TEXT)''')
    
    c.execute("SELECT COUNT(*) FROM clientes")
    if c.fetchone()[0] == 0:
        hoy = datetime.now().date()
        # Generamos 20 ejemplos variados
        ejemplos = [
            ('Juan Pérez', '59899123456', 'Toyota Hilux SRX', 450, (hoy - timedelta(days=5))),
            ('María Rodríguez', '59898765432', 'VW Gol Trend', 210, (hoy - timedelta(days=1))),
            ('Carlos Sosa', '59891111111', 'Fiat Toro Volcano', 380, hoy),
            ('Elena Martínez', '59892222222', 'Ford Ranger XLT', 520, (hoy + timedelta(days=1))),
            ('Ricardo Gómez', '59893333333', 'Chevrolet S10', 400, (hoy + timedelta(days=2))),
            ('Lucía Fernández', '59894444444', 'Peugeot 208', 190, (hoy + timedelta(days=3))),
            ('Marcos Paz', '59895555555', 'Jeep Renegade', 310, (hoy + timedelta(days=4))),
            ('Ana Silva', '59896666666', 'Renault Kwid', 150, (hoy + timedelta(days=10))),
            ('Roberto Lugano', '59897777777', 'Hyundai HB20', 230, (hoy + timedelta(days=15))),
            ('Sofía Recoba', '59898888888', 'Suzuki Swift', 180, (hoy - timedelta(days=10))),
            ('Diego Forlán', '59899999999', 'BMW 320i', 1200, (hoy + timedelta(days=5))),
            ('Braulio López', '59891212121', 'Citroen C3', 175, (hoy + timedelta(days=2))),
            ('Valeria Lynch', '59892323232', 'Nissan Frontier', 490, (hoy - timedelta(days=3))),
            ('Jorge Drexler', '59893434343', 'Honda Civic', 350, (hoy + timedelta(days=8))),
            ('Natalia Oreiro', '59894545454', 'Audi A1', 600, (hoy + timedelta(days=12))),
            ('Edinson Cavani', '59895656565', 'Ford F-150', 950, (hoy + timedelta(days=1))),
            ('Luis Suárez', '59896767676', 'Range Rover', 1500, (hoy + timedelta(days=20))),
            ('Fede Valverde', '59897878787', 'Mercedes A200', 850, (hoy - timedelta(days=12))),
            ('Tabaré Cardozo', '59898989898', 'Fiat Cronos', 220, (hoy + timedelta(days=4))),
            ('Noelia Campo', '59899090909', 'Kia Sportage', 420, (hoy + timedelta(days=6)))
        ]
        c.executemany("INSERT INTO clientes (nombre, telefono, vehiculo, cuota, vencimiento) VALUES (?,?,?,?,?)", ejemplos)
        conn.commit()

inicializar_db()

# --- INTERFAZ ---
st.title("🚀 Otormín Control & Gestión v2.6")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3001/3001223.png", width=100)
menu = st.sidebar.radio("Navegación", ["📊 Tablero de Control", "🔍 Buscador de Clientes", "➕ Nuevo Registro"])

df = pd.read_sql_query("SELECT * FROM clientes", conn)
df['vencimiento'] = pd.to_datetime(df['vencimiento'])
hoy = datetime.now()

if menu == "📊 Tablero de Control":
    # KPIs Superiores
    atrasados = df[df['vencimiento'] < hoy]
    esta_semana = df[(df['vencimiento'] >= hoy) & (df['vencimiento'] <= hoy + timedelta(days=7))]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 EN MORA", f"{len(atrasados)} Clientes", f"${atrasados['cuota'].sum():,.0f}", delta_color="inverse")
    col2.metric("🟠 A COBRAR (7 días)", f"{len(esta_semana)} Clientes", f"${esta_semana['cuota'].sum():,.0f}")
    col3.metric("🟢 TOTAL CARTERA", f"{len(df)} Registros", f"${df['cuota'].sum():,.0f}")

    st.divider()
    
    st.subheader("⚠️ Acciones Prioritarias (Vencimientos Próximos)")
    
    prioridad = df[df['vencimiento'] <= (hoy + timedelta(days=7))].sort_values(by='vencimiento')
    
    for _, r in prioridad.iterrows():
        dias = (r['vencimiento'] - hoy).days + 1
        color = "red" if dias < 0 else "orange"
        label = "VENCIDO" if dias < 0 else f"Vence en {dias} días"
        
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.markdown(f"**{r['nombre']}** \n*{r['vehiculo']}*")
            c2.markdown(f"**Monto:** ${r['cuota']}  \n**Fecha:** {r['vencimiento'].date()}")
            
            msg = f"Hola {r['nombre']}, te escribimos de Automotora Otormín por la cuota de la {r['vehiculo']} (${r['cuota']}). ¿Cuándo podrías pasar? Saludos."
            url = f"https://wa.me/{r['telefono']}?text={msg.replace(' ', '%20')}"
            c3.markdown(f"[📲 Avisar por WhatsApp]({url})")
            st.divider()

elif menu == "🔍 Buscador de Clientes":
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
            st.success("Registrado.")
