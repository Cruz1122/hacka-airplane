# actions curator — decision log

## Environment proof (2026-11-22, before curation)

- (a) `fetch_evidence.py` OK: HTTP 200, `research_notes/curation_v2/evidence/actions/policia-123-2023.txt`, sha256_raw `a59fd71569c26b0e15f59ba84ca38e70d4e4b968c747c4b1a2419d48caf2e007`, fetched_at `2026-11-22T16:30:19+00:00`.
- (b) `uv run python --version` OK: Python 3.14.8.
- (c) `knowledge.py inspect --id actions.report_emergency_general` OK: `"status": "ok"`, `needs: []`, `action: report_emergency`.
- Second fetch also OK (not required for the canary): `pnn-los-nevados-ficha.txt` HTTP 200, fetched_at `2026-11-22T16:32:22+00:00`.


## Operaciones

- `actions.register_planned_visit` update: el paso mezclaba Brisas–Valle de las Tumbas (reserva indispensable en fin de semana y festivo) con Brisas-Kumanday (no obligatoria). Ahora cita cada nombre, dice que la ficha no confirma el día de la visita y nombra la Resolución 1815 del 24 de julio de 2026 sin copiar el horario. Evidencia: `research_notes/curation_v2/evidence/actions/pnn-los-nevados-ficha.txt`.
- `actions.register_arrival_today` update: solo metadatos. Etiqueta igual. Hard negatives de Letras, el atajo del mapa y la reserva. Sin evidencia.
- `actions.report_emergency_general` update: la definición del 123 queda fechada al 12 de marzo de 2023; la instrucción de marcar va primero; `needs` sigue vacío; la app no avisa a rescate. Evidencia: `research_notes/curation_v2/evidence/actions/policia-123-2023.txt` y `pnn-los-nevados-ficha.txt`.
- `actions.report_injury` update: etiqueta de reporte en la app, hard negatives de denuncia ambiental y persona perdida, fecha del 123. Misma evidencia de Policía y ficha.
- `actions.report_lost_person` update: se distingue de objeto perdido y de “me perdí”. Se conservó “no encuentro a mi grupo” porque al quitarla la entrada salía del top 3. Evidencia: solo `policia-123-2023.txt`.
- `actions.report_altitude_sickness` update: contraste con síntomas en niños e hipotermia; fecha del 123. No se quitó “persona con dolor de cabeza fuerte en la cumbre” porque es hard negative de `flora_ecosystems.glaciers_snow_presence`. Evidencia: Policía y ficha.
- `actions.report_hypothermia` update: se quitaron dos síntomas que piden primeros auxilios; fecha del 123. Evidencia: Policía y ficha.
- `actions.report_storm` update: hard negatives de nieve, granizo y rayo; fecha del 123. Evidencia: Policía y ficha.
- `actions.report_fire` update: contraste con el incendio de Romerales y con la emergencia genérica; fecha del 123. Evidencia: Policía y ficha.
- `actions.report_offline_emergency` update: sin señal la app no avisa a rescate; fecha del 123; `needs` vacío. Evidencia: Policía y ficha.

Las ocho emergencias conservan `needs: []`. Ninguna promete transmisión, rastreo ni despacho.

## No comprobado, huecos, descargas, cruces

- Entradas sin revisar: ninguna. Las 10 tienen fila en `audit/actions.csv`.
- Hueco: no hay página nacional posterior al 12 de marzo de 2023. La nota es de la Policía del Meta. No se afirma cobertura de hoy.
- Hueco: la ficha pide 3 días hábiles en Cisne y Otún y 5 en Quindío-Dulima. No se copiaron; quedan en `booking_fees`.
- Hueco: no hay entrada de “consultar un reporte”. `knowledge.py` solo admite `register_visit` y `report_emergency`. El clon `get_emergency_report_status` describe un reporte enviado; el execute solo guarda un código local (`src/nevados_bench/world/model.py`, `mobile/src/state/history.ts`). El texto del FSM dice “quedó enviado” (`src/nevados_bench/fsm/driver.py`). La respuesta no lo repite.
- Descargas fallidas: ninguna.
- Cruces: `research_notes/curation_v2/findings/actions.cross.json` (5).
- `route_check`: `n_removed_not_routing` = 0 (6 ejemplos quitados siguen en el top 3 de su entrada). `stage`: `status` staged, warnings vacíos. `verify_evidence`: `fail` [].
