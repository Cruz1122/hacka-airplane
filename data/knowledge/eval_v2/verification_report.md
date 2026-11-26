# Informe de verificación semántica

Total: 740 filas. Verificadas: 739. Descartadas: 1. Filas con correcciones: 38.

*“Corregida” es un subconjunto de “verificada”.

### Por caso
| categoría | verificada | descartada | corregida* |
|---|---:|---:|---:|
| ambiguous | 29 | 1 | 0 |
| answerable | 549 | 0 | 37 |
| none | 161 | 0 | 1 |

### Por escenario
| categoría | verificada | descartada | corregida* |
|---|---:|---:|---:|
| clarification | 29 | 1 | 0 |
| colloquial | 60 | 0 | 7 |
| compound | 30 | 0 | 0 |
| confusable | 120 | 0 | 7 |
| english | 20 | 0 | 0 |
| long | 40 | 0 | 3 |
| natural | 150 | 0 | 11 |
| near_miss | 60 | 0 | 0 |
| out_of_scope | 80 | 0 | 0 |
| short | 40 | 0 | 5 |
| temporal | 60 | 0 | 0 |
| typo | 50 | 0 | 5 |

## Correcciones por tipo
- Añadidos a acceptable: 47 etiquetas en 38 filas.
- Retirados de acceptable: 4 etiquetas.
- Cambios de case: 1; cambios de gold: 1; cambios de escenario: 0.
- Descartes: 1 fila.

## Filas disputadas
- A-0017/A-0018: se retiró la ficha genérica de cierres; A-0017 conserva también la respuesta que prohíbe explícitamente cima y cráter del Ruiz.
- A-0081: se retiró la ficha de última inducción porque no informa la apertura a las 8:00; A-0082 la conserva porque pregunta cierre e inducción.
- A-0129, A-0179/A-0180 y A-0311/A-0312: permanecen `none`; los resultados más cercanos no confirman operador celular, Nequi ni disponibilidad actual.
- B-0236: pasó de `answerable` a `none`; la ficha del pato no cubre la petición completa de no alimentarlo.
- B-0240: se conservaron etiquetas relacionadas que informan sobre el venado conejo, dado que la consulta breve solo nombra la especie.
- B-0288, B-0333/B-0334/B-0335 y B-0359: se añadieron fichas de ruta que cubren Brisas, Arenales, Letras y el corredor La Esperanza–Murillo.
- B-0362, B-0371/B-0372/B-0373/B-0375 y B-0385: se conservaron como ambiguas porque cada una admite las interpretaciones enumeradas en `acceptable` y requiere aclaración por sección.
- B-0389: descartada; «eso» no tiene antecedente en la pregunta aislada.

## Método y validación
- Se juzgaron las filas answerable/ambiguous con `answer.short`, `answer.detail` y `answer.steps` de las 15 secciones; para `none` se revisaron resultados de búsqueda léxica y E5 sobre las 160 filas originales.
- Verificación estructural: 740 filas únicas; IDs de respuesta existentes; `gold` dentro de `acceptable` para answerable/ambiguous; `gold: null` y `acceptable: []` para none.
- Cada fila incluye evidencia breve; toda modificación de etiquetas registra valor anterior, valor nuevo y motivo.
