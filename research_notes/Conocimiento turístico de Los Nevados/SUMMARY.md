# Base de conocimiento, fase 2 — PNN Los Nevados

Fecha de corte: 2026-11-21.

## Entregables

- **`knowledge_phase2.zip`**: los 15 `<id>.json` de `data/knowledge/sections/` y el conjunto de evaluación `data/knowledge/phase2/eval/`.
  - `knowledge_v1.zip` se conserva como foto de la v1. El archivo actualizado de esta entrega es `knowledge_phase2.zip`, que también incluye los 15 logs, este resumen, la validación y los hashes.
- **15 archivos `<id>.research.md`**: cada uno tiene una sección «Round 2». Tres tienen además «Coordinator final pass»: `geography`, `hours_status` y `preparation`.
- **Evidencia** en `<id>/evidence/`: los archivos descargados están en `raw/`, las citas literales en `quotes.md` y `check_quotes.py` las comprueba.
- **Coordinación** en `coordination/`: constructores, parches, decisiones de deduplicación, mapa de hard negatives y prueba de regeneración.

## Validación final de entrega

Se ejecutaron los controles estructurales después de las últimas correcciones de ejemplos.

- Los 15 JSON pasan el esquema, la unicidad de IDs y ejemplos, las referencias `related` y `featured`, y las preguntas de slots. Resultado detallado en `coordination/validation.json`.
- Se restauró el mapa de hard negatives que había quedado apartado al interrumpirse la ejecución. Se corrigieron tres destinos que ya no eran ejemplos vigentes. Todos los negativos apuntan a ejemplos de otra entrada.
- El conjunto de evaluación pasa la comprobación de JSONL, IDs existentes, preguntas duplicadas y coincidencias exactas con los ejemplos del corpus.
- No se repitieron las mediciones semánticas, la comprobación de citas ni la prueba de regeneración después de los últimos cambios. Sus informes anteriores son históricos y no certifican los bytes de esta entrega.
- El ZIP incluye un manifiesto SHA256 de sus archivos. La integridad del archivo y el esquema de los JSON empaquetados se comprobaron directamente.

La validación estructural no demuestra la exactitud de cada afirmación ni mide la precisión del asistente. No se ejecutó una evaluación final de recuperación y decisión en el teléfono.

## Entradas y ejemplos frente a la meta de la fase 2

La meta (`docs/plan-knowledge-system.md`) es de unas 900 entradas y al menos 9.000 ejemplos.

| order | espacio | v1 | fase 2 | ejemplos | perfil |
|---|---|---|---|---|---|
| 1 | `actions` | 10 | 10 | 131 | safety |
| 2 | `health_safety` | 28 | 70 | 840 | safety |
| 3 | `weather_volcano` | 16 | 54 | 685 | safety |
| 4 | `access` | 75 | 78 | 947 | procedure |
| 5 | `booking_fees` | 31 | 67 | 816 | lookup |
| 6 | `hours_status` | 38 | 40 | 505 | lookup |
| 7 | `preparation` | 53 | 34 | 516 | procedure |
| 8 | `activities` | 48 | 70 | 840 | explain |
| 9 | `rules` | 31 | 73 | 907 | rules |
| 10 | `services` | 24 | 26 | 326 | lookup |
| 11 | `fauna` | 48 | 69 | 854 | explain |
| 12 | `flora_ecosystems` | 38 | 65 | 869 | explain |
| 13 | `geography` | 50 | 61 | 744 | explain |
| 14 | `history_culture` | 45 | 59 | 712 | explain |
| 15 | `conversation` | 29 | 30 | 376 | chat |
| | **Total** | **564** | **806** (meta ~900, 90 %) | **10.068** (meta ≥ 9.000, 112 %) | |

La meta de entradas no se completó a propósito: ninguna entrada se rellenó sin una fuente leída. Cada sección deja en su `research.md` los temas que se buscaron y no tienen fuente. Bajadas a destacar:

- `preparation` pasó de 53 a 34. Se quitaron 17 consejos atribuidos sin respaldo a la ficha de PNN.
- `flora_ecosystems` se rehízo con evidencia descargada.

Todas las entradas tienen al menos 12 ejemplos.

## Conjunto de evaluación (`data/knowledge/phase2/eval/`)

Las preguntas las escribió Grok 4.7, que no es Claude. La tanda que empezó Gemini 4 Argon se canceló y la rehízo Grok. Trabajaron solo con el id, la etiqueta y la respuesta de cada entrada, sin ver los ejemplos de entrenamiento (`eval_tools.py dump`).

| Archivo | Filas | Qué mide |
|---|---|---|
| `paraphrase.<sección>.jsonl` (15) | 1.752 | La entrada correcta (`expected`). Las 806 entradas están cubiertas; incluye las alternativas añadidas a las casi copias |
| `near_miss.jsonl` | 80 | Preguntas del parque sin dato en la base (`expected: []`, la respuesta correcta es el fallback) |
| `out_of_scope.jsonl` | 80 | Preguntas ajenas al parque |

- **Casi copias:** 122 preguntas llevan `near_copy: true` y cuentan con una pregunta alternativa marcada `replaces_near_copy`. La similitud de las alternativas no se volvió a medir tras las últimas reversiones. Al medir precisión, separa las preguntas marcadas del resto.
- **Varias respuestas correctas:** 8 filas aceptan más de una entrada en `expected`, porque varias respuestas son correctas.
- **Cambios en `near_miss`:** 3 preguntas ya tienen respuesta en la base y ahora apuntan a una entrada:
  - Villahermosa → lista de municipios;
  - protocolo ante oso o puma (2 filas) → `health_safety.no_published_wildlife_protocol`;

  La pregunta sobre *Atelopus carauta* conserva `expected: []`; no se considera respondida por una lista no exhaustiva.
- **Sesgo conocido:** las preguntas se escribieron leyendo la respuesta, así que tienden a usar sus palabras. El conjunto está diseñado para medir el ruteo entre entradas. Este sesgo puede sobreestimar el rendimiento con turistas reales.

## Los vacíos más importantes

1. **Protocolo oficial ante fauna** (oso, puma, danta): no existe para el parque. `health_safety.no_published_wildlife_protocol` lo dice y da la única regla oficial: evitar el contacto.
2. **Estado actual del Ruiz:** la base explica cada color de alerta, pero no fija el vigente; remite al boletín del SGC.
3. **Rescate:** no hay línea propia de rescate, tiempos de rescate ni refugios de emergencia públicos.
4. **Reservas:** no hay política vigente de cancelación y devolución ni precio del seguro obligatorio.
5. **Senderos:** no hay duración ni dificultad oficial de los senderos, ni cupos diarios vigentes. Las cifras citan la Resolución 252 de 2008.
6. **Servicios en sitio:** faltan alquiler de equipo, cajeros, datáfono, wifi, gasolina en ruta y el estado 2026 de cabañas y camping (los datos son de 2024).
7. **Fauna menor:** de reptiles e insectos del parque no hay nombres; los anfibios vienen de un muestreo de 2014 del complejo de páramos.
8. **Flora:** no hay tasa de crecimiento del frailejón ni *Puya trianae* dentro del parque. La Resolución 1987 de 2016 es un escaneo sin texto.
9. **Preparación:** no hay lista oficial de pesos, valores R, lúmenes, equipo para niños ni plan de entrenamiento.
10. **Geografía:** no hay alturas publicadas de La Olleta, La Piraña y Nereidas, ni se sabe si los cerros Bravo, España y Machín están dentro del polígono.

## Conflictos sin resolver

En todos los casos la respuesta da las dos versiones con su fuente y remite al canal oficial.

1. **Edad máxima:** 69 años según la página de PNN y 70 según la Resolución 207 de 2023.
2. **Tarifa de buseta:** $27.500 según la página de PNN y $56.000 con el bus según la Resolución 551 de 2025.
3. **Tarifa de Quindío-Dulima:** la página dice $0 y la Resolución 551 no separa tarifas por sector.
4. **Vehículos en Brisas:** la Resolución 207 prohíbe ingresar con vehículos y la ficha de 2026 permite el carro y solo prohíbe motos.
5. **Pesca y fogatas:** el Decreto 1076 de 2015 es más permisivo que la Resolución 207, que es la que siguen las respuestas.
6. **Glaciar Conejeras:** se extinguió en «marzo de 2024» según el IDEAM y «entre diciembre de 2023 y febrero de 2024» según la página del Santa Isabel.
7. **Glaciar Santa Isabel:** el IDEAM proyecta que desaparece en 3 a 5 años y la ficha del parque cita 2028.
8. **Alturas:**
   - Santa Isabel: 4.935, 4.923 o 4.903 m (IDEAM) y 4.965 m (SGC).
   - Paramillo del Cisne-Morro Negro: 4.700 o 4.600 m.
   - Paramillo de Santa Rosa: 4.600 o 4.602 m.
9. **Oficina de PNN en Manizales:** «Calle 69 A No 24-69» según el anexo de 2023 y «Calle 68 No. 23A – 25» según una carta de 2026.
10. **Porteo:**
    - En Arenales lo prohíbe el anexo de 2023 y lo registra el informe de 2024.
    - El porteo de maletas figura solo para el sur (2023) o también para Juntas y Chilcos (2024).
11. **Horario de Juntas:** 6–10 a. m. según la Resolución 207 y 6–11 a. m. según la página de PNN.
12. **Alojamiento en Brisas:** la misma página de PNN dice en un lugar que UTON lo gestiona y en otro no lo menciona.
13. **Área del parque:**
    - Ficha de 2026: 61.388,24 ha en el encabezado y 61.410 ha en la historia.
    - CARDER: 61.410,53 ha.
    - Portal antiguo: 61.420 ha.
14. **Municipios:** la ficha vigente lista 10. La CARDER cuenta 11 sin nombrar el último, y la descripción anterior de PNN incluía Villahermosa.
15. **Ley 2505:** su redacción cambia entre las versiones descargadas.

## Datos que cambian pronto

- **Cierres por conservación:** del cuarto lunes de noviembre al viernes. En 2026 es del **23 al 27 de noviembre**.
- **Pico y Placa Ambiental:** fines de semana y festivos de noviembre hacia Brisas (Resolución 1815 del 24 de julio de 2026).
- **Tarifas 2026:** vienen de la página de PNN y de la Resolución 551 de 2025. Cambian cada año.

## Cómo se reconstruye

1. **Constructor de cada sección** (`coordination/builders.py`).
   - Siete secciones (`actions`, `access`, `hours_status`, `activities`, `services`, `geography`, `conversation`) se reconstruyen desde una foto congelada `source/<id>.v1.json` más `source/overlay.py`.
   - Las otras ocho usan su generador.
2. **`coordination/coordinator_fixes.py`**, en este orden:
   1. cruces entre secciones;
   2. parches `polish/`, luego `style/`, luego `style_final/`;
   3. fusiones;
   4. segunda pasada de parches;
   5. ejemplos retirados;
   6. mapa de hard negatives;
   7. limpieza de referencias.

   Es idempotente: una segunda corrida deja todo igual byte a byte.
3. **`coordination/validate_knowledge.py`**.

`coordination/rebuild_all.py` hace los pasos 1 y 2 y deja el resultado. `coordination/regen_test.py full|scratch` lo comprueba sin tocar el corpus. Nunca hay que editar a mano `data/knowledge/sections/*.json`.

## Riesgos y lo que no se verificó

- **Ruteo sin medir:** no se probó con el embedder completo ni en el teléfono. Los cambios de ejemplos se juzgaron con e5-base (coseno), no con la tubería real de recuperación y decisión.
- **Hard negatives elegidos por similitud:** 685 de los que se habían escrito a mano se reemplazaron por el ejemplo de otra entrada más parecido al centro de la entrada (`map_hard_negatives.py`, mediana del coseno 0,81). Algunos son flojos (por ejemplo, «cómo estás» para la identidad del asistente). Conviene revisarlos al calibrar umbrales.
- **Certificados TLS:** el Decreto 1076 de 2015 y la Ley 1333 de 2009 se descargaron sin validar el certificado (`curl -k`), porque falló la cadena del certificado del servidor.
- **Fuentes que son portadas de sitio:** son canales a los que se remite al turista (`reservasnevados.com`, el portal de PNN, `ideam.gov.co`), no fuentes de un dato.
- **Nombre común sin fuente:** «colibrí coliazul o cobrizo» (*Metallura tyrianthina*) no aparece en ninguna fuente. Ahora la etiqueta usa el nombre científico.
- **Correo corregido:** el correo `losnevados@parquesnacionales.gov.co` de `hours_status` no tenía fuente. Se corrigió a `nevados@parquesnacionales.gov.co`, que da la Resolución 207 de 2023.
