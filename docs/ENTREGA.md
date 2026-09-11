# Guía de entrega — lo que falta hacer manualmente

Todo el código, la configuración y la documentación de este repo ya están listos y probados
(`pytest tests/ -q` en verde, app corriendo en `http://localhost:8080`). Lo que sigue son los pasos
manuales que requieren cuenta/herramientas a las que esta sesión no tiene acceso: Replit y Cursor.

## 1. Repositorio en GitHub (entregable "URL del Repositorio")

Este repo ya tiene remoto configurado:

**https://github.com/Sofia-ariza-783/EcoTrack-ADA-Exercise**

Solo falta confirmar los cambios y subirlos:

```bash
git add -A
git commit -m "EcoTrack: MVP de huella de carbono + ecosistema de Vibe Coding"
git push
```

## 2. Importar y desplegar en Replit

1. En [replit.com](https://replit.com), **Create App → Import from GitHub** y pega la URL del
   repo del paso 1. Replit detecta `.replit` y `replit.nix` automáticamente.
2. Verifica que el comando de ejecución sea `streamlit run app.py --server.port 8080
   --server.address 0.0.0.0` (ya está en `.replit`) y presiona **Run**.
3. (Opcional, para el motor de IA) En **Tools → Secrets** agrega `ANTHROPIC_API_KEY` con tu clave;
   sin ella la app sigue funcionando con el motor de reglas locales — así lo confirma el badge
   "⚙️ Motor activo" que se ve en la propia interfaz.
4. Click en **Deploy** (arriba a la derecha) para obtener una URL pública `https://<repl>.replit.app`.

## 3. Las dos capturas que faltan (Cursor + Replit)

Este repo ya incluye tres capturas **reales** de la app corriendo en `docs/capturas/`
(`01-app-inicio.png`, `02-resultado-desglose.png`, `03-historial-sesion.png`), generadas
automatizando un navegador real contra el servidor local — no son mockups.

Lo que el enunciado pide además ("captura de Cursor y Replit operando en conjunto") requiere
abrir esas dos aplicaciones de escritorio/navegador, algo que esta sesión no puede hacer por no
tener licencia de Cursor. Pasos para completarlo tú misma en un par de minutos:

1. Abre este proyecto en **Cursor** y deja visible el panel de Composer/Chat a la izquierda
   (puedes pegar uno de los prompts de `docs/PROMPTS.md` para que se vea una conversación real).
2. Abre la pestaña del **Repl desplegado** (paso 2) a la derecha, mostrando la app EcoTrack
   funcionando con algún resultado calculado.
3. Toma una captura de pantalla completa que muestre ambas ventanas lado a lado y guárdala como
   `docs/capturas/04-cursor-replit.png`.

## Checklist de entregables

- [x] Código fuente funcional (`app.py`, `ecotrack/`) — probado con `pytest`.
- [x] URL del repositorio: https://github.com/Sofia-ariza-783/EcoTrack-ADA-Exercise (falta el push final, paso 1).
- [x] `.cursorrules` (raíz) y `.cursor/rules/ecotrack.mdc`.
- [x] `docs/VIBE_REPORT.md` (496 palabras).
- [x] Capturas reales de la app (`docs/capturas/01-03`).
- [ ] Captura conjunta Cursor + Replit (paso 3, pendiente de acceso a esas herramientas).
