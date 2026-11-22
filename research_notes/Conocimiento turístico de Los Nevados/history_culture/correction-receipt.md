# Recibo de corrección: history_culture

Fecha: 2026-11-21. Archivo servido: `data/knowledge/sections/history_culture.json`. Entradas: 45. Ejemplos: 541. Schema: válido.

## Hallazgos de `history_culture.review.json`

1. Respuestas largas, comparaciones de fuentes y avisos no pedidos.
   Resuelto en todas las entradas, no solo en la muestra. La respuesta corta tiene una a tres frases y abre con el hecho. La comparación queda en `detail` o en el log. Se quitaron muletillas del tipo «esta guía» y «no es el plan de esta semana», salvo donde la entrada es justamente el monitoreo o las erupciones de 2012 y el visitante puede confundirlas con el boletín.

2. Ejemplos que eran notas del autor.
   Resuelto. Se reescribieron los de la muestra (`volcanology_since_1985`, `iugs_listing`, `risk_lessons`, `ruiz_natural_heritage` y los que citaban «la ficha» o «el portal» como si fueran la pregunta) y se revisó el resto. Hay coloquial, sin tildes y una o dos preguntas en inglés por entrada.

3. `iugs_listing` duplicaba `geography.geoheritage`.
   Resuelto. La entrada se eliminó y ningún `related` apunta a ella. El reconocimiento de 2022 no se repite. Quedan dos preguntas históricas distintas: Acosta, 1846, en `scientific_observers`, y el monitoreo desde 1985 en `monitoring_since_1985`, con el año 1986 de la ficha IUGS solo en el detalle.

4. `why_1985_deadly` comparaba muertos con el Pinatubo en lugar de explicar la causa.
   Resuelto. La respuesta abre con los lahares hacia zonas habitadas y con el desconocimiento, la falta de memoria, la incredulidad y la falta de institucionalidad. Pinatubo, el índice 6 y los 300 muertos están en el detalle, atados a la cifra de 25 mil de esa misma hoja y al desacuerdo con otras páginas del SGC.

5. `subject_of_rights` era larga y jurídica.
   Resuelto. La respuesta dice la protección a la vida, la salud y un ambiente sano, la representación del Presidente por medio de Parques Nacionales, y el plan conjunto. También dice que entrar hoy lo define el parque. La directriz de cero presencia humana y su modificación están en el detalle.

6. No convertir un desacuerdo de fuentes en un hecho, y no apoyar cifras de la Unesco solo con la página del operador.
   Resuelto. Muertos, VEI de 1985, ríos y velocidad se sirven como desacuerdo, no como un entero. El paisaje cafetero usa la ficha de whc.unesco.org (2011, criterios v y vi, seis paisajes, dieciocho centros) y la frase de la ficha del parque. Se quitaron 51 municipios y el 25 de junio. Las 141.120 ha y las 207.000 ha de la Unesco están en el detalle y se dicen del paisaje cafetero, no del parque.

## Alcance pedido en la misma ronda

- Agua como regulación del ecosistema: se eliminó `water_and_coffee_region`.
- Colonización antioqueña como censo del parque: se eliminó. La arquitectura de los pueblos cafeteros sigue en `bahareque`, con la ficha Unesco.
- Límites físicos y hectáreas actuales: no se sirven. La semilla 23 queda en la fecha de 1974 y en las 38.000 ha aproximadas de 1973.
- IUGS: fusionado con la retirada de `iugs_listing`.
- `related` solo local, revisado después de los borrados.

## Sin cerrar

- El gestor de la Ley 2 y la ficha SUIN no abrieron por el certificado SSL. No hay día único de la Ley 2 ni se afirma la excepción de turismo.
- No hay hora de la erupción, cifra única de muertos, velocidad medida de esa noche, cronología de Santa Isabel, censo de familias, ni horario del centro de memoria.
