# Recibo de corrección: activities

Fecha: 2026-11-21. Sección final: `data/knowledge/sections/activities.json`. Semilla de revisión: 20261121. Muestra original: `picnic_on_trail`, `victor_mariposa_lagoons`, `chilcos_trail`, `demanding_south`, `vehicle_or_on_foot`.

| Hallazgo | Resolución |
|---|---|
| Respuestas de la muestra con narración de fuente, comparaciones y salvedades largas | Reescritas en toda la sección: 1 a 3 frases, de tú, con el siguiente paso. Sin «la ficha dice» ni «la norma que revisé». La historia de la carta del Ruiz quedó en el detalle de `activities.ruiz_summit_closed` y en el log. |
| `demanding_south`: persona gramatical «comprometerme» y descargo de lo que el asistente no hace | Ahora pide preparación, como la ficha, y hablar con el operador antes de comprometer la cumbre. |
| Ejemplos declarativos en las 73 entradas | Sustituidos en las 49 entradas finales. Ningún ejemplo es una frase de contraste escrita por el autor. |
| Picnic: el ejemplo de dejar la basura pertenece a `rules.leave_no_waste`; la ausencia no prueba que no exista un área física | Entrada eliminada. Ese ejemplo no se conservó. Picnic, bote, esquí de paseo y caminata nocturna están en `activities.unlisted_activities` como actividades no descritas, con la orden de confirmarlas. No se afirma una prohibición. |
| `victor_mariposa_lagoons`: ejemplos de posición de ruta y de apertura actual; no dar por abiertos los senderos de 2023 | La respuesta describe el sendero al mirador, Víctor y Mariposa. Corta y variante dicen que la lista del 4 de agosto de 2023 no los deja abiertos hoy. |
| `vehicle_or_on_foot` se solapa con acceso y negaba el transporte interno por ausencia | Hecho ya resuelto y releído: la ficha dice que el parque no presta transporte interno. La respuesta lo dice, distingue el vehículo cubierto del valle y la caminata de los otros sectores, y la variante repite el hecho. No explica cómo llegar desde una ciudad. |
| Inducción a `booking_fees`; porteo como servicio a `services`; enumeración de sectores a `geography` | `activities.induction_talk` eliminada. `activities.luggage_portage` eliminada. El tope de porteo hacia Calvito y Arenales, de la Resolución 207, quedó solo dentro del pernocte y la cumbre del Tolima. `activities.four_or_five_sectors` eliminada. Los perfiles del POE corto no tienen entrada. |
| Bote, esquí, caminata nocturna, refugio y hueco de duración no deben ser varias entradas de «no hay información» ni prohibiciones inventadas | Una sola entrada, `activities.unlisted_activities`, para bote, picnic, esquí de paseo y caminata nocturna. El refugio no se declara cerrado: no se releyó el informe de 2024 y `services.refugio_cabin` ya cubre la cabaña. La duración que falta se dice en el sendero concreto cuando no hay cifra, no en una entrada aparte. |
| Restricciones y camping: la salvedad de fecha o permiso debe estar en la variante. Un anuncio en futuro no es un sendero abierto | Variantes de camping, cumbres, senderos de 2023, deportes, Ruiz y paramillos repiten la fecha o la condición. `activities.paramillo_trails_announced` cita «se habilitarán» el 6 de marzo de 2026 y dice que no se tomen como abiertos. |

Punto ya resuelto por la revisión y conservado: la ficha dice que el parque no presta transporte interno. Se mantiene, con la presentación más corta.

## Qué no quedó cerrado

- La versión íntegra del POE 2026 no se leyó. Ciclomontañismo, trail running y el trámite deportivo posterior a 2023 se responden con esa salvedad.
- No hay una fuente leída que diga si los campings y senderos de la Resolución 207 siguen abiertos en una fecha de 2026. Las respuestas piden confirmación.
- Los nombres de las 15 rutas favorables no están en el texto de la edición corta.
- La prohibición de cima y cráter del Ruiz está en la carta del 11 de mayo de 2026, que la atribuye a la Resolución 207. El cuerpo extraído de esa resolución no repite la frase. No es una contradicción escondida: el detalle de la entrada lo dice.
- La Resolución 207 prohíbe ingresar con vehículos y la ficha autoriza vehículo cubierto en Brisas. La respuesta sigue la ficha.

## Conteo final

49 entradas, 588 ejemplos, perfil `explain`, order 8. Meta de la fila: 90. Semillas 1, 7, 20, 28, 29, 33 y 40 conservadas en `what_to_visit`, `ruiz_summit_closed`, `camping_where`, `sector_santa_isabel`, `sector_tolima`, `photography_amateur` y `cloudy_visit_landscape`. jsonschema: 0 errores.
