"""Round 2 overlay for the actions section (audit against N/actions/evidence/quotes.md).

Applied by coordination/build_from_snapshot.py on a fresh copy of actions.v1.json. Every edit
asserts its old text, so a snapshot change fails loudly instead of being skipped silently.
Sources: Policía Nacional (123) and Parques Nacionales ficha Los Nevados, both read 2026-11-21.
"""


def _entry(section, entry_id):
    matches = [e for e in section["entries"] if e["id"] == entry_id]
    assert len(matches) == 1, f"expected one entry {entry_id!r}, found {len(matches)}"
    return matches[0]


def apply(section: dict) -> dict:
    # Brisas reservation: the snapshot attributed the weekend rule to Brisas-Kumanday. Sources conflict:
    # the ficha says the weekend/puente reservation is indispensable for "Brisas–Valle de las Tumbas", and
    # says that for "Brisas-Kumanday" the reservation is not mandatory but recommended one day ahead.
    # Both are stated, each with its scope.
    planned = _entry(section, "actions.register_planned_visit")
    old_step = (
        "Para Brisas-Kumanday en fines de semana y festivos, la ficha oficial pide reservar con al menos "
        "un día de anticipación en reservasnevados.com. En los demás sectores la reserva es obligatoria "
        "y la gestiona la agencia registrada."
    )
    new_step = (
        "En Brisas, en fines de semana y puentes festivos, la reserva es indispensable con al menos un día "
        "de anticipación en reservasnevados.com. En otros días no es obligatoria, pero la ficha recomienda "
        "reservar con un día de anticipación. En los demás sectores la reserva es obligatoria y la gestiona "
        "la agencia registrada."
    )
    assert planned["answer"]["steps"][1][1] == old_step, "register_planned_visit step text changed"
    planned["answer"]["steps"][1][1] = new_step

    # The 123 detail said the misuse "puede impedir" a real emergency response. The Policía text says
    # "puede evitar la atención de una emergencia real"; the wording now matches the source.
    emergency = _entry(section, "actions.report_emergency_general")
    old_detail = "puede impedir la atención de una emergencia real"
    assert old_detail in emergency["answer"]["detail"], "report_emergency_general detail changed"
    emergency["answer"]["detail"] = emergency["answer"]["detail"].replace(
        old_detail, "puede evitar la atención de una emergencia real"
    )
    return section
