# Recibo de corrección: `weather_volcano`

Revisión base: `coordination/weather_volcano.review.json`. Corrección: 2026-11-21. JSON final: `data/knowledge/sections/weather_volcano.json`.

| Hallazgo | Resolución |
|---|---|
| Cuatro entradas volcánicas citaban fuentes SGC no recuperadas como verificadas. | Consolidé actividad/alerta en `weather_volcano.ruiz_bulletins` y la limité a consultar los boletines. La página semanal sí fue leída en la evidencia local de `conversation`; no se afirma alerta o actividad actual. |
| La respuesta de colores exponía limitaciones del entorno de investigación. | Retiré `alert_levels_meaning`; no encontré una guía oficial de colores leída que sustente la explicación. |
| `park_climate`, `bimodal_rainfall` y `seasonal_weather` se solapaban. | Fusionadas en `weather_volcano.park_weather`, según el único pasaje de clima de PNN leído. |
| Los ejemplos necesitaban giros colombianos, errores/tildes y variedad. | Sustituidos por 12 ejemplos por tema, con coloquialismos colombianos, escritura acentless/errores y ejemplos naturales en inglés. |
| Ceniza mezclaba estado actual y respuesta de seguridad incompleta. | Eliminada: no se leyó orientación oficial de protección/acción para visitantes. No hay recomendación N95 ni afirmación de protección frente a gases. |
| `featured` omitía alertas/seguridad y `related` era circular. | `featured` ahora prioriza pronóstico, boletines y clima; `related` enlaza a los otros dos temas, sin autorreferencia. |

## Vacíos que siguen abiertos

- No se verificó el boletín más reciente, el estado/alerta vigente del Ruiz ni una guía oficial de colores. La sección deriva a la página SGC, pero no interpreta alertas.
- No se verificó recomendación oficial de protección ante ceniza para visitantes. El tema operativo de ceniza se excluyó.
- No se consultó pronóstico IDEAM puntual para sector/fecha; el tema solo indica dónde buscarlo.

## Resultado

3 entradas; 36 ejemplos; 6 negativos difíciles; 3 variantes; 4 preguntas de aclaración; 0 necesidades/filtros. Semilla `8` preservada en `weather_volcano.ruiz_bulletins`. Ninguna afirmación numérica en contenido de respuesta. La validación final del esquema y contrato queda registrada en el informe de entrega.
