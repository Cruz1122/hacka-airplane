# Prompt: Fase 2, investigación profunda (15 subagentes)

Adjunta tres archivos antes de pegar el prompt:

1. `conocimiento.json` (semilla de 44 temas)
2. `docs/knowledge-contract.md`
3. `docs/schemas/knowledge-section.schema.json`

---

Usa la skill de deep research. Coordina 15 subagentes en paralelo, uno por espacio de conocimiento.
Tú eres el coordinador: repartes, revisas, unificas y validas. No escribas contenido tú mismo
salvo para corregir.

## Contexto

Construimos un asistente 100 % offline para **turistas y visitantes del Parque Nacional Natural
Los Nevados (Colombia)**, que corre en un teléfono en modo avión. No genera texto libre:

- un modelo de embeddings recupera temas por similitud con los `examples`;
- un modelo de decisión elige el mejor tema;
- se devuelve la respuesta curada (`answer.short`) con su fuente.

Por eso la calidad depende de tres cosas:

1. **Ejemplos** que suenen a cómo pregunta un turista real.
2. **Respuestas** exactas y con fuente.
3. **Etiquetas** (`label`) claramente distintas entre temas.

El formato exacto está en `knowledge-contract.md` y en el schema adjunto. Es obligatorio.

Fecha de hoy: 2026-11-21.

## Los 15 espacios (un subagente por fila)

| order | id | Meta de entradas | Cubre | NO cubre (va en otro espacio) |
|---|---|---|---|---|
| 1 | `actions` | 10 | Intención de **registrar una visita** (`action: "register_visit"`) o **reportar una emergencia** (`action: "report_emergency"`), con muchas formas de pedirlo | Información sobre emergencias (`health_safety`) |
| 2 | `health_safety` | 70 | Mal de altura, aclimatación, hipotermia, sol y UV, deshidratación, refugios, números de emergencia, qué hacer si te pierdes, primeros auxilios, niños y adultos mayores en altura | Ropa (`preparation`), alertas del volcán (`weather_volcano`) |
| 3 | `weather_volcano` | 60 | Clima por temporada y altura, lluvias, niebla, nieve, niveles de alerta del Nevado del Ruiz y qué significan para el visitante, ceniza, dónde consultar boletines (SGC) | Historia de erupciones (`history_culture`) |
| 4 | `access` | 80 | Cómo llegar desde cada ciudad o pueblo (Manizales, Pereira, Ibagué, Murillo, Villamaría, Santa Rosa de Cabal, Bogotá, Medellín), vías, sectores y entradas (Brisas, Santa Isabel, Tolima, Otún), transporte público, tours, parqueo, distancias y tiempos | Precios (`booking_fees`), horarios (`hours_status`) |
| 5 | `booking_fees` | 70 | Reservas, canales, tarifas por tipo de visitante (nacional, extranjero, estudiante, niños, adultos mayores), pagos, requisitos de ingreso, edad mínima, seguro, guía obligatorio, grupos, cancelaciones | Horarios (`hours_status`) |
| 6 | `hours_status` | 40 | Horarios por sector, días de apertura, cierres temporales y por conservación, cómo saber si está abierto, temporadas altas | Clima (`weather_volcano`) |
| 7 | `preparation` | 60 | Ropa en capas, calzado, equipo, comida y agua, condición física, qué llevar con niños, qué no llevar, checklist | Salud en altura (`health_safety`) |
| 8 | `activities` | 90 | Qué visitar en cada sector, senderos (distancia, dificultad, duración), miradores, cumbres permitidas o prohibidas, cráter, acampar, fotografía, avistamiento de aves, ciclismo, actividades para niños | Reglas (`rules`) |
| 9 | `rules` | 80 | Normas para el visitante: mascotas, drones, fuego, basura, salir del sendero, recolectar plantas o rocas, alimentar fauna, ruido, alcohol, sanciones; reglamento interno redactado para el visitante | Requisitos de ingreso (`booking_fees`) |
| 10 | `services` | 40 | Centro de visitantes, baños, cafetería, señal celular, puntos de primeros auxilios, accesibilidad, alojamiento cercano, tiendas | Refugios de emergencia (`health_safety`) |
| 11 | `fauna` | 90 | Animales por grupo (aves, mamíferos, anfibios, reptiles, insectos), especies emblemáticas (cóndor andino, oso de anteojos, danta de montaña, colibríes del páramo), dónde y cuándo verlos, especies amenazadas, qué hacer si ves uno | Plantas (`flora_ecosystems`) |
| 12 | `flora_ecosystems` | 90 | Páramo, superpáramo, bosque altoandino, frailejones y otras plantas, humedales y lagunas como ecosistema, glaciares y su retroceso, ciclo del agua, conservación, cambio climático | Geografía física (`geography`) |
| 13 | `geography` | 70 | Nevados y picos (Ruiz, Santa Isabel, Tolima, Quindío, Cisne), alturas, lagunas (Otún, Verde, del Encanto), departamentos, extensión, sectores, diferencia parque vs volcán, cráter Arenas | Ecosistemas (`flora_ecosystems`) |
| 14 | `history_culture` | 70 | Erupción de 1985 y Armero, lahares, otras erupciones, nombres indígenas (Kumanday), pueblos originarios, creación del parque, comunidades campesinas, leyendas, cultura cafetera relacionada | Riesgo volcánico actual (`weather_volcano`) |
| 15 | `conversation` | 30 | Saludos, gracias, despedidas, "qué puedes hacer", "eres un robot", cambio de idioma, quejas, chistes (respuesta amable que redirige al parque) | Cualquier tema del parque |

Si un tema cabe en dos espacios, va en el de la columna "Cubre". En caso de duda, gana el espacio
con menor `order`.

## Reglas para cada subagente

### Investigación

1. **Fuentes primero oficiales:**
   - Parques Nacionales Naturales (parquesnacionales.gov.co)
   - Servicio Geológico Colombiano y Observatorio de Manizales
   - IDEAM
   - Instituto Humboldt y SiB Colombia
   - gobernaciones y alcaldías (Caldas, Risaralda, Tolima)
   - Corpocaldas, Carder y Cortolima
2. **Fuentes secundarias:** prensa reconocida, guías turísticas, eBird o iNaturalist para fauna.
   Wikipedia sirve solo para orientarse, nunca como fuente de una cifra.
3. **Horarios, precios, teléfonos, alturas y cifras** solo de una fuente oficial con fecha.
   Pon `last_verified`.
   - Si la información puede cambiar (precios, cierres, alertas), la respuesta lo dice y remite a
     la fuente oficial.
   - Si no encuentras una cifra oficial, **no la inventes**: escribe la respuesta sin la cifra y
     anótalo en el log de vacíos.
4. **Fuentes que se contradicen:** usa la más oficial y reciente, y anota el conflicto en el log.

### Entradas

1. Cada entrada es **un tema que un turista preguntaría**, no un párrafo de enciclopedia.
2. `label`: 3-8 palabras, específico y distinto de los demás del espacio. Por ejemplo,
   "tarifa para extranjeros", no "tarifas".
3. `examples`: **mínimo 12** por entrada.
   - **Mezcla de formas:**
     - consulta corta ("precio extranjeros");
     - pregunta completa;
     - coloquial colombiano ("qué vía cojo", "toca llevar guía?");
     - sin tildes o con errores ("cuanto bale");
     - 1-2 en inglés.
   - **Variedad:** nada de casi-copias; cada uno debe cambiar palabras, no solo el orden.
   - **Sin repetir:** ningún ejemplo se repite en otra entrada.
4. `hard_negatives`: 2-4 preguntas que **parecen** de esta entrada pero pertenecen a otra,
   idealmente de un espacio vecino.
5. `answer.short`: 1-3 frases, de tú, amable, concreta, con la acción a seguir.
   - `variants`: 1-2 reformulaciones.
   - `steps`: profundidad opcional para "cuéntame más".
6. `kind`, `audience`, `entities` y `needs` según el contrato.
   - `audience: "staff"` solo para información interna que no se debe responder al turista.
7. `id`: `<espacio>.<snake_case>`, único, en inglés. Por ejemplo, `booking_fees.foreign_adult_fee`.
8. `related`: 1-3 ids de temas que el turista querría después.

### Semilla

Los 44 temas de `conocimiento.json` deben quedar incluidos y mejorados en el espacio que les
corresponde según la tabla:

- conserva su contenido verificado;
- añade ejemplos hasta llegar a 12;
- corrige lo que la investigación contradiga.

### Archivo de sección

Cada subagente entrega `<id>.json` completo y válido contra el schema:

- `title` y `description`;
- `retrieval.profile`, según el contrato:
  - `lookup` para reservas, horarios y servicios;
  - `procedure` para acceso y preparación;
  - `explain` para fauna, flora, geografía, historia y actividades;
  - `rules` para reglas;
  - `safety` para salud y clima/volcán;
  - `chat` para conversación;
  - para `actions`, usa `safety`;
- `clarification`, con 4-8 preguntas de aclaración propias del espacio, plantilla `between_entries`, `slot_questions` y `fallback` amable que sugiera temas;
- `featured`: los 3-5 temas más preguntados.

### Log por espacio

Además, cada subagente entrega `<id>.research.md` con:

1. Las fuentes consultadas, con URL y fecha.
2. Vacíos: datos que no encontró de fuente oficial.
3. Conflictos entre fuentes y cómo los resolvió.
4. Temas descartados y por qué.

## Trabajo del coordinador (al final)

1. **Validar** los 15 archivos contra `knowledge-section.schema.json`. Corrige y repite hasta 0 errores.
2. **Unicidad global:**
   - ningún `id` repetido;
   - ningún ejemplo idéntico en dos entradas;
   - etiquetas casi iguales entre espacios, fusionadas o diferenciadas.
3. **Referencias:** todo `related` y `featured` apunta a un `id` existente; todo `needs` tiene su
   `slot_questions`.
4. **Cifras:** toda respuesta con números tiene `last_verified` y fuente oficial.
5. **Muestreo de calidad:** revisa 5 entradas al azar por espacio. Si alguna tiene ejemplos
   artificiales, una respuesta larga o fuente débil, devuélvesela al subagente.

## Entregables

1. 15 archivos `<id>.json`, en un zip `knowledge_v1.zip`.
2. 15 archivos `<id>.research.md`.
3. `SUMMARY.md` con:
   - entradas y ejemplos por espacio, frente a la meta;
   - totales (meta: ~900 entradas, ≥ 10.800 ejemplos);
   - los 10 vacíos más importantes;
   - los conflictos sin resolver.

No inventes datos para llegar a la meta. Es mejor quedarse corto con contenido verificado que
completar con relleno.
