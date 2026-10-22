import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.bloqueos import URLFilter
from core.dataset import normalize_url, quality_score
from core.procesador import WebProcessor


def test_noise_filter_keeps_normal_sentences():
    p = WebProcessor()
    text = p.clean_text_preserving_code(
        "JavaScript es un lenguaje muy usado en la web.\n"
        "GitHub aloja proyectos de código fuente.\n"
        "El index del array empieza en cero.\n"
        "Una frase normal con suficiente contenido."
    )
    assert "JavaScript" in text
    assert "GitHub" in text
    assert "index del array" in text


def test_inline_code_is_preserved():
    p = WebProcessor()
    text = p.clean_text_preserving_code("Usa `print()` para mostrar el resultado.")
    assert "print" in text


def test_wikipedia_parenthesis_is_preserved():
    f = URLFilter()
    assert f.sanitize_url("https://es.wikipedia.org/wiki/Python_(lenguaje)") == "https://es.wikipedia.org/wiki/Python_(lenguaje)"


def test_quality_score_is_useful_for_normal_article():
    # El texto debe contener variedad real; repetir una misma frase cientos de veces
    # se clasifica correctamente como contenido de baja calidad.
    content = "\n".join(
        f"Sección {i}: el procesador {i * 7} ejecuta instrucciones distintas y coordina "
        f"{i + 3} unidades internas mientras la caché conserva datos recientes para acelerar el trabajo."
        for i in range(30)
    )
    assert quality_score(content) >= 65


def test_url_normalization():
    assert normalize_url("HTTPS://EXAMPLE.COM/a/?utm_source=x") == "https://example.com/a"
