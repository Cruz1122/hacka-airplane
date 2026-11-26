# Política temporal

## Regla exacta de PLAN.md, «Operation policy»

Temporal policy: an answer about changeable state (alerts, closures, hours, fees, road status, permits) states the date of the information, never claims to know the current state, and points to the official channel. last_verified is set; valid_until only when the source gives an expiry.

## Frases modelo

- **Alertas:** «El boletín del SGC fechado [fecha] informó [nivel o actividad]. Esta respuesta no consulta alertas en tiempo real; revisa el boletín más reciente del SGC antes de salir».
- **Cierres:** «La Resolución [número y año], fechada [fecha], estableció [restricción o cierre]. No confirma si sigue aplicando a tu visita; confirma el ingreso con Parques Nacionales por [canal oficial]».
- **Horarios:** «La ficha de Parques Nacionales consultada el [fecha] publica este horario para [sector]: [horario]. No confirma la apertura en la fecha de tu visita; verifica con [canal oficial]».
- **Tarifas:** «La fuente oficial consultada el [fecha] publica [monto] para [categoría] en [año tarifario]. Confirma el monto antes de pagar en [canal oficial]».
- **Permisos y reservas:** «La Resolución [número y año] del [fecha] describe [requisito o plazo]. No garantiza cupo ni aprobación para tu visita; confirma los requisitos con Parques Nacionales o tu operador antes de viajar».

last_verified debe contener la fecha de consulta. valid_until solo se llena si la fuente expresa una fecha de vencimiento.
