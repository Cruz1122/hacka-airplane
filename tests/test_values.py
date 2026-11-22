"""Regression tests for free-text value and citation extraction."""

from nevados_bench.values import extract_citations, extract_numbers


def test_bare_bracketed_passage_id_is_a_citation_not_a_value():
    # Regression: "[EST-C-15]" used to leak "15" into the extracted values, which the
    # grounding scorer then reported as a fabricated quantity.
    text = "Repose 45 minutos antes de continuar [EST-C-15]."
    assert extract_numbers(text) == {"45"}
    assert extract_citations(text) == ["EST-C-15"]
    assert extract_citations("Abre a las 8 [fuente: par-06].") == ["PAR-06"]
    assert extract_numbers("Lleve [2] bastones") == {"2"}
