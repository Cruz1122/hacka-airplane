# Citas de `conversation` — ronda 2 (leídas el 2026-11-21)

Las citas entre «» son copias literales del texto extraído de cada página (`conversation/evidence/*.txt`, generado del HTML descargado con `actions/html_to_text.py`). `conversation/check_quotes.py` verifica que cada cita aparezca en su archivo (espacios normalizados). Ninguna respuesta de conversación da cifras, reglas ni lugares del parque: solo el nombre del parque y punteros a canales oficiales, citados abajo.

## A. Ficha Los Nevados (nombre del parque)

- URL: https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/
- Fecha de acceso: 2026-11-21
- Archivo: `conversation/evidence/www_parquesnacionales_gov_co_nuestros-parques_parque-nacional-natural-los-nevados_.txt` (HTML bruto del mismo nombre `.html`)
- Nombre: «Parque Nacional Natural Los Nevados»
- Usada en: `conversation.greeting_hello`

## B. Portada de Parques Nacionales (canales de queja y de atención)

- URL: https://www.parquesnacionales.gov.co/
- Fecha de acceso: 2026-11-21
- Archivo: `conversation/evidence/www_parquesnacionales_gov_co_.txt` (HTML bruto `www_parquesnacionales_gov_co_.html`)
- Nombre de la entidad: «Parques Nacionales Naturales de Colombia»
- Canal de atención: «Canales de atención»
- Formulario: «Formulario PQRSDF»
- Usada en: `conversation.park_complaint_channel` (formulario), `conversation.human_contact_request` (canales)
- Limitación: es la portada, no una página profunda. La página del formulario (https://pqrsd.parquesnacionales.gov.co/principal) se descargó en `conversation/evidence/pqrsd-principal.html`, pero es una aplicación de una sola página: el texto extraído es solo el título, así que no sirve como cita. Queda pendiente una URL profunda verificable.

## C. Servicio Geológico Colombiano — boletines

- URL: https://www2.sgc.gov.co/Noticias/Paginas/Boletines-semanales.aspx
- Fecha de acceso: 2026-11-21
- Archivo: `conversation/evidence/www2_sgc_gov_co_Noticias_Paginas_Boletines-semanales_aspx.txt` (HTML bruto del mismo nombre `.html`)
- Entidad: «Servicio Geológico Colombiano»
- Tipo de boletín: «Boletines de actividad volcánica»
- Usada en: `conversation.info_source_trust`

## Sin cita: hechos de la app (no del parque)

- `conversation.history_storage`: "guarda el historial … en la base de datos local de tu teléfono". Verificado en código: `mobile/src/state/history.ts` abre SQLite (`nevados.db`) en el dispositivo. No es una cita de fuente oficial.
- `conversation.offline_operation` y `conversation.ai_identity`: "funciona sin conexión" y "textos preparados guardados en tu teléfono". Coincide con la arquitectura offline de `mobile/` (skill `mobile-offline-stack`); no lo comprobé por una prueba en el dispositivo.
