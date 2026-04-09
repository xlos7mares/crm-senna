import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE APARIENCIA MODO TURBO 2026
st.set_page_config(
    page_title="Otormín | Gestión Pro", 
    page_icon="🚗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS para forzar el modo oscuro y el estilo de tablero de fibra de carbono/gris oscuro
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Estilo del Sidebar (Menú lateral) */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }

    /* Tarjetas de Métricas (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Títulos y textos */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Botones de WhatsApp Estilo Premium */
    .stButton>button {
        background-color: #25D366;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #128C7E;
        transform: scale(1.02);
    }

    /* Dataframes y Tablas */
    .stDataFrame {
        border: 1px solid #333;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS PROFESIONAL
conn = sqlite3.connect('otormin_premium_v2.db', check_same_thread=False)
c = conn.cursor()

def inicializar_db():
    c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT, 
                  vehiculo TEXT, cuota REAL, vencimiento DATE)''')
    
    c.execute("SELECT COUNT(*) FROM clientes")
    if c.fetchone()[0] == 0:
        hoy = datetime.now().date()
        # 20 Ejemplos con nombres comunes y autos reales
        ejemplos = [
            ('Ricardo Méndez', '59899123456', 'Toyota Hilux SRV', 480, (hoy - timedelta(days=5))),
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

# 3. INTERFAZ DE USUARIO (UI)
# Logo y Título Central
st.markdown("<center><img src='https://otormin.uy/wp-content/uploads/2022/10/Logo-Otormin-Blanco-2.png' width='250'></center>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #bbb;'>CONTROL & GESTIÓN DE CARTERA</h2>", unsafe_allow_html=True)
st.divider()

# Menú Lateral
st.sidebar.markdown("<h3 style='text-align: center;'>MENÚ</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("", ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"])

df = pd.read_sql_query("SELECT * FROM clientes", conn)
df['vencimiento'] = pd.to_datetime(df['vencimiento'])
hoy = datetime.now()

if menu == "📊 Tablero de Control":
    # KPIs Superiores
    atrasados = df[df['vencimiento'] < hoy]
    esta_semana = df[(df['vencimiento'] >= hoy) & (df['vencimiento'] <= hoy + timedelta(days=7))]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 EN MORA", f"{len(atrasados)} Clientes", f"Total: ${atrasados['cuota'].sum():,.0f}")
    c2.metric("🟠 A COBRAR (7 DÍAS)", f"{len(esta_semana)} Clientes", f"Total: ${esta_semana['cuota'].sum():,.0f}")
    c3.metric("🟢 TOTAL CARTERA", f"{len(df)} Registros", f"Total: ${df['cuota'].sum():,.0f}")

    st.markdown("### ⚠️ Acciones de Cobranza Prioritaria")
    
    prioridad = df[df['vencimiento'] <= (hoy + timedelta(days=7))].sort_values(by='vencimiento')
    
    for _, r in prioridad.iterrows():
        dias = (r['vencimiento'] - hoy).days + 1
        etiqueta = "VENCIDO" if dias < 0 else f"Vence en {dias} días"
        color_borde = "#ff4b4b" if dias < 0 else "#ffa500"
        
        with st.container():
            col_a, col_b, col_c = st.columns([3, 2, 2])
            col_a.markdown(f"<span style='color:{color_borde}; font-weight:bold;'>{etiqueta}</span> | **{r['nombre']}**", unsafe_allow_html=True)
            col_b.markdown(f"*{r['vehiculo']}* \n**Vence:** {r['vencimiento'].date()}")
            
            # Link de WhatsApp Profesional
            msg = f"Hola {r['nombre']}, te saludamos de Automotora Otormín. Te recordamos el vencimiento de tu cuota del {r['vehiculo']} por ${r['cuota']}. ¿Podrías confirmarnos si ya realizaste el pago? Saludos."
            url = f"https://wa.me/{r['telefono']}?text={msg.replace(' ', '%20')}"
            col_c.markdown(f"[📲 Notificar WhatsApp]({url})")
            st.markdown("<hr style='margin: 10px 0; border: 0.5px solid #333;'>", unsafe_allow_html=True)

elif menu == "🔍 Buscador Inteligente":
    st.subheader("Consultar Base de Datos")
    search = st.text_input("Ingrese nombre o modelo de vehículo...")
    if search:
        res = df[df['nombre'].str.contains(search, case=False) | df['vehiculo'].str.contains(search, case=False)]
        st.dataframe(res[['nombre', 'vehiculo', 'cuota', 'vencimiento']], use_container_width=True)
    else:
        st.dataframe(df[['nombre', 'vehiculo', 'cuota', 'vencimiento']].sort_values(by='vencimiento'), use_container_width=True)

elif menu == "➕ Nuevo Registro":
    st.subheader("Carga Manual de Nuevo Cliente")
    with st.form("nuevo_form"):
        c1, c2 = st.columns(2)
        n = c1.text_input("Nombre Completo")
        t = c2.text_input("Celular (598...)")
        v = c1.text_input("Vehículo")
        m = c2.number_input("Monto de Cuota", min_value=0.0)
        f = st.date_input("Fecha de Vencimiento")
        
        if st.form_submit_button("Confirmar y Guardar"):
            c.execute("INSERT INTO clientes (nombre, telefono, vehiculo, cuota, vencimiento) VALUES (?,?,?,?,?)", (n, t, v, m, f))
            conn.commit()
            st.success("Registro añadido con éxito a la base de datos de Otormín.")

st.sidebar.divider()
st.sidebar.info("Sistema v1.1 | 2026 © Automotora Otormín - Paysandú")
