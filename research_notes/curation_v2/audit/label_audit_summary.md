# Auditoría semántica de etiquetas none

## Alcance y método

Se adjudicaron 750 filas: 300 de train_negatives_review.csv, 300 de human_label_review_TEMPLATE.csv y 150 filas dev con expected=ninguna de estas opciones.
Las filas del CSV humano se enlazaron con train.jsonl por pregunta exacta, ya que row_index conserva la ordenación anterior; las 300 coincidencias fueron únicas y sus candidatos coincidieron con las opciones del registro enlazado. Las 550 hard_positive_replays son positivos existentes y ninguna comparte pregunta exacta con estas filas; no se relabelaron.
Se leyeron answer.short y answer.detail de las 639 entradas únicas incluidas como gold o pool en estas filas. Los canónicos están fuera del pool en las 750 filas.

## Conteo por caso

- A · retrieval miss: 649
- B · reranking risk: 70
- C · true none: 0 (rows 3858 and 6019 reclassified C→B on 2026-11-22: otun_river_supplies_pereira states the 4000 m altitude)
- D · ambiguous / several valid / clarification: 31

Confianza: alta 709, media 27, baja 14. Las 14 filas de baja confianza quedan marcadas `review_required=true` y todas conservan `training_label_action=unchanged`; no se editaron los jsonl de entrenamiento.

## Cinco pares con más casos B/D

- `access.esperanza_murillo_corridor` ↔ `access.from_murillo`: 5 fila(s).
- `access.cedral_walk_distances` ↔ `activities.otun_cedral_walk`: 4 fila(s).
- `access.brisas_visitor_center` ↔ `access.esperanza_murillo_corridor`: 4 fila(s).
- `access.esperanza_murillo_corridor` ↔ `access.ignore_single_kilometer`: 4 fila(s).
- `access.brisas_visitor_center` ↔ `access.from_murillo`: 4 fila(s).

## Qué implica para etiquetas y ejemplos

- A: `ninguna de estas opciones` sigue siendo correcta para el pool actual; corregir el objetivo de recuperación requiere que el FAQ válido llegue al pool.
- B: usar el ID candidato que sí responde como etiqueta aceptable de esa fila; no entrenar `ninguna` cuando ya hay una respuesta completa disponible.
- C: conservar `ninguna` como respuesta; revisar el hueco de conocimiento por separado antes de crear un FAQ.
- D: no forzar una sola etiqueta si hay varias respuestas completas o falta contexto; crear ejemplos con varias etiquetas aceptables o pedir la aclaración que falta.
- Mantener contrastes de intención en ejemplos cercanos: palabras compartidas como “baños” y “baños terapéuticos” no hacen equivalentes sus respuestas.

## Pares para merge o contraste

La lista priorizada está en `findings/arbiter.json` (20 pares observados en filas B/D).
