from __future__ import annotations

from ainft.utils import normalize_text, truncate_text


class TestUtils:
    def test_normalize_text(self):
        assert normalize_text("é" * 10) == "e" * 10
        assert normalize_text("ñ" * 10) == "n" * 10

    def test_truncate_simple_text(self):
        assert truncate_text("a" * 11, 10) == "a" * 7 + "..."

    def test_truncate_korean_text(self):
        assert truncate_text("한" * 11, 10) == "한" * 7 + "..."

    def test_truncate_emoji_text(self):
        assert truncate_text("😊" * 11, 10) == "😊" * 7 + "..."

    def test_truncate_special_character_text(self):
        assert truncate_text("€" * 11, 10) == "€" * 7 + "..."

    def test_truncate_combined_character_text(self):
        assert truncate_text("é" * 11, 10) == "ééée..."

    def test_truncate_normalized_text(self):
        assert truncate_text(normalize_text("é" * 11), 10) == "e" * 7 + "..."
