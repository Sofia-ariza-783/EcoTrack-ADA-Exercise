# Despliegue

## Repositorio

**https://github.com/Sofia-ariza-783/EcoTrack-ADA-Exercise**

## Repl en Replit

URL del Repl desplegado: `<pega aquí la URL de tu Repl, ej. https://ecotrack-ada-exercise.sofia-ariza783.replit.app>`

Configuración usada (ya incluida en el repo, se importa sola al conectar el repositorio a Replit):

1. **Create App → Import from GitHub**, pegando la URL del repositorio de arriba. Replit detecta
   `.replit` y `replit.nix` automáticamente.
2. Comando de ejecución: `streamlit run app.py --server.port 8080 --server.address 0.0.0.0`
   (definido en `.replit`).
3. Motor de IA opcional: variable `ANTHROPIC_API_KEY` en **Tools → Secrets**. Sin ella la app corre
   igual con el motor de reglas locales — el badge "⚙️ Motor activo" de la interfaz indica cuál está
   en uso.
4. **Deploy** (botón superior derecho) para publicar la URL pública.

## Captura Cursor + Replit

Colocar la imagen en `docs/capturas/04-cursor-replit.png`, mostrando el Composer/Chat de Cursor
junto al Repl desplegado ejecutando EcoTrack.

## Checklist de entregables

- [x] Código fuente funcional (`app.py`, `ecotrack/`) — probado con `pytest`.
- [x] URL del repositorio: https://github.com/Sofia-ariza-783/EcoTrack-ADA-Exercise
- [x] `.cursorrules` (raíz) y `.cursor/rules/ecotrack.mdc`.
- [x] `docs/VIBE_REPORT.md` (496 palabras).
- [x] Capturas de la app en ejecución (`docs/capturas/01-03`).
- [ ] `docs/capturas/04-cursor-replit.png` — colocar aquí la captura conjunta.
