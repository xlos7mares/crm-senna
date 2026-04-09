import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Control & Gestión de Cartera", layout="wide")

# 2. CSS Maestro (Modo Oscuro y Textos Blancos)
st.markdown(
    """
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        [data-testid="stSidebar"] * { color: white !important; }
        .titulo-central {
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: bold;
            margin-top: -20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Función para generar el link de WhatsApp
def crear_link_whatsapp(fila):
    # Mensaje predefinido
    texto = f"Hola {fila['Cliente']}, le recordamos que su cuota del {fila['Vehículo']} vence el {fila['Vencimiento']}. Saludos de Automotora Otormín."
    # Codificamos el texto para URL
    texto_url = urllib.parse.quote(texto)
    # Retornamos el link (usamos un número ficticio o el del cliente si lo tuvieras)
    return f"https://wa.me/59899000000?text={texto_url}"

# 4. Datos de Ejemplo (20 Clientes)
data = {
    "Cliente": [
        "Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña",
        "Lucía Méndez", "Carlos Paez", "Elena Solari", "Diego Lugano", "Sonia Britos",
        "Martín Sosa", "Valentina Ríos", "Jorge Blanco", "Carmen Díaz", "Raúl Martínez",
        "Patricia Sosa", "Gabriel Vera", "Natalia Luna", "Oscar Duarte", "Silvia Pereyra"
    ],
    "Vehículo": [
        "Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger",
        "Chevrolet Onix", "Hyundai HB20", "Peugeot 208", "Suzuki Vitara", "Renault Kwid",
        "Honda Civic", "Nissan Frontier", "Jeep Renegade", "BMW 320i", "Ford Ka",
        "Citroen C3", "VW Amarok", "Toyota Corolla", "Fiat Toro", "Chevrolet Cruze"
    ],
    "Vencimiento": [
        "2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01",
        "2026-04-20", "2026-03-28", "2026-04-05", "2026-04-12", "2026-04-18",
        "2026-03-20", "2026-04-25", "2026-04-30", "2026-05-05", "2026-04-02",
        "2026-04-08", "2026-03-15", "2026-04-22", "2026-04-28", "2026-05-10"
    ],
    "Estado": [
        "VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA",
        "AL DÍA", "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA",
        "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA", "AL DÍA",
        "AL DÍA", "VENCIDO", "AL DÍA", "AL DÍA", "AL DÍA"
    ]
}
df = pd.DataFrame(data)

# Creamos la columna de acción dinámicamente
df["Acción"] = df.apply(crear_link_whatsapp, axis=1)

# 5. Sidebar
with st.sidebar:
    st.markdown("### MENÚ")
    opcion = st.radio(
        "Navegación:",
        ["📊 Tablero de Control", "🔍 Buscador Inteligente", "➕ Nuevo Registro"],
        index=0
    )
    st.write("---")
    st.markdown("<p style='color: #55acee; font-size: 0.8rem;'>Sistema v1.1 | 2026 © Automotora Otormín</p>", unsafe_allow_html=True)

# 6. Encabezado Principal
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        pass
    st.markdown('<div class="titulo-central">CONTROL & GESTIÓN DE CARTERA</div>', unsafe_allow_html=True)

# 7. Lógica de Secciones
if opcion == "📊 Tablero de Control":
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("EN MORA", "5 Clientes", "-$2,210", delta_color="inverse")
    with c2: st.metric("A COBRAR (7 DÍAS)", "4 Clientes", "$1,850")
    with c3: st.metric("TOTAL CARTERA", "20 Registros", "$15,400")

    st.markdown("### 📋 Gestión de Cartera y Cobranza")
    
    # Configuración avanzada de la tabla
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Acción": st.column_config.LinkColumn(
                "Enviar WhatsApp",
                help="Haz clic para abrir el chat con el cliente",
                validate=r"^https://wa\.me/.*",
                display_text="📲 Enviar Mensaje"
            ),
            "Estado": st.column_config.TextColumn("Estado")
        }
    )
    
    st.info("💡 Haz clic en 'Enviar Mensaje' para simular el aviso de cobro al cliente.")
