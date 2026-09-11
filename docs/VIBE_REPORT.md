# Vibe Report — EcoTrack

## Cómo configuré las reglas del agente

Escribí `.cursorrules` (y su equivalente moderno `.cursor/rules/ecotrack.mdc`) como un contrato, no
como una lista de deseos. En vez de decir "código limpio" en abstracto, fijé decisiones concretas
que un agente puede verificar: el stack es Python + Streamlit y nada más, la lógica de negocio vive
en `ecotrack/` separada de la interfaz en `app.py`, cada factor de emisión debe citar su fuente, y
está prohibido agregar dependencias pesadas o `try/except` decorativos. También describí el flujo
esperado: resumir antes de tocar código, avanzar en pasos pequeños, y —lo más importante— que ante
un error no me pidiera depurarlo a mí, sino que propusiera la causa y el fix directamente. Esa regla
fue la que más cambió el resultado: convirtió cada bug en una conversación, no en una pausa manual.

## Dificultades al delegar el código a la IA

La primera versión del parser fallaba de una forma sutil, no ruidosa: con "Hoy comí carne y viajé
20km en bus" el total salía inflado, porque el patrón de kilómetros se buscaba sobre todo el texto y
terminaba filtrándose hacia la comida. No era un error de sintaxis que un linter atrapara; era un
error de diseño que solo aparecía al probar con el caso real del enunciado. Delegar aquí no significó
"que la IA adivine qué pasó", sino describirle el síntoma exacto y dejar que ella aislara la causa —
funcionó, pero solo porque el reporte del síntoma fue preciso. Una segunda dificultad, más
conceptual, apareció al diseñar la capa opcional de IA: el primer borrador dejaba que el modelo
calculara directamente los kg de CO2, lo cual abre la puerta a que alucine un número con apariencia
confiable. Tuve que intervenir con una regla explícita — el modelo solo identifica actividades, el
cálculo siempre pasa por los factores locales citados — porque ese tipo de error no se nota leyendo
el código, se nota cuando el dato ya está mal y alguien confió en él.

## De escribir código a orquestar una visión

Pasar de escribir cada línea a orquestar se siente menos como delegar trabajo y más como delegar
*ejecución sin delegar criterio*. Dejé de preguntarme "¿cómo implemento esta función regex?" y empecé
a preguntarme "¿qué invariante no puede romperse aquí?" — que la comida y el transporte no se mezclen
entre sí, que ningún número de emisión aparezca sin fuente, que un fallo de la IA no tumbe la app. El
tiempo se corre de teclear sintaxis a diseñar restricciones y a leer resultados con sospecha
razonable, no con fe ciega. También es más incómodo de lo que suena: se pierde el control fino
línea por línea, y esa incomodidad solo se resuelve escribiendo las reglas y las pruebas con más
cuidado del que le pondría a una función escrita a mano, precisamente porque ahora son el único lugar
donde mi intención queda fijada. El "vibe" no es escribir menos, es especificar mejor.
