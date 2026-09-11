"""Interfaz de EcoTrack. Toda la lógica de negocio vive en el paquete ecotrack/."""

from __future__ import annotations

import streamlit as st

from ecotrack.factores import ABSORCION_ARBOL_DIA_KG, META_DIARIA_2030_KG, PROMEDIO_MUNDIAL_DIARIO_KG
from ecotrack.ia import interpretar, motor_activo
from ecotrack.parser import Actividad, total_kg_co2e

EJEMPLOS = [
    "Hoy comí carne y viajé 20km en bus",
    "Desayuné dos huevos, comí pollo y fui 8km en bici",
    "Volé 500km en avión y comí pescado",
]

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")

if "historial" not in st.session_state:
    st.session_state.historial = []  # list[tuple[str, float]]: (texto, kg_co2e)
if "input_texto" not in st.session_state:
    st.session_state.input_texto = ""


def _usar_ejemplo(ejemplo: str) -> None:
    st.session_state.input_texto = ejemplo


st.title("🌱 EcoTrack")
st.caption("Registra tu día en lenguaje natural y descubre tu huella de carbono estimada.")
st.caption(f"⚙️ Motor activo: {motor_activo()}")

st.text_area("¿Qué hiciste hoy?", key="input_texto", placeholder=EJEMPLOS[0], height=100)

columnas_ejemplo = st.columns(len(EJEMPLOS))
for columna, ejemplo in zip(columnas_ejemplo, EJEMPLOS):
    columna.button(ejemplo, use_container_width=True, on_click=_usar_ejemplo, args=(ejemplo,))

calcular = st.button("Calcular huella de carbono", type="primary")

if calcular:
    actividades: list[Actividad] = interpretar(st.session_state.input_texto)

    if not actividades:
        st.warning(
            "No reconocí ninguna actividad. Menciona comida, transporte (con distancia en km) "
            "o consumo del hogar, por ejemplo: \"" + EJEMPLOS[0] + "\"."
        )
    else:
        total = total_kg_co2e(actividades)
        st.session_state.historial.append((st.session_state.input_texto, total))

        st.metric("Huella estimada de hoy", f"{total} kg CO2e")

        st.subheader("Desglose")
        st.table(
            [
                {
                    "Actividad": actividad.etiqueta,
                    "Cantidad": f"{actividad.cantidad:g} {actividad.unidad}",
                    "kg CO2e": f"{actividad.kg_co2e:.2f}",
                }
                for actividad in actividades
            ]
        )

        st.subheader("En contexto")
        columna_meta, columna_promedio = st.columns(2)
        columna_meta.metric("Meta diaria 2030", f"{META_DIARIA_2030_KG} kg")
        columna_promedio.metric("Promedio mundial", f"{PROMEDIO_MUNDIAL_DIARIO_KG} kg")
        st.progress(min(total / PROMEDIO_MUNDIAL_DIARIO_KG, 1.0))

        arboles = round(total / ABSORCION_ARBOL_DIA_KG)
        st.caption(f"🌳 Equivale a lo que absorben {arboles} árboles en un día.")

if st.session_state.historial:
    st.divider()
    st.subheader("Historial de esta sesión")
    st.line_chart({"kg CO2e": [kg for _, kg in st.session_state.historial]})

    encabezado = "texto,kg_co2e\n"
    filas = "\n".join(f'"{texto}",{kg}' for texto, kg in st.session_state.historial)
    st.download_button("Descargar historial (CSV)", encabezado + filas, file_name="ecotrack_historial.csv")
