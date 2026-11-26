# Citas de `actions` — ronda 2 (leídas el 2026-11-21)

Cada bloque indica la URL, la fecha de acceso y el archivo bruto (texto extraído con `actions/html_to_text.py` del HTML descargado en `actions/evidence/raw/`). Las citas entre «» son copias literales del texto extraído; `actions/check_quotes.py` verifica que cada una aparezca en su archivo (espacios normalizados). No se cita ninguna página de inicio.

## A. Policía Nacional — línea 123

- URL: https://www.policia.gov.co/noticia/policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155
- Fecha de acceso: 2026-11-21
- Archivo: `actions/evidence/raw/policia-123-155.txt` (HTML bruto: `actions/evidence/raw/policia-123-155.html`)
- Fecha de la nota: «12 March, 2023»
- Línea única: «La Línea de emergencia 123, es la línea única de emergencias Nacional»
- Servicios y gratuidad: «gratuitamente las 24 horas del día todos los días del año»
- Servicios del Estado: «todos los servicios de emergencia y seguridad que ofrece el Estado»
- Mal uso: «el mal uso de la línea puede evitar la atención de una emergencia real»

## B. Parques Nacionales — ficha Los Nevados (registro, ingreso y reservas)

- URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/
- Fecha de acceso: 2026-11-21
- Archivo: `actions/evidence/raw/pnn-los-nevados.txt` (HTML bruto: `actions/evidence/raw/pnn-los-nevados.html`; la página no tiene fecha de publicación, contiene "tarifas 2026" y "© 2026")
- Nombre del parque: «Parque Nacional Natural Los Nevados»
- Dónde se registra el ingreso: «de los puntos de registro e ingreso del Parque»
- Brisas, fines de semana (ficha línea 111, sector nombrado "Brisas–Valle de las Tumbas"): «Para el recorrido Brisas–Valle de las Tumbas (zona norte del Parque Nacional Natural Los Nevados) en fines de semana y puentes festivos, es indispensable reservar con al menos un día de anticipación»
- Brisas, otros días (ficha línea 212, sector nombrado "Brisas-Kumanday"): «Ingreso al sector Brisas-Kumanday: la reserva no es obligatoria.»
- Brisas, anticipación y enlace (línea 212): «reserva con al menos un día de anticipación»
- Enlace de reserva (línea 212): «Reserva para este atractivo en: www.reservasnevados.com»
- Otros sectores: «Ingreso a los demás sectores: la reserva sí es obligatoria.»
- Gestión en otros sectores: «La puedes gestionar a través de la agencia operadora registrada que elegiste para tu viaje.»
- Guías registrados (línea 218): «Los operadores y guías deben estar registrados»
- Equipo de guías (línea 218): «el equipo médico de respuesta y los radios con la frecuencia requerida»

## Mapeo: entrada → citas que la sostienen

| Entrada | Hecho del answer | Cita |
|---|---|---|
| `report_emergency_general` (short) | 123, línea única, gratuita, 24 h | A: línea única; A: gratuitamente 24 h |
| `report_emergency_general` (detail) | 123 como línea de emergencias y seguridad del Estado; mal uso | A: servicios del Estado; A: mal uso |
| los 7 reportes de emergencia | 123 | A: línea única; A: gratuitamente 24 h |
| `report_injury`, `report_lost_person`, `report_altitude_sickness`, `report_hypothermia`, `report_storm`, `report_fire`, `report_offline_emergency` (steps) | guía registrado con equipo médico y radios | B: Los operadores y guías deben estar registrados; B: el equipo médico de respuesta y los radios |
| `register_planned_visit` (steps 2, 1) | registro e ingreso en los puntos del parque | B: de los puntos de registro e ingreso del Parque |
| `register_planned_visit` (steps 2, 2) | Brisas: reserva indispensable en fines de semana y puentes festivos, con un día de anticipación, en reservasnevados.com | B: Brisas, fines de semana; B: enlace de reserva |
| `register_planned_visit` (steps 2, 2) | Brisas, otros días: no obligatoria, con un día de anticipación recomendado | B: Brisas, otros días; B: reserva con al menos un día de anticipación |
| `register_planned_visit` (steps 2, 2) | otros sectores: reserva obligatoria, gestionada por la agencia registrada | B: Otros sectores; B: Gestión en otros sectores |
| `register_arrival_today` | registro e ingreso en los puntos del parque | B: de los puntos de registro e ingreso del Parque |

## Sin cita oficial (instrucciones operativas de la app)

No son cifras, nombres ni reglas del parque. Quedan sin cita y se registran aquí:

- "marca el 123 cuando tengas señal": la condición de señal es lógica del teléfono; ninguna fuente lo dice. El número 123 sí está citado (A).
- "la app no avisa a rescate": límite de la app. No hay ninguna frase de envío de datos en los answers.
- "avisa de inmediato a tu guía" y "pregúntale": instrucción operativa; la capacidad del guía sí está citada (B).
