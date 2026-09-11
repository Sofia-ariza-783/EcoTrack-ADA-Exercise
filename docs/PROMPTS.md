# Bitácora de orquestación — Fase 2 (el "Vibe" inicial)

Nota de transparencia: esta sesión se ejecutó con **Claude Code**, no con el Composer de Cursor,
porque Cursor es una herramienta de pago sin acceso disponible para este ejercicio. El flujo de
trabajo — describir la intención, dejar que el agente proponga arquitectura, iterar sobre errores
reales en vez de corregirlos a mano — es exactamente el que pide la guía para Cursor, aplicado con
otro editor agentic. `.cursorrules` y `.cursor/rules/ecotrack.mdc` quedan listos para que, si se abre
este mismo repo en Cursor, el agente herede el mismo contrato de reglas descrito aquí.

## 1. Prompt de arquitectura

> "Arma el MVP de EcoTrack: una app donde el usuario escribe algo como 'Hoy comí carne y viajé 20km
> en bus' y le devuelvo un estimado de kg de CO2. Interfaz simple, Streamlit, sin base de datos.
> Separa la lógica de negocio de la UI y cita la fuente de cada factor de emisión que uses."

**Resultado del agente:** propuso la estructura `ecotrack/factores.py` + `ecotrack/parser.py` +
`app.py`, con factores de Poore & Nemecek (2018) para alimentos y DEFRA/BEIS (2023) para transporte.
Se aceptó la propuesta tal cual — es la separación que pide `.cursorrules`.

## 2. Iteración sobre un bug real (no corregido a mano)

Primera versión del parser buscaba números de kilómetros en todo el texto sin segmentar antes. Al
probar con la frase canónica, el resultado salía inflado.

> "Con 'Hoy comí carne y viajé 20km en bus' el total no cuadra — parece que le está sumando algo de
> más a la carne. No lo arreglo yo, dime qué está pasando y corrígelo."

**Resultado del agente:** identificó que el patrón de distancia se aplicaba sobre el texto completo
en vez de por segmento, así que la carne "heredaba" la unidad de km de la frase de transporte
cuando el patrón de cantidad barría hacia atrás sin límites. La solución fue introducir
`_segmentar()` (split por " y ", comas, puntos) antes de correr cualquier detección, para que cada
cláusula se analice de forma aislada. Se agregó `test_cada_segmento_usa_su_propio_medio_de_transporte`
para que ese bug no vuelva a colarse.

## 3. Corrección de un dato inventado por el modelo

Al diseñar la capa opcional de IA (`ecotrack/ia.py`) se le pidió al modelo un primer borrador que
calculaba el kg de CO2 directamente en la respuesta del LLM.

> "No dejes que el modelo invente el número de kg de CO2 — que solo identifique la actividad y la
> cantidad, y que el cálculo final siempre pase por los mismos factores locales de
> `ecotrack.factores`, para que un dato alucinado nunca llegue a la pantalla."

**Resultado del agente:** reescribió `interpretar()` para que el LLM devuelva únicamente
`{etiqueta, cantidad}` en JSON, y esos valores se validan contra el diccionario de factores locales
antes de calcular `kg_co2e`. Si el LLM no está disponible o la respuesta no es JSON válido, cae de
vuelta al parser de reglas (`analizar()`) sin que la interfaz se entere de la diferencia.

## 4. Prompt de despliegue

> "Prepara `.replit` y `replit.nix` para que esto corra con un solo click en Replit, puerto 8080,
> sin necesidad de configurar nada manualmente aparte de pegar el repo."

**Resultado del agente:** generó `.replit` con el comando de arranque y la sección `[deployment]`
para el botón "Deploy" de Replit, `replit.nix` con Python 3.11, y `.streamlit/config.toml` con
`headless = true` para que no intente abrir un navegador local dentro del contenedor de Replit.
