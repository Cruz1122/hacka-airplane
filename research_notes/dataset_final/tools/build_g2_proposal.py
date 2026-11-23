import json, subprocess, sys
from pathlib import Path

ROOT = Path('/home/cruz1122/dev/hacka-airplane')
W = ROOT / 'research_notes/dataset_final'

def get_entry(eid):
    res = subprocess.run(['uv', 'run', 'python', str(ROOT / '.claude/skills/add-park-knowledge/scripts/knowledge.py'), '--root', str(ROOT), 'inspect', '--id', eid], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)['entry']

# Build operations
operations = []

# 1. geography.park_area
e = get_entry('geography.park_area')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'Hay tres cifras oficiales: 61.388,24 hectáreas en el encabezado de la ficha de Parques Nacionales, 61.410 hectáreas en su apartado de historia y 61.410,53 hectáreas según la Carder (julio de 2026). No se toma una sola como única extensión.',
    'variants': [
        'Las publicaciones oficiales reportan tres cifras de extensión: 61.388,24 hectáreas en el encabezado de la ficha de Parques Nacionales, 61.410 hectáreas en su historia y 61.410,53 hectáreas según la Carder en 2026.'
    ],
    'detail': 'El encabezado de la ficha oficial de Parques Nacionales indica 61.388,24 ha, mientras que el párrafo de historia de la misma ficha señala 61.410 hectáreas en diez municipios. A su vez, la Carder, el 14 de julio de 2026, registra 61.410,53 hectáreas. Ninguna fuente anula a las otras y no se promedian.'
}
ev_park_area = [
    {
        'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
        'path': 'research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/pnn_ficha_nevados.txt',
        'quote': 'Extensión total\n61.388,24 ha',
        'checked_on': '2026-11-22'
    },
    {
        'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
        'path': 'research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/pnn_ficha_nevados.txt',
        'quote': 'área geográfica de 61.410 hectáreas distribuidas en diez municipios: Santa Rosa de Cabal, Pereira,',
        'checked_on': '2026-11-22'
    },
    {
        'url': 'https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/',
        'path': 'research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/carder_pnn_nevados_2026.txt',
        'quote': 'de 1974, y cuenta con una extensión de 61.410,53 hectáreas distribuidas entre los departamentos de',
        'checked_on': '2026-11-22'
    },
    {
        'url': 'https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/',
        'path': 'research_notes/Conocimiento turístico de Los Nevados/geography/evidence/raw/carder_pnn_nevados_2026.txt',
        'quote': 'Pereira, 14 de julio de 2026.',
        'checked_on': '2026-11-22'
    }
]
operations.append({
    'op': 'update',
    'reason': 'Presentar las tres extensiones oficiales publicadas (encabezado PNN, historia PNN y CARDER) sin fijar una sola como vigente.',
    'entry': e,
    'evidence': ev_park_area
})

# Common evidence for booking_fees admission
ev_pnn_admission = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Quindío-Dulima\n*Estos valores no incluyen el seguro obligatorio de accidentes, que debe ser asumido por el visitante y pagado a través de la agencia o guía ecoturístico de su elección.\n0\n0\n0\nNo aplica\nSegún el guía o la agencia operadora registrada que se elija.',
    'checked_on': '2026-11-22'
}
ev_pnn_admission_rates = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Cisne-Poleka Kasue y Laguna del Otún\n*Estos valores no incluyen el seguro obligatorio de accidentes, que debe ser asumido por el visitante y pagado a través de la agencia o guía ecoturístico de su elección.\n12.500\n24.500\n68.000',
    'checked_on': '2026-11-22'
}
ev_pnn_admission_brisas = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Brisas-Kumanday\n*Estos valores no incluyen el seguro obligatorio de accidentes, que debe ser asumido por el visitante y pagado a través de la concesión Unión Temporal Operación Nevados (UTON).\n12.500\n24.500\n68.000',
    'checked_on': '2026-11-22'
}
ev_res551_header = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt',
    'quote': 'RESOLUCIÓN 551\n\nDE 19 DE DICIEMBRE DE 2025\n\n“Por medio de la cual se actualiza el valor de los derechos de ingreso y\nservicios complementarios a las áreas protegidas del Sistema de Parques\nNacionales Naturales de Colombia y se unifican disposiciones.”',
    'checked_on': '2026-11-22'
}
ev_res551_vigencia = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt',
    'quote': 'ARTÍCULO 22. – La presente resolución rige a partir del primero de enero de\n2026 y deroga a partir de esta fecha las disposiciones que le sean contrarias,\nentre éstas, la Resolución 695 de 2024 .\nDada en Bogotá D.C., a los 19\n\ndías del mes de diciembre de 2025.',
    'checked_on': '2026-11-22'
}
ev_res551_rates = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt',
    'quote': '$12.500\n\n$24.500\n\n$68.000\n\nVía Parque Isla de Salamanca.\nParque Nacional Naturales Los\nNevados.',
    'checked_on': '2026-11-22'
}

# 2. booking_fees.under25_admission_fee
e = get_entry('booking_fees.under25_admission_fee')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'En 2026, la ficha de Parques Nacionales publica $12.500 COP para menores de 25 años (nacional, residente en Colombia, miembro de la CAN o extranjero residente) en Brisas, Cisne-Poleka Kasue y Laguna del Otún, pero en Quindío-Dulima figura en $0. La Resolución 551 de 2025 rige desde el primero de enero de 2026 y no separa sectores. Confirma en parquesnacionales.gov.co antes de pagar.',
    'variants': [
        'Para 2026, la tarifa de $12.500 COP para menores de 25 años aplica según la ficha web en Brisas, Cisne y Otún, mientras Quindío-Dulima figura en $0, en contraste con la Resolución 551 de 2025 que fija una tarifa general sin separar sectores. Confirma en parquesnacionales.gov.co.'
    ],
    'detail': 'La tabla de tarifas 2026 de Parques Nacionales lista $12.500 para menores de 25 años en tres sectores, pero pone $0 en Quindío-Dulima. La Resolución 551 del 19 de diciembre de 2025 no divide sectores. Seguro de accidentes y guianza se pagan aparte.'
}
operations.append({
    'op': 'update',
    'reason': 'Aclarar que la tarifa de $12.500 no aplica a Quindío-Dulima ($0 en web) y reflejar la discrepancia con la Resolución 551 de 2025.',
    'entry': e,
    'evidence': [ev_pnn_admission, ev_pnn_admission_rates, ev_pnn_admission_brisas, ev_res551_header, ev_res551_vigencia, ev_res551_rates]
})

# 3. booking_fees.adult_resident_admission_fee
e = get_entry('booking_fees.adult_resident_admission_fee')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'En 2026, la ficha de Parques Nacionales publica $24.500 COP para mayores de 25 años (nacional, residente en Colombia, miembro de la CAN o extranjero residente) en Brisas, Cisne-Poleka Kasue y Laguna del Otún, pero en Quindío-Dulima figura en $0. La Resolución 551 de 2025 rige desde el primero de enero de 2026 y no separa sectores. Confirma en parquesnacionales.gov.co antes de pagar.',
    'variants': [
        'Para 2026, la tarifa de $24.500 COP para adultos residentes aplica según la ficha web en Brisas, Cisne y Otún, mientras Quindío-Dulima figura en $0, frente a la Resolución 551 de 2025 que fija una tarifa general sin separar sectores. Confirma en parquesnacionales.gov.co.'
    ],
    'detail': 'La tabla de tarifas 2026 de Parques Nacionales lista $24.500 para adultos nacionales o residentes en Brisas, Cisne y Otún, pero pone $0 en Quindío-Dulima. La Resolución 551 del 19 de diciembre de 2025 no divide sectores. Seguro de accidentes y guianza van aparte.'
}
operations.append({
    'op': 'update',
    'reason': 'Aclarar que la tarifa de $24.500 no aplica a Quindío-Dulima ($0 en web) y reflejar la discrepancia con la Resolución 551 de 2025.',
    'entry': e,
    'evidence': [ev_pnn_admission, ev_pnn_admission_rates, ev_pnn_admission_brisas, ev_res551_header, ev_res551_vigencia, ev_res551_rates]
})

# 4. booking_fees.foreign_nonresident_admission_fee
e = get_entry('booking_fees.foreign_nonresident_admission_fee')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'En 2026, la ficha de Parques Nacionales publica $68.000 COP para extranjeros no residentes ni miembros de la CAN en Brisas, Cisne-Poleka Kasue y Laguna del Otún, pero en Quindío-Dulima figura en $0. La Resolución 551 de 2025 rige desde el primero de enero de 2026 y no separa sectores. Confirma en parquesnacionales.gov.co antes de pagar.',
    'variants': [
        'Para 2026, la tarifa de $68.000 COP para extranjeros no residentes aplica según la ficha web en Brisas, Cisne y Otún, mientras Quindío-Dulima figura en $0, a diferencia de la Resolución 551 de 2025 que fija tarifa sin dividir sectores. Confirma en parquesnacionales.gov.co.'
    ],
    'detail': 'La ficha de Parques Nacionales publica $68.000 para extranjeros no residentes en Brisas, Cisne y Otún, pero reporta $0 en Quindío-Dulima. La Resolución 551 del 19 de diciembre de 2025 no separa sectores. El seguro obligatorio y la guianza se pagan aparte.'
}
operations.append({
    'op': 'update',
    'reason': 'Aclarar que la tarifa de $68.000 no aplica a Quindío-Dulima ($0 en web) y reflejar la discrepancia con la Resolución 551 de 2025.',
    'entry': e,
    'evidence': [ev_pnn_admission, ev_pnn_admission_rates, ev_pnn_admission_brisas, ev_res551_header, ev_res551_vigencia, ev_res551_rates]
})

# 5. booking_fees.sector_entry_fee_difference
e = get_entry('booking_fees.sector_entry_fee_difference')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'En 2026, la ficha oficial (parquesnacionales.gov.co) muestra los mismos valores en Brisas, Cisne-Poleka Kasue y Laguna del Otún. Para Quindío-Dulima hay un conflicto sin resolver: esa ficha muestra $0, pero la Resolución 551 del 19 de diciembre de 2025 no separa sectores. Confirma en parquesnacionales.gov.co antes de viajar.',
    'variants': [
        'Los valores de 2026 son iguales en Brisas, Cisne-Poleka Kasue y Laguna del Otún. Para Quindío-Dulima hay un conflicto sin resolver: la página de PNN muestra $0, pero la resolución no separa sectores. Confirma antes de viajar.'
    ],
    'detail': 'El protocolo sur de 2023 recomendó no cobrar en los senderos del sur como medida transitoria, mientras se implementa la infraestructura de cobro. La resolución 551 no separa sectores. Conflicto sin resolver.'
}
ev_proto_sur = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2024/02/Protocolo-de-reservas-nevado-del-Tolima.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/protocolo_reservas_tolima_2024.txt',
    'quote': 'sin realizar el cobro de derecho de ingreso, hasta tanto se cuente con la\n         infraestructura necesaria para el cobro',
    'checked_on': '2026-11-22'
}
operations.append({
    'op': 'update',
    'reason': 'Actualizar la fecha precisa de la Resolución 551 de 2025 y mantener la coherencia en las tarifas por sector y Quindío-Dulima.',
    'entry': e,
    'evidence': [ev_pnn_admission, ev_pnn_admission_rates, ev_pnn_admission_brisas, ev_res551_header, ev_res551_vigencia, ev_proto_sur]
})

# 6. booking_fees.vehicle_entry_fee
e = get_entry('booking_fees.vehicle_entry_fee')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'En 2026, la ficha de Parques Nacionales publica en Brisas-Kumanday automóvil a $10.000 COP, microbús o buseta a $27.500 y bus a $56.000; la moto tiene prohibido el ingreso y en los demás sectores no aplica. La Resolución 551 del 19 de diciembre de 2025 rige desde el primero de enero de 2026. Confirma en parquesnacionales.gov.co antes de viajar.',
    'variants': [
        'Para 2026, las tarifas vehiculares en Brisas según la ficha oficial son $10.000 para automóvil, $27.500 para microbús o buseta y $56.000 para bus, con ingreso prohibido para motos. En Cisne y Otún no aplica cobro vehicular. Confirma en parquesnacionales.gov.co.'
    ],
    'detail': 'La tabla de la ficha de Parques Nacionales clasifica los vehículos en Brisas como automóvil ($10.000), microbús o buseta ($27.500) y bus ($56.000). Aunque otra fila usa el término colectivo para el monto de $27.500, la buseta no corresponde al bus de $56.000. Motos están prohibidas y en Cisne y Otún figura No aplica.'
}
ev_vehicle_pnn1 = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Automóvil:\n10.000\nColectivo:\n27.500\nBuseta:\n56.000\n(máximo 30 pasajeros)\nMoto:\nProhibido el ingreso',
    'checked_on': '2026-11-22'
}
ev_vehicle_pnn2 = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Vehículo tipo automóvil\n$ 10.000\nMicrobús o buseta\n$ 27.500\nBus\n$ 56.000\nMoto\nPROHIBIDO',
    'checked_on': '2026-11-22'
}
ev_vehicle_pnn3 = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': 'Cisne-Poleka Kasue y Laguna del Otún\n*Estos valores no incluyen el seguro obligatorio de accidentes, que debe ser asumido por el visitante y pagado a través de la agencia o guía ecoturístico de su elección.\n12.500\n24.500\n68.000\nNo aplica',
    'checked_on': '2026-11-22'
}
ev_vehicle_res551 = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2026/02/RESOLUCION-551-DE-2025-ACTUALIZA-EL-VALOR-DERECHOS-DE-INGRESO-Y-SERVICIOS-COMPLEMENTARIOS-A-LAS-AREAS-PROTEGIDAS.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/resolucion-551-2025-pnn-2026-02.txt',
    'quote': 'Parque Nacional Natural Los\n$10.000\n$27.500\n$56.000\nNevados',
    'checked_on': '2026-11-22'
}
operations.append({
    'op': 'update',
    'reason': 'Alinear categorías de vehículos con la ficha oficial: automóvil $10.000, microbús o buseta $27.500 y bus $56.000, sin confundir buseta con bus.',
    'entry': e,
    'evidence': [ev_vehicle_pnn1, ev_vehicle_pnn2, ev_vehicle_pnn3, ev_vehicle_res551, ev_res551_header, ev_res551_vigencia]
})

# 7. hours_status.night_entry_prohibition
e = get_entry('hours_status.night_entry_prohibition')
e['last_verified'] = '2026-11-22'
e['sources'] = [
    {
        'label': 'Parques Nacionales Naturales de Colombia · PNN Los Nevados',
        'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
        'retrieved_at': '2026-11-21'
    },
    {
        'label': 'Parques Nacionales Naturales de Colombia · Resolución 207 de 2023 (Reglamentación transitoria PNN Los Nevados)',
        'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf',
        'retrieved_at': '2026-11-21'
    },
    {
        'label': 'PNN Los Nevados · Informe de necesidades de asistencia 2024',
        'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx',
        'retrieved_at': '2026-11-21'
    }
]
e['answer'] = {
    'short': 'La ficha solo publica franjas de ingreso de día y la Resolución 207 de 2023 manda respetar los horarios establecidos; no trae una frase de prohibición de ingreso nocturno. El informe de necesidades de 2024 lista «Actividad nocturna: Sector Brisas y Cisne» entre actividades que requieren permiso especial, y esa lista no está en la Resolución 207. No entres de noche sin ese permiso especial del parque para esa fecha: confirma con Parques Nacionales (@ParquesColombia).',
    'variants': [
        'No hay una frase de prohibición nocturna en la ficha ni en la Resolución 207 de 2023, que solo manda respetar los horarios. El informe de 2024 lista actividad nocturna en Brisas y Cisne como permiso especial, y no está en esa resolución: no entres de noche sin ese permiso para tu fecha y confírmalo con Parques Nacionales (@ParquesColombia).'
    ],
    'detail': 'La Resolución 207 de 2023 establece que los visitantes deben respetar los horarios de las actividades turísticas autorizadas, todos ellos diurnos. El informe de necesidades de asistencia 2024 cataloga la actividad nocturna en Brisas y Cisne como sujeta a permiso especial expedido por la entidad. No está permitido el tránsito nocturno sin dicha autorización.'
}
ev_night_pnn = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/pnn_nevados.txt',
    'quote': 'abierto todos los días del año en horario de 8:00 a. m. a 2:00 p. m., pero ten presente que la última charla de inducción obligatoria se realiza a la 1:30 p. m.',
    'checked_on': '2026-11-22'
}
ev_night_res207 = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/hours_status/evidence/raw/resolucion_207_2023.txt',
    'quote': 'Respetar los horarios establecidos para realizar cada una de las actividades turísticas.',
    'checked_on': '2026-11-22'
}
ev_night_informe = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/activities/evidence/raw/pnn_informe_necesidades_2024.txt',
    'quote': 'Estas actividades requieren un permiso especial para realizarlas en el PNN Los Nevados.\n1.Actividad nocturna: Sector Brisas y Cisne',
    'checked_on': '2026-11-22'
}
operations.append({
    'op': 'update',
    'reason': 'Eliminar prohibición absoluta aislada; articular la exigencia de franjas diurnas con el permiso especial de 2024 para actividades nocturnas en Brisas y Cisne.',
    'entry': e,
    'evidence': [ev_night_pnn, ev_night_res207, ev_night_informe]
})

# 8. services.porter_luggage
e = get_entry('services.porter_luggage')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'El porteo de maletas solo está permitido por El Cedral, Valle de Cocora y Palomar, y está prohibido en los campamentos de Calvito y Arenales (reglamentación de 2023). El informe de 2024 menciona el sendero Chilcos–Arenales cumbre, pero no establece autorización de porteo en Juntas ni en Chilcos: confirma la ruta con el prestador antes de contratar.',
    'variants': [
        'Según la reglamentación de 2023, el porteo de equipaje se permite únicamente ingresando por El Cedral, Cocora y Palomar, y está estrictamente prohibido hacia Calvito y Arenales. El informe de 2024 no autoriza porteo en Juntas ni Chilcos: verifica la ruta con el prestador autorizado.'
    ],
    'detail': 'La reglamentación ecoturística de 2023 (Anexo PNN) limita el servicio de porteo de maletas exclusivamente al sector sur por El Cedral, Cocora y Palomar hasta puntos determinados, y prohíbe el porteo para las zonas de camping temporales de Calvito y Arenales. El informe de 2024 cita el sendero Chilcos-Arenales cumbre pero no autoriza porteo en Juntas o Chilcos. Cualquier ruta debe verificarse con el prestador registrado.'
}
ev_porteo_anexo = {
    'url': 'https://parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/anexo_pnn_nevados_2023.txt',
    'quote': 'Nota: queda prohibido el uso del porteo de maletas para las zonas de camping temporales\n      correspondientes al Calvito y Arenales.',
    'checked_on': '2026-11-22'
}
ev_porteo_informe = {
    'url': 'https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/activities/evidence/raw/pnn_informe_necesidades_2024.txt',
    'quote': 'Sendero los chilcos – arenales cumbre',
    'checked_on': '2026-11-22'
}
ev_porteo_pnn = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/services/evidence/raw/pnn_nevados.txt',
    'quote': 'Guías y operadores turísticos autorizados',
    'checked_on': '2026-11-22'
}
operations.append({
    'op': 'update',
    'reason': 'Alinear porteo de maletas: mantener la prohibición en Calvito y Arenales según norma 2023 y aclarar que el informe 2024 menciona el sendero Chilcos-Arenales sin autorizar porteo en Juntas o Chilcos.',
    'entry': e,
    'evidence': [ev_porteo_anexo, ev_porteo_informe, ev_porteo_pnn]
})

# 9. booking_fees.brisas_guide_price
e = get_entry('booking_fees.brisas_guide_price')
e['last_verified'] = '2026-11-22'
e['answer'] = {
    'short': 'La ficha oficial de Parques Nacionales publica $22.000 para el servicio de guianza e interpretación de UTON en Brisas, pero lo hace sin año y sin aclarar si es por persona o por grupo. No lo tomes como el precio a pagar: consulta directamente con UTON la tarifa vigente antes de contratar.',
    'variants': [
        'El valor de $22.000 que aparece en la ficha de Parques Nacionales para la guianza de UTON en Brisas no indica año de vigencia ni si aplica por persona o por grupo. No lo asumas como el precio a pagar y confirma la tarifa con la concesión UTON antes de viajar.'
    ],
    'detail': 'En la ficha oficial de Los Nevados figura la cifra 22.000 para servicios de interpretación y guianza prestados por la Concesión Unión Temporal Operación Nevados (UTON) en Brisas-Kumanday, pero la página no indica fecha ni unidad de cobro (individual o grupal). Las tarifas de guianza deben confirmarse directamente con el operador.'
}
ev_brisas_guide = {
    'url': 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
    'path': 'research_notes/Conocimiento turístico de Los Nevados/booking_fees/evidence/raw/pnn_nevados.txt',
    'quote': '22.000\n*Este servicio es prestado por la Concesión Unión Temporal Operación Nevados (UTON).',
    'checked_on': '2026-11-22'
}
operations.append({
    'op': 'update',
    'reason': 'No presentar $22.000 como tarifa vigente fija a pagar; señalar que la ficha oficial lo publica sin año y sin unidad (persona o grupo), remitiendo a UTON.',
    'entry': e,
    'evidence': [ev_brisas_guide]
})

proposal = {'operations': operations}
out_path = W / 'proposals/G2.json'
out_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Wrote {len(operations)} operations to {out_path}')
