import streamlit as st

# ---------------------- OBJETIVOS Y REQUERIMIENTOS ------------------------

OBJETIVO = "Distribuir el agua de forma racional según el promedio de consumo de personas para evitar escasez."
REQUERIMIENTO = "El usuario debe ingresar los litros disponibles y el número de personas por tipo."

# ------------------------- CONSUMO PROMEDIO -------------------------------

# Lista con el tipo de personas
tipos_persona = ["Hombre", "Mujer", "Niño", "Anciano"]

# Lista con el consumo promedio (en litros por día) [Hombre, Mujer, Niño, Anciano]
consumo_promedio = [50, 45, 30, 40]

# ------------------------- FUNCIONES DEL PROGRAMA -------------------------

def construir_matriz_consumo(personas):
    matriz = []
    for i in range(len(personas)):
        fila = [personas[i], consumo_promedio[i], personas[i] * consumo_promedio[i]]
        matriz.append(fila)
    return matriz

def calcular_total(matriz):
    total = sum(fila[2] for fila in matriz)
    return total

def ajustar_distribucion(matriz, litros_disponibles, total_necesario):
    proporcion = litros_disponibles / total_necesario
    distribucion = []
    for fila in matriz:
        litros_por_persona = fila[1] * proporcion
        distribucion.append(round(litros_por_persona, 2))
    return distribucion, proporcion

def mostrar_resultados(matriz, litros_disponibles, total_necesario, distribucion=None):
    resultados = []
    resultados.append(f"Total de litros disponibles: {litros_disponibles} L")
    resultados.append(f"Demanda total calculada: {total_necesario} L\n")

    for i, fila in enumerate(matriz):
        nombre = tipos_persona[i]
        if distribucion:
            resultados.append(f"{nombre:<8}: {fila[0]} personas x {distribucion[i]} L = {fila[0]*distribucion[i]:.2f} L")
        else:
            resultados.append(f"{nombre:<8}: {fila[0]} personas x {fila[1]} L = {fila[2]:.2f} L")

    if distribucion:
        resultados.append("\nDistribución ajustada debido a escasez de agua.")
    else:
        resultados.append("\nEl agua es suficiente. Distribución estándar aplicada.")

    return "\n".join(resultados)

# ----------------------------- INICIO DEL PROGRAMA ---------------------------

st.title("Sistema de Distribución de Agua")
st.write(f"**Objetivo:** {OBJETIVO}")
st.write(f"**Requerimiento:** {REQUERIMIENTO}")

st.header("Promedio de consumo diario por persona:")
for tipo, consumo in zip(tipos_persona, consumo_promedio):
    st.write(f"  • {tipo}: {consumo} L")

litros_disponibles = st.number_input("Litros de agua disponibles:", min_value=0.0, step=1.0)
personas_hombre = st.number_input("Número de hombres:", min_value=0, step=1)
personas_mujer = st.number_input("Número de mujeres:", min_value=0, step=1)
personas_nino = st.number_input("Número de niños:", min_value=0, step=1)
personas_anciano = st.number_input("Número de ancianos:", min_value=0, step=1)

if st.button("Calcular distribución"):
    personas = [personas_hombre, personas_mujer, personas_nino, personas_anciano]
    matriz = construir_matriz_consumo(personas)
    total_necesario = calcular_total(matriz)

    if litros_disponibles >= total_necesario:
        resultados = mostrar_resultados(matriz, litros_disponibles, total_necesario)
    else:
        distribucion_ajustada, proporcion = ajustar_distribucion(matriz, litros_disponibles, total_necesario)
        resultados = mostrar_resultados(matriz, litros_disponibles, total_necesario, distribucion_ajustada)

    st.text_area("Resultados:", value=resultados, height=300)
