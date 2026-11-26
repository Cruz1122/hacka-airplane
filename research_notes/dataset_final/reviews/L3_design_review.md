# Goal
Revisar el builder de Laya y reportar defectos verificables de retrieval, etiquetado, separación de splits y trazabilidad. No modificar las herramientas.

# Verdict
**REJECT.** Hay rutas que admiten filas sin revisión en train, mezclan procedencias y dejan incompleta la trazabilidad de la evaluación.

# Hallazgos

1. **Crítico: pares de alta similitud pueden entrar en train sin revisión de pares.** En `build_splits.py:138-142`, `pending_high_similarity` solo cambia el estado cuando `review == "auto"`. Las filas `label_audit` conservan ese estado, y el filtro en `:160` solo excluye `review == "pending_pair_review"`. Una fila de train con auditoría de etiqueta y un candidato decisivo sin juicio, con `pair_sim >= HIGH_SIM`, pasa a train. **Fix mínimo:** aplicar el bloqueo de pares pendientes con independencia de `review_status`, excepto cuando exista un juicio explícito para el par.

2. **Alto: filas de procedencia adversarial pueden ir a train.** `build_splits.py:24-25` asigna familias `X1` y `X3` a train hasta los umbrales 0.30 y 0.25; `:180-181` las marca como `provenance="adversarial"`. Por ejemplo, una familia `X1` cuyo bucket sea menor que 0.30 entra en train. **Fix mínimo:** reservar toda procedencia adversarial para evaluación y validar que ninguna fila de train la tenga.

3. **Alto: la máscara deja activa la etiqueta del FAQ dueño.** `build_dataset.py:94-96` indexa el label y sus ejemplos como textos distintos; `:106-109` enmascara solo el vector de la pregunta de ejemplo. Si un ejemplo tiene el mismo texto que su label, el label del dueño sigue con coseno 1.0 y el FAQ puede ganar por coincidencia consigo mismo. **Fix mínimo:** al enmascarar una consulta de corpus, enmascarar todos los textos de su dueño que sean idénticos tras normalización.

4. **Alto: se retienen temas de emergencia aunque el código promete mantenerlos en train.** `build_dataset.py:47,148-150` excluye del holdout solo las secciones `actions` y `conversation`; el `unseen_topic_ids` del manifiesto incluye `health_safety.unresponsive_cpr`, `health_safety.firefighters_line_119` y `health_safety.lost_person_protocol`. Esos FAQs quedan fuera de los ejemplos de train por `build_splits.py:94-99`. **Fix mínimo:** seleccionar el holdout por `kind`/tags de seguridad o por una lista de IDs protegidos, y comprobar la regla antes de exportar.

5. **Alto: el gateway de consultas enmascaradas no coincide con retrieval real.** `build_dataset.py:108-118` enmascara el vector originador antes de calcular scores de sección. `experiments/laya/retrieval.py:87-94` calcula el gateway desde `section_vecs`, sin aplicar `mask_vector`; la máscara de referencia solo altera el score de FAQ en `:72-78`. Si el ejemplo define el score de su sección, el builder puede producir un pool distinto al de la app. **Fix mínimo:** mantener el cálculo real del gateway y enmascarar el texto solo en el score de FAQ, o cambiar explícitamente la implementación de referencia.

6. **Alto: el control de casi duplicados omite la evaluación retrospectiva.** `build_splits.py:238-240` salta `retrospective_READ_ONLY` al comparar splits con train; `:267-283` coteja los splits de evaluación entre sí, pero no incluye la retrospectiva. Una fila retrospectiva y una fila unseen con coseno e5 ≥0.93 pueden quedar en ambas. **Fix mínimo:** comparar la retrospectiva con cada split y excluir la fila no retrospectiva, sin editar el archivo read-only.

7. **Alto: el manifiesto no identifica todos los datos que deciden etiquetas.** `build_splits.py:50` lee `work/pair_sim.json`, que determina `pending_high_similarity` en `:62-63`; el manifiesto de `:334-339` no guarda su hash. Cambiar ese archivo puede cambiar qué filas entran en train sin dejar evidencia en el paquete. **Fix mínimo:** registrar su hash y origen en el manifiesto, o calcular el contenido dentro del build.

8. **Medio: el conjunto de veredictos no se valida.** `build_dataset.py:161-169` carga veredictos arbitrarios; `build_splits.py:76-81` solo trata explícitamente `also_answers`, `query_dependent` y `mislabeled`. Un typo cae por la ruta sin efecto y luego `:142` puede clasificar `judged:<valor>` como verificado. **Fix mínimo:** validar cada valor al cargarlo contra el enum completo aceptado, que incluye `distinct`, `also_answers`, `query_dependent` y `mislabeled`.

9. **Medio: el histórico no recibe la validación de IDs que promete su comentario.** `build_splits.py:309-311` copia el archivo histórico verbatim y lo da por validado en `validate_dataset`; la auditoría delegada confirmó que el conjunto de `SPLITS` de ese validador no lo incluye. No queda comprobación de los IDs históricos en este build. **Fix mínimo:** incluir `historical_READ_ONLY` en la validación o quitar la afirmación y marcar el paquete histórico como fuera de validación.

# Caveat del artefacto

El `split_manifest.json` disponible no corresponde al código revisado: sus filas retrospectivas tienen `review_status: null`, mientras que `build_splits.py:224-226` asigna `eval_v2_verified`. Por eso no tomo sus conteos ni las muestras de JSONL como prueba de la salida actual. El manifiesto también informa cero filas para `checkpoint_selection`, `calibration`, `adversarial` y `final_test`; hay que regenerar el paquete para juzgar los conteos actuales.

## Alcance

- Contrasté el brief, el retrieval de referencia, los dos builders y el manifiesto disponible.
- Auditoría de comentarios delegada a `claudeAgent/claude-opus-5-5`; usé sus hallazgos como segunda revisión de restricciones y datos.
- No edité los scripts ni reconstruí el paquete.
- Throughput checkpoint: n/a, read-only investigation.
