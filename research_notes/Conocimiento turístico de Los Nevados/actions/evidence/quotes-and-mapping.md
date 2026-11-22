# Citas literales y mapeo a entradas — sección `actions` (corrección)

Fecha de lectura: 2026-11-21. Todas las citas fueron leídas en los archivos guardados en este directorio
(`pnn-los-nevados.txt`, `policia-123-155.txt`), extraídos con `html_to_text.py` desde el HTML descargado por `curl`.
Línea = número de línea en el `.txt` correspondiente.

## Fuente A — Policía Nacional, nota del 12 mar 2023 (`policia-123-155.txt`)

URL: https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155
Fecha de la nota: "12 March, 2023" (texto de la página). Región: Departamento de Policía Meta (nota de sensibilización).

| Cita literal | Uso |
|---|---|
| "La Línea de emergencia 123, es la línea única de emergencias Nacional" | `report_emergency_general` (short), las 8 entradas de reporte: 123 como número único |
| "gratuitamente las 24 horas del día todos los días del año" | `report_emergency_general` (short: gratuita, 24 horas) |
| "el mal uso de la línea puede evitar la atención de una emergencia real" | `report_emergency_general` (detail) |

Caveat (log): fuente de 2023. No se confirmó con una fuente oficial posterior leída. Ver `actions.research.md` §2.

## Fuente B — Parques Nacionales Naturales, ficha Los Nevados (`pnn-los-nevados.txt`)

URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/
Fecha de publicación: no indicada en la página. Contenido de 2026 (tarifas "2026", pie "© 2026"). Lectura: 2026-11-21.

| Línea | Cita literal | Uso |
|---|---|---|
| 111 | "Para el recorrido Brisas–Valle de las Tumbas … en fines de semana y puentes festivos, es indispensable reservar con al menos un día de anticipación para asegurar tu ingreso. Hazlo en: www.reservasnevados.com" | `register_planned_visit` (steps, nivel 2) |
| 144 | "Los horarios dependen del sector ecoturístico que quieras visitar y de los puntos de registro e ingreso del Parque" | `register_planned_visit` (steps), `register_arrival_today` (short y steps: registro en puntos de registro e ingreso) |
| 212 | "Ingreso al sector Brisas-Kumanday: la reserva no es obligatoria. Sin embargo, … reserva con al menos un día de anticipación." | Conflicto resuelto en log; no usado como afirmación general |
| 213 | "Ingreso a los demás sectores: la reserva sí es obligatoria. La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje." | `register_planned_visit` (steps, nivel 2) |
| 218 | "Los operadores y guías deben estar registrados … el equipo médico de respuesta y los radios con la frecuencia requerida." | `report_emergency_general`, `report_injury`, `report_lost_person`, `report_altitude_sickness`, `report_hypothermia`, `report_fire` (guía registrado: equipo médico y radios), `report_offline_emergency` (radios) |
| 218 | "es obligatorio el servicio de acompañamiento y guianza en todos los sectores" | Contexto (no citado textualmente en una entrada) |
| 106 | "todo ingreso al área protegida debe realizarse con una agencia operadora o guía … inscrito en … REPSE … y se debe adquirir un seguro obligatorio de accidentes." | Fuera de alcance de `actions` (booking_fees). No usado aquí. |

## Mapeo entrada → fuentes (final)

| Entrada | Fuente A (123) | Fuente B (PNN) | Hecho usado |
|---|---|---|---|
| register_planned_visit | — | 111, 144, 213 | puntos de registro e ingreso; reserva Brisas fin de semana/festivo; reserva obligatoria fuera de Brisas vía agencia |
| register_arrival_today | — | 144 | puntos de registro e ingreso |
| report_emergency_general | sí | 218 | 123 único, gratuito, 24 h; mal uso; guía con radios y equipo médico |
| report_injury | sí | 218 | 123; guía con equipo médico y radios |
| report_lost_person | sí | 218 | 123; guía con radios |
| report_altitude_sickness | sí | 218 | 123; guía con equipo médico |
| report_hypothermia | sí | 218 | 123; guía con equipo médico |
| report_storm | sí | 218 | 123; guía (aviso general) |
| report_fire | sí | 218 | 123; guías con radios |
| report_offline_emergency | sí | 218 | 123 con señal; guía con radios |

## Lo que NO tiene soporte y se quitó de las respuestas

- Monto del comparendo "$926.320" (Fuente A): no se usa; no es necesario para el visitante.
- Síntomas clínicos de alarma (confusión, pérdida de conocimiento, "no habla bien") como criterio médico: no hay fuente oficial de PNN o Policía; se reemplazó por "si empeora o no responde bien" (criterio genérico sin cifra).
- Instrucciones de protocolo de fuego o rayos ("aléjate", "sigue indicaciones del personal"): sin fuente; se quitaron.
- Promesas de envío, guardado o llegada a rescate: se quitaron (no transmisión de reportes).
- Teléfono de PNN (018000129722): aparece en la ficha como línea general del ciudadano, no como línea de emergencia. No se usa como emergencia.
