from __future__ import annotations

from ainft.utils import truncate_text


class TestUtils:
    def test_truncate_simple_text(self):
        assert truncate_text("a" * 11, 10) == "a" * 7 + "..."

    def test_truncate_korean_text(self):
        assert truncate_text("한" * 11, 10) == "한" * 7 + "..."

    def test_truncate_emoji_text(self):
        assert truncate_text("😊" * 11, 10) == "😊" * 7 + "..."

    def test_truncate_special_character_text(self):
        assert truncate_text("€" * 11, 10) == "€" * 7 + "..."

    def test_truncate_combining_character_text(self):
        assert truncate_text("é" * 11, 10) == "ééééééé..."
