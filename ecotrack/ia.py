"""Capa opcional de interpretación por IA.

Si hay una `ANTHROPIC_API_KEY` configurada y el paquete `anthropic` está instalado, se le pide al
modelo que identifique las actividades del texto (mejor comprensión de frases ambiguas o mal
escritas). El modelo NUNCA inventa el factor de emisión: solo devuelve qué actividad detectó y con
qué cantidad, y ese resultado se revalúa contra los factores locales de `ecotrack.factores`. Así, un
error de la IA como "40 kg de CO2 por viajar en bus" nunca llega a mostrarse al usuario.

Sin API key, o si la llamada falla por cualquier motivo, la app sigue funcionando con el parser
local (`ecotrack.parser`) sin degradar la experiencia.
"""

from __future__ import annotations

import json
import os

from .factores import ALIMENTOS, HOGAR, TRANSPORTE, FactorEmision
from .parser import Actividad, analizar

MODELO = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

_TODOS: dict[str, FactorEmision] = {
    factor.etiqueta: factor for factor in (*ALIMENTOS, *TRANSPORTE, *HOGAR)
}


def motor_activo() -> str:
    """Nombre del motor que se usará: 'IA (Claude)' o 'Reglas locales'."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return "Reglas locales"
        return "IA (Claude)"
    return "Reglas locales"


def _prompt_sistema() -> str:
    etiquetas = ", ".join(_TODOS.keys())
    return (
        "Identifica actividades de huella de carbono en un texto en español. "
        f"Responde SOLO un JSON: una lista de objetos con 'etiqueta' (una de: {etiquetas}) "
        "y 'cantidad' (número, en km para transporte, en porciones/unidades para el resto). "
        "No incluyas texto fuera del JSON. Si no reconoces ninguna actividad, responde []."
    )


def interpretar(texto: str) -> list[Actividad]:
    """Interpreta el texto con Claude si está disponible; si no, usa el parser local."""
    if motor_activo() != "IA (Claude)":
        return analizar(texto)

    import anthropic

    cliente = anthropic.Anthropic()
    try:
        respuesta = cliente.messages.create(
            model=MODELO,
            max_tokens=512,
            system=_prompt_sistema(),
            messages=[{"role": "user", "content": texto}],
        )
        datos = json.loads(respuesta.content[0].text)
    except Exception:
        return analizar(texto)

    actividades: list[Actividad] = []
    for item in datos:
        factor = _TODOS.get(item.get("etiqueta", ""))
        if factor is None:
            continue
        try:
            cantidad = float(item["cantidad"])
        except (KeyError, TypeError, ValueError):
            continue
        categoria = (
            "Transporte" if factor in TRANSPORTE
            else "Alimentación" if factor in ALIMENTOS
            else "Hogar"
        )
        actividades.append(Actividad(categoria, factor.etiqueta, cantidad, factor.unidad, factor.kg_co2e))

    return actividades or analizar(texto)
