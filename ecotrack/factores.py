"""Factores de emisión de CO2 equivalente usados por el parser y la capa de IA.

Fuentes:
- Alimentos (kg CO2e por porción de referencia, ~150 g cocido salvo huevo/leche/café):
  Poore, J. & Nemecek, T. (2018), "Reducing food's environmental impacts through producers
  and consumers", Science 360(6392) — promedios globales de ciclo de vida por producto.
- Transporte (kg CO2e por km-pasajero): UK DEFRA/BEIS, "Greenhouse gas reporting: conversion
  factors 2023", categoría de factores de transporte de pasajeros.
- Hogar: estimaciones de referencia de la EPA (kWh) y promedios divulgativos usados por
  calculadoras de huella de carbono de uso doméstico (ducha, lavadora, aire acondicionado).

Estos números son promedios globales orientativos para un prototipo educativo, no mediciones
certificadas para reporte regulatorio.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactorEmision:
    etiqueta: str
    kg_co2e: float
    unidad: str
    sinonimos: tuple[str, ...]


ALIMENTOS: tuple[FactorEmision, ...] = (
    FactorEmision("Carne de res", 6.61, "porción", ("carne de res", "carne", "res", "bistec", "hamburguesa")),
    FactorEmision("Cordero", 3.67, "porción", ("cordero",)),
    FactorEmision("Cerdo", 1.08, "porción", ("cerdo", "puerco", "chuleta")),
    FactorEmision("Pollo", 0.92, "porción", ("pollo", "gallina")),
    FactorEmision("Pescado", 0.81, "porción", ("pescado", "atun", "salmon", "mariscos")),
    FactorEmision("Queso", 0.63, "porción", ("queso",)),
    FactorEmision("Leche", 0.75, "vaso", ("leche",)),
    FactorEmision("Huevo", 0.27, "unidad", ("huevo", "huevos")),
    FactorEmision("Arroz", 0.40, "porción", ("arroz",)),
    FactorEmision("Café", 0.28, "taza", ("cafe",)),
    FactorEmision("Vegetales / vegetariano", 0.06, "porción", ("vegetales", "verduras", "ensalada", "vegetariano", "vegano")),
)

TRANSPORTE: tuple[FactorEmision, ...] = (
    FactorEmision("Avión", 0.246, "km", ("avion", "vuelo", "volar")),
    FactorEmision("Taxi / app de transporte", 0.212, "km", ("taxi", "uber", "didi", "cabify")),
    FactorEmision("Auto particular", 0.171, "km", ("carro", "auto", "coche", "automovil")),
    FactorEmision("Motocicleta", 0.113, "km", ("moto", "motocicleta")),
    FactorEmision("Bus urbano", 0.105, "km", ("bus", "autobus", "camion", "colectivo", "guagua")),
    FactorEmision("Tren", 0.035, "km", ("tren",)),
    FactorEmision("Metro", 0.028, "km", ("metro", "subte")),
    FactorEmision("Bicicleta / caminando", 0.0, "km", ("bicicleta", "bici", "caminando", "caminar", "a pie")),
)

HOGAR: tuple[FactorEmision, ...] = (
    FactorEmision("Ducha con agua caliente", 0.50, "ducha", ("ducha", "bañarme con agua caliente", "regaderazo")),
    FactorEmision("Lavadora", 0.60, "carga", ("lavadora", "lavado de ropa")),
    FactorEmision("Aire acondicionado", 0.50, "hora", ("aire acondicionado", "aire acondicionador", "clima")),
    FactorEmision("Electricidad", 0.35, "kWh", ("kwh", "electricidad")),
)

TODOS_LOS_FACTORES: tuple[FactorEmision, ...] = ALIMENTOS + TRANSPORTE + HOGAR

# Contexto para comparar el resultado en la interfaz.
META_DIARIA_2030_KG = 6.3
"""Huella diaria per cápita compatible con el objetivo de 2.3 t CO2e/año a 2030 (referencia divulgativa)."""

PROMEDIO_MUNDIAL_DIARIO_KG = 12.9
"""Huella diaria per cápita promedio mundial aproximada (~4.7 t CO2e/año)."""

ABSORCION_ARBOL_DIA_KG = 0.058
"""Un árbol adulto absorbe ~21 kg de CO2 al año (~0.058 kg/día), cifra divulgativa de referencia."""
