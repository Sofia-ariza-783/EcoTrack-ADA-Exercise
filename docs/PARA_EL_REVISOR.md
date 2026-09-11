# Guía de revisión — EcoTrack

Nota para quien evalúe este repositorio (persona o IA): esta guía indica en qué orden leer el
proyecto y qué archivo respalda cada criterio de la rúbrica, para no tener que inferirlo navegando
al azar.

## Orden de lectura sugerido

1. `README.md` — qué es el proyecto, cómo correrlo, mapa de archivos.
2. `.cursorrules` (y su equivalente `.cursor/rules/ecotrack.mdc`) — reglas de arquitectura y estilo
   fijadas para el agente de IA antes de escribir código.
3. `ecotrack/factores.py` — datos base: factores de emisión con su fuente citada.
4. `ecotrack/parser.py` — la lógica central: convierte una frase en español en actividades con
   huella de carbono. El docstring del módulo explica el bug que motivó el diseño (segmentar antes
   de buscar distancias).
5. `ecotrack/ia.py` — capa opcional que delega la interpretación a Claude sin delegarle el cálculo.
6. `app.py` — interfaz Streamlit; nótese que no contiene lógica de negocio, solo la consume.
7. `tests/test_parser.py` — casos de prueba, incluido el ejemplo textual del enunciado
   ("Hoy comí carne y viajé 20km en bus" → 8.71 kg CO2e).
8. `docs/PROMPTS.md` — bitácora de los prompts reales usados para construir el MVP y cómo se
   resolvieron los problemas que aparecieron, sin corregir código a mano.
9. `docs/VIBE_REPORT.md` — la reflexión pedida en la Fase 3 del ejercicio.
10. `docs/capturas/` — evidencia visual de la app funcionando y del ecosistema Cursor + Replit.

## Cómo verificar que funciona (no solo que "se ve bien")

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest tests/ -q      # 6 pruebas, deben pasar
streamlit run app.py            # abre http://localhost:8080
```

## Qué criterio respalda cada parte

- **Integridad del ecosistema** → `.cursorrules`, `.cursor/rules/ecotrack.mdc`, `.replit`,
  `replit.nix`, `.streamlit/config.toml` y `docs/capturas/04-cursor-replit.png`.
- **Ejecución técnica / orquestación** → `ecotrack/` + `tests/` (funciona y está probado) y
  `docs/PROMPTS.md` (evidencia de que los errores se resolvieron delegando a la IA, no a mano).
- **Mentalidad de Vibe Coding** → `docs/VIBE_REPORT.md`.
