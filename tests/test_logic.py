import pytest
from app_final import to_slug, convert_case

import pytest
from app_final import analyze_text, convert_case, to_slug

@pytest.mark.parametrize(
    "text, slug",
    [
        ("Hello World", "hello-world"),
        ("Привет Мир", "privet-mir"),
        ("FastAPI & Python", "fastapi-python"),
        ("Multiple   spaces   between", "multiple-spaces-between"),
        ("---dashes-------------", "dashes"),
        ("Mixed CASE text", "mixed-case-text"),
        ("Numbers 123 and 456", "numbers-123-and-456"),
    ],
)
def test_to_slug(text, slug):
    assert to_slug(text) == slug

@pytest.mark.parametrize("text", ["", "   ", "---", "!@#$%^&*()_+"])
def test_to_slug_special(text):
    assert to_slug(text) == ""

@pytest.mark.parametrize(
    "text, mode, expected",
    [
        ("hello world", "upper", "HELLO WORLD"),
        ("HELLO WORLD", "lower", "hello world"),
        ("hello world from fastapi", "snake", "hello_world_from_fastapi"),
        ("hello world from fastapi", "pascal", "HelloWorldFromFastapi"),
        ("hello world from fastapi", "camel", "helloWorldFromFastapi"),
        ("hello", "camel", "hello"),
        ("hello world", "alternating", "hElLo WoRlD"),
        ("a, b! c?", "alternating", "a, B! c?"),
    ],
)
def test_convert_case_normal(text, mode, expected):
    assert convert_case(text, mode) == expected

def test_convert_case_unknown():
    original = "stay like this"
    assert convert_case(original, mode="unknown") == original


def test_convert_case_empty():
    assert convert_case("", mode="camel") == ""
    assert convert_case("", mode="snake") == ""

def test_analyze_text_basic():
    text = "Hello world! Hello Python."
    stats = analyze_text(text)
    assert stats["chars_total"] == len(text)
    assert stats["chars_no_spaces"] == len(text.replace(" ", ""))
    assert stats["word_count"] == 4
    assert stats["most_frequent_word"] == "hello"
    assert stats["most_frequent_count"] == 2
