"""Convierte una descripción libre en español en actividades con huella de carbono.

El punto que rompía el prototipo inicial: si no se segmenta el texto antes de buscar distancias,
una frase como "comí carne y viajé 20km en bus" le atribuye los 20 km también a la carne. Por eso
el primer paso siempre es partir el texto en segmentos por conectores (" y ", comas, puntos) y
razonar cada segmento por separado.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .factores import ALIMENTOS, HOGAR, TRANSPORTE, FactorEmision

NUMEROS_ESCRITOS = {
    "un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
}

_SEPARADORES = re.compile(r"\s+y\s+|,|;|\.|\s+luego\s+|\s+despues\s+")
_PATRON_DISTANCIA = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:km|kms|kilometros)\b")
_PATRON_CANTIDAD = re.compile(
    r"(\d+(?:[.,]\d+)?|" + "|".join(NUMEROS_ESCRITOS) + r")\s*"
    r"(?:porciones?|vasos?|tazas?|unidades?)?\s*(?:de\s+)?$"
)


@dataclass(frozen=True)
class Actividad:
    categoria: str
    etiqueta: str
    cantidad: float
    unidad: str
    factor: float

    @property
    def kg_co2e(self) -> float:
        return round(self.cantidad * self.factor, 2)


def _normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sin_tildes.lower()


def _segmentar(texto_normalizado: str) -> list[str]:
    partes = _SEPARADORES.split(texto_normalizado)
    return [parte.strip() for parte in partes if parte.strip()]


def _buscar_sinonimo(segmento: str, factor: FactorEmision) -> re.Match | None:
    for sinonimo in factor.sinonimos:
        coincidencia = re.search(r"\b" + re.escape(sinonimo) + r"\b", segmento)
        if coincidencia:
            return coincidencia
    return None


def _cantidad_antes_de(segmento: str, inicio: int) -> float:
    coincidencia = _PATRON_CANTIDAD.search(segmento[:inicio])
    if not coincidencia:
        return 1.0
    valor = coincidencia.group(1)
    return float(NUMEROS_ESCRITOS.get(valor, 0)) or float(valor.replace(",", "."))


def _detectar_transporte(segmento: str) -> Actividad | None:
    distancia = _PATRON_DISTANCIA.search(segmento)
    if not distancia:
        return None
    km = float(distancia.group(1).replace(",", "."))
    for factor in TRANSPORTE:
        if _buscar_sinonimo(segmento, factor):
            return Actividad(
                categoria="Transporte", etiqueta=factor.etiqueta,
                cantidad=km, unidad=factor.unidad, factor=factor.kg_co2e,
            )
    return None


def _detectar_categoria(
    segmento: str, categoria: str, factores: tuple[FactorEmision, ...]
) -> Actividad | None:
    for factor in factores:
        coincidencia = _buscar_sinonimo(segmento, factor)
        if coincidencia:
            cantidad = _cantidad_antes_de(segmento, coincidencia.start())
            return Actividad(
                categoria=categoria, etiqueta=factor.etiqueta,
                cantidad=cantidad, unidad=factor.unidad, factor=factor.kg_co2e,
            )
    return None


def analizar(texto: str) -> list[Actividad]:
    """Convierte una descripción en español en una lista de actividades con su huella de carbono."""
    if not texto or not texto.strip():
        return []

    actividades: list[Actividad] = []
    for segmento in _segmentar(_normalizar(texto)):
        actividad = (
            _detectar_transporte(segmento)
            or _detectar_categoria(segmento, "Alimentación", ALIMENTOS)
            or _detectar_categoria(segmento, "Hogar", HOGAR)
        )
        if actividad:
            actividades.append(actividad)

    return actividades


def total_kg_co2e(actividades: list[Actividad]) -> float:
    return round(sum(actividad.kg_co2e for actividad in actividades), 2)
