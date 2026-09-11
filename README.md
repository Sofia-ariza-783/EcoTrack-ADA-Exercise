# EcoTrack 🌱

MVP de EcoTrack: describe tu día en lenguaje natural ("Hoy comí carne y viajé 20km en bus") y la
app estima tu huella de carbono en kg de CO2 equivalente. Proyecto integrador de configuración de
un ecosistema de Vibe Coding (Cursor + Replit + agente de IA).

## Correr localmente

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8080`. La app funciona sin ninguna clave configurada (motor de reglas
locales); si defines `ANTHROPIC_API_KEY` en el entorno, usa Claude para interpretar el texto y el
badge "⚙️ Motor activo" de la interfaz cambia a "IA (Claude)".

## Correr las pruebas

```bash
python -m pip install pytest
python -m pytest tests/ -q
```

## Estructura

| Ruta | Contenido |
|---|---|
| `app.py` | Interfaz Streamlit (solo presentación). |
| `ecotrack/factores.py` | Factores de emisión de CO2 con su fuente citada. |
| `ecotrack/parser.py` | Interpreta el texto en español y calcula la huella. |
| `ecotrack/ia.py` | Capa opcional que usa Claude para interpretar frases ambiguas. |
| `tests/test_parser.py` | Pruebas del parser (casos del enunciado incluidos). |
| `.cursorrules` / `.cursor/rules/ecotrack.mdc` | Reglas del agente de IA para este proyecto. |
| `.replit` / `replit.nix` / `.streamlit/config.toml` | Configuración de ejecución y deploy en Replit. |
| `docs/VIBE_REPORT.md` | Reflexión sobre el flujo de Vibe Coding (entregable). |
| `docs/PROMPTS.md` | Bitácora de los prompts usados para construir el MVP. |
| `docs/ENTREGA.md` | Registro de despliegue: repositorio, Repl y capturas. |
| `docs/PARA_EL_REVISOR.md` | Guía de lectura del repo para quien evalúe el ejercicio. |
| `docs/capturas/` | Capturas reales de la app en ejecución. |

## Entregables del ejercicio

1. **URL del repositorio** — https://github.com/Sofia-ariza-783/EcoTrack-ADA-Exercise
2. **`.cursorrules`** — en la raíz de este repo.
3. **Vibe Report** — `docs/VIBE_REPORT.md`.
4. **Capturas** — `docs/capturas/` (app real y captura conjunta Cursor + Replit).
