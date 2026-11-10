import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content_validation import validate_content


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((ROOT / "src/base.json").read_text("utf-8"))
        self.dyn = json.loads((ROOT / "src/actualizaciones.json").read_text("utf-8"))

    def test_current_content_passes(self):
        validate_content(self.base, self.dyn)

    def test_duplicate_news_and_unsafe_links_block_publication(self):
        duplicate = copy.deepcopy(self.dyn)
        duplicate["noticias"].append(duplicate["noticias"][0])
        with self.assertRaisesRegex(ValueError, "duplicado"):
            validate_content(self.base, duplicate)
        unsafe = copy.deepcopy(self.dyn)
        unsafe["noticias"][0]["fuentes"][0]["url"] = "javascript:alert(1)"
        with self.assertRaisesRegex(ValueError, "Enlace externo"):
            validate_content(self.base, unsafe)

    def test_missing_sources_and_ambiguous_timestamps_block_publication(self):
        self.dyn["noticias"][0]["fuentes"] = []
        with self.assertRaisesRegex(ValueError, "fuentes"):
            validate_content(self.base, self.dyn)
        self.dyn["meta"]["actualizado"] = "2026-11-10T12:00:00"
        with self.assertRaisesRegex(ValueError, "zona horaria"):
            validate_content(self.base, self.dyn)
