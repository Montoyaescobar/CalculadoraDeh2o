import streamlit as st

# -------------------------------- DATOS -----------------------------------

OBJETIVO = "Distribuir el agua de forma racional según el promedio de consumo de personas para evitar escasez."
REQUERIMIENTO = "El usuario debe ingresar los litros disponibles y el número de personas por tipo."

TIPOS_PERSONA = ["Hombre", "Mujer", "Niño", "Anciano"]
CONSUMO_PROMEDIO = [50, 45, 30, 40]
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# ----------------------- FUNCIONES LÓGICAS ------------------------------

def construir_matriz_consumo(personas):
    return [[personas[i], CONSUMO_PROMEDIO[i], personas[i] * CONSUMO_PROMEDIO[i]] for i in range(len(personas))]

def calcular_total(matriz):
    return sum(fila[2] for fila in matriz)

def ajustar_distribucion(matriz, litros_disp, total_necesario):
    proporcion = litros_disp / total_necesario
    distribucion = [round(fila[1] * proporcion, 2) for fila in matriz]
    return distribucion, proporcion

def calcular_dias_restantes(agua_restante, demanda_diaria):
    if demanda_diaria == 0:
        return float('inf')
    return round(agua_restante / demanda_diaria, 2)

def consumo_por_persona_texto(matriz, distribucion=None):
    lines = []
    for i, fila in enumerate(matriz):
        nombre = TIPOS_PERSONA[i]
        if distribucion:
            lines.append(f"👤 {nombre:7}: {distribucion[i]} L por persona")
        else:
            lines.append(f"👤 {nombre:7}: {fila[1]} L por persona (consumo promedio)")
    return "\n".join(lines)

# ----------------------------- CONFIGURACION DE PÁGINA -----------------------

st.set_page_config(page_title="💧 Distribución Inteligente del Agua", layout="wide", page_icon="💧")

# ----------------------------- INYECCIÓN CSS ---------------------------

st.markdown("""
<style>
/* Fuentes */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Pacifico&display=swap');

/* Fondo claro celeste suave */
body, .stApp {
    margin:0; padding:0; min-height:100vh;
    font-family: 'Montserrat', sans-serif;
    background: linear-gradient(135deg, #d9f0ff, #a5d9ff);
    color: #1b1b1b;
}

/* Contenedor principal vidrio claro */
.container-glass {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.85);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05);
    border-radius: 24px;
    max-width: 900px;
    margin: 3rem auto 5rem auto;
    padding: 2rem 3rem;
    border: 1px solid rgba(0,0,0,0.1);
}

/* Título principal elegante */
h1.title {
    font-family: 'Pacifico', cursive;
    font-size: 3.8rem;
    font-weight: 400;
    text-align: center;
    color: #003366;
    margin-bottom: 0.2rem;
}

/* Subtítulos */
h4.subtitle {
    font-weight: 600;
    text-align: center;
    font-size: 1.3rem;
    color: #004080;
    margin-bottom: 2rem;
}

/* Tarjetas sección */
.card {
    background: rgba(255,255,255,0.9);
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    color: #1b1b1b;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,80,0.12);
}

/* Inputs labels */
.stNumberInput>div>label {
    font-weight: 600;
    margin-bottom: 0.3rem;
    color: #00509e;
}

/* Botón estilizado */
div.stButton > button {
    background: linear-gradient(45deg, #0074d9, #004080);
    border: none;
    border-radius: 15px;
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    padding: 0.7rem 2.8rem;
    box-shadow: 0 6px 20px #00408088;
    transition: all 0.35s ease;
    width: 100%;
    cursor: pointer;
    margin-top: 1rem;
}
div.stButton > button:hover {
    background: linear-gradient(45deg, #00509e, #002651);
    box-shadow: 0 8px 26px #00509eaa;
    transform: scale(1.05);
}

/* Textarea con estilo limpio */
textarea {
    background: #f0f7ff !important;
    color: #1b1b1b !important;
    border-radius: 12px !important;
    font-family: 'Consolas', monospace !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    padding: 1rem !important;
}

/* Resultados cuadro */
.result-box {
    background: #e0f0ff;
    border-left: 6px solid #00509e;
    padding: 1rem 1.5rem;
    border-radius: 15px;
    white-space: pre-wrap;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: #003366;
}

/* Resultados textos destacados */
.result-main {
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: 0.7rem;
}

/* Área scroll para historial */
.historial {
    max-height: 300px;
    overflow-y: auto;
    background: #f9fbff;
    border-radius: 15px;
    border: 1px solid #0074d9;
    padding: 1rem 1.5rem;
    box-shadow: inset 0 0 15px #00509e44;
    color: #003366;
}
.hist-item {
    border-bottom: 1px solid #0074d922;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}
.hist-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
}
.hist-item h3 {
    margin-top: 0;
    color: #00509e;
    font-weight: 700;
}

/* Expanders */
streamlit-expander > div > div:first-child {
    background: #c6dafc !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    color: #004080 !important;
    margin-bottom: 0.5rem !important;
}

/* Responsive columnas */
@media (max-width: 700px) {
    .stNumberInput > div > label {
        font-size: 0.9rem !important;
    }
    .stNumberInput > div {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- INTERFAZ -----------------------

with st.container():
    st.markdown('<div class="container-glass">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">💧 Distribución Inteligente del Agua</h1>', unsafe_allow_html=True)
    st.markdown(f'<h4 class="subtitle">Objetivo: {OBJETIVO}<br>Requerimiento: {REQUERIMIENTO}</h4>', unsafe_allow_html=True)

    # Consumo promedio como dos columnas
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Consumo promedio diario por persona")
    col1, col2 = st.columns(2)
    with col1:
        for i in range(0, len(TIPOS_PERSONA), 2):
            st.write(f"💧 {TIPOS_PERSONA[i]}: {CONSUMO_PROMEDIO[i]} L")
    with col2:
        for i in range(1, len(TIPOS_PERSONA), 2):
            st.write(f"💧 {TIPOS_PERSONA[i]}: {CONSUMO_PROMEDIO[i]} L")
    st.markdown('</div>', unsafe_allow_html=True)

    # Formulario de entrada con columnas
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("formulario_distribucion"):
        st.subheader("🧮 Ingrese datos para calcular la distribución")
        col1, col2 = st.columns(2)
        with col1:
            litros_disponibles = st.number_input("Litros de agua disponibles:", min_value=0.0, step=1.0, format="%.2f")
            personas_hombre = st.number_input("Número de hombres:", min_value=0, step=1)
            personas_nino = st.number_input("Número de niños:", min_value=0, step=1)
        with col2:
            personas_mujer = st.number_input("Número de mujeres:", min_value=0, step=1)
            personas_anciano = st.number_input("Número de ancianos:", min_value=0, step=1)
        btn_calc = st.form_submit_button("Calcular distribución")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'historial' not in st.session_state:
        st.session_state.historial = []

    if 'contador_dia' not in st.session_state:
        st.session_state.contador_dia = 0

    if btn_calc:
        personas = [personas_hombre, personas_mujer, personas_nino, personas_anciano]
        matriz = construir_matriz_consumo(personas)
        total_necesario = calcular_total(matriz)

        dia_actual = DIAS_SEMANA[st.session_state.contador_dia % len(DIAS_SEMANA)]
        st.session_state.contador_dia += 1

        if litros_disponibles >= total_necesario:
            distribucion = None
            agua_usada = total_necesario
            proporcion_uso = 1.0
        else:
            distribucion, proporcion_uso = ajustar_distribucion(matriz, litros_disponibles, total_necesario)
            agua_usada = litros_disponibles

        agua_restante = max(litros_disponibles - agua_usada, 0)
        dias_restantes = calcular_dias_restantes(agua_restante, total_necesario)

        # CUADRO 1: Demanda total y racionamiento adecuado
        st.markdown('<div class="card result-box">', unsafe_allow_html=True)
        st.markdown(f"### Demanda total y estado de racionamiento")
        estado = "✅ Agua suficiente para demanda completa." if proporcion_uso >= 1 else "⚠️ Agua insuficiente, se ajustó racionamiento."
        st.markdown(f"- **Demanda total calculada:** {total_necesario:.2f} L")
        st.markdown(f"- **Estado:** {estado}")
        st.markdown('</div>', unsafe_allow_html=True)

        # CUADRO 2: Consumo por persona
        st.markdown('<div class="card result-box">', unsafe_allow_html=True)
        st.markdown(f"### Consumo recomendado por persona")
        texto_consumo = consumo_por_persona_texto(matriz, distribucion)
        st.text_area("Consumo individual:", value=texto_consumo, height=160, key="consumo_personal_area")
        st.markdown('</div>', unsafe_allow_html=True)

        # CUADRO 3: Duración estimada agua restante
        st.markdown('<div class="card result-box">', unsafe_allow_html=True)
        st.markdown(f"### Duración estimada del agua restante")
        agua_rest_text = f"{agua_restante:.2f} L restante"
        dias_text = "Indefinido (sin demanda)" if dias_restantes == float('inf') else f"{dias_restantes} días"
        st.markdown(f"- Agua restante: **{agua_rest_text}**")
        st.markdown(f"- Estimación de días que puede durar el agua: **{dias_text}**")
        st.markdown('</div>', unsafe_allow_html=True)

        # Guardar historial para mostrar después
        nuevo_registro = {
            "día": dia_actual,
            "litros_disponibles": litros_disponibles,
            "demanda_total": total_necesario,
            "proporción_uso": proporcion_uso,
            "agua_usada": agua_usada,
            "agua_restante": agua_restante,
            "dias_restantes": dias_restantes,
            "consumo_individual": texto_consumo,
        }
        st.session_state.historial.append(nuevo_registro)

    # Historial
    if st.session_state.historial:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📅 Historial semanal de cálculos")
        st.markdown('<div class="historial">', unsafe_allow_html=True)
        for item in reversed(st.session_state.historial[-7:]):
            st.markdown('<div class="hist-item">', unsafe_allow_html=True)
            st.markdown(f"### {item['día']}")
            st.markdown(f"- 💧 Litros disponibles: **{item['litros_disponibles']} L**")
            st.markdown(f"- 📊 Demanda total: **{item['demanda_total']} L**")
            st.markdown(f"- ⚠️ Proporción de uso: **{item['proporción_uso']*100:.2f}%**")
            st.markdown(f"- 💦 Agua usada: **{item['agua_usada']:.2f} L**")
            st.markdown(f"- 💧 Agua restante: **{item['agua_restante']:.2f} L**")
            dias_rest_text = "Indefinido" if item['dias_restantes'] == float('inf') else f"{item['dias_restantes']} días"
            st.markdown(f"- ⏳ Estimación días restantes: **{dias_rest_text}**")
            with st.expander("🔍 Detalles consumo individual"):
                st.text(item["consumo_individual"])
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
