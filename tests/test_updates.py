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

    def test_secret_markers_have_real_anchors_and_reachable_guides(self):
        articles = {a['id']: a for a in self.base['articulos'] + self.dyn['articulos_nuevos']}
        landmarks = json.loads((ROOT / 'src/tiles/datos/gtadb-6.json').read_text('utf-8'))
        anchors = {r[0]: r for r in landmarks['l']}
        for pin in self.dyn['mapa_lugares']:
            if not pin.get('secreto'):
                continue
            with self.subTest(pin=pin['id']):
                self.assertTrue(150 <= pin['x'] <= 625 and 150 <= pin['y'] <= 800)
                self.assertIn(pin['guia'], articles)
                self.assertTrue(articles[pin['guia']].get('spoiler'))
                self.assertTrue(pin.get('precision'))
                self.assertFalse(pin['exacta'])
                anchor = anchors[int(pin['gtadb'][1:])]
                self.assertAlmostEqual(pin['x'], anchor[3], places=2)
                self.assertAlmostEqual(pin['y'], anchor[4], places=2)

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
