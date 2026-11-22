"""Round 2 overlay for the conversation section (audit against N/conversation/evidence/quotes.md).

Applied by coordination/build_from_snapshot.py on a fresh copy of conversation.v1.json. Edits assert
their old text so a snapshot change fails loudly. No answer states a park number, rule or place:
the only park-related strings are the park's name and official channel pointers, all quoted.
"""

import copy


def _entry(section, entry_id):
    matches = [e for e in section["entries"] if e["id"] == entry_id]
    assert len(matches) == 1, f"expected one entry {entry_id!r}, found {len(matches)}"
    return matches[0]


def apply(section: dict) -> dict:
    # The snapshot answer told the user to rephrase their own question. The examples (repite por favor,
    # explícamelo de nuevo, otra vez) ask the assistant to repeat or simplify. The app has no free
    # generation, so the honest answer is to repeat the prepared text, not to promise a simpler rewrite.
    repeat = _entry(section, "conversation.repeat_or_unclear")
    assert repeat["answer"]["short"].startswith("Perdón, no te entendí bien."), "repeat answer changed"
    repeat["answer"]["short"] = (
        "Claro. Dime el tema, como acceso, horarios o clima, y te repito el texto preparado; "
        "no tengo otra versión más sencilla."
    )
    repeat["answer"]["variants"] = [
        "Con gusto. Escribe otra vez la pregunta o el tema del parque y te respondo con el mismo texto preparado."
    ]

    # Missing intent: asking for a shorter answer ("resúmelo"). Checked: no example in any section
    # contains resum, corto, breve, al grano or summary wording.
    summary = {
        "id": "conversation.summary_request",
        "label": "pedir una respuesta más corta",
        "kind": "chat",
        "audience": "visitor",
        "examples": [
            "resúmelo",
            "dime en corto",
            "muy largo, resúmelo",
            "sin tanto rollo, al grano",
            "solo lo importante porfa",
            "resumen rápido?",
            "dime lo básico nomás",
            "puedes ser más breve?",
            "y en dos líneas?",
            "no me cuentes todo, solo lo clave",
            "can you summarize that?",
            "make it short please",
            "ya dime rápido lo principal",
            "resume eso pues",
        ],
        "hard_negatives": [
            "cuéntame más",
            "explícamelo de nuevo",
            "háblame en voz alta",
        ],
        "answer": {
            "short": (
                "Claro. Dime el tema en una palabra (acceso, horarios, clima o qué llevar) "
                "y te respondo en pocas palabras."
            ),
            "variants": [
                "Con gusto. Dime sobre qué tema quieres la versión corta: acceso, horarios, clima o qué llevar."
            ],
        },
        "sources": copy.deepcopy(_entry(section, "conversation.more_detail_followup")["sources"]),
        "related": ["conversation.more_detail_followup", "conversation.repeat_or_unclear"],
        "tags": ["resumen", "respuesta corta"],
    }
    assert not any(e["id"] == summary["id"] for e in section["entries"]), "summary entry already exists"
    section["entries"].append(summary)
    return section
