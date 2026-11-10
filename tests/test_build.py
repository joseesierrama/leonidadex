import json
import pathlib
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build
from site_support import info_pages, load_config, privacy_ready, legal_ready


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("a", "link") and "href" in attrs:
            self.hrefs.append(attrs["href"])


class BuildTests(unittest.TestCase):
    def test_build_and_internal_navigation(self):
        with tempfile.TemporaryDirectory(prefix="test-site-", dir=ROOT) as tmp:
            original = build.OUT
            build.OUT = pathlib.Path(tmp) / "site"
            try:
                build.main()
                output = build.OUT
                pages = list(output.rglob("*.html"))
                base = json.loads((build.SRC / "base.json").read_text("utf-8"))
                dyn = json.loads((build.SRC / "actualizaciones.json").read_text("utf-8"))
                expected = len(base["articulos"]) + len(dyn.get("articulos_nuevos", [])) + 9
                expected += 2 if privacy_ready(build.CONFIG) else 0
                expected += 1 if legal_ready(build.CONFIG) else 0
                self.assertEqual(len(pages), expected)
                self.assertEqual((output / "ads.txt").exists(), bool(build.CONFIG["adsense_publisher_id"]))
                self.assertEqual((output / "privacidad").exists(), privacy_ready(build.CONFIG))
                self.assertEqual((output / "aviso-legal").exists(), legal_ready(build.CONFIG))
                # The standalone FAQ must retain source links, not just the answers.
                faq_page = (output / "preguntas-frecuentes/index.html").read_text("utf-8")
                faq_links = Links()
                faq_links.feed(faq_page)
                for answer in base["faq"]:
                    for source in answer.get("fuentes", []):
                        self.assertIn(source["url"], faq_links.hrefs)
                for page in pages:
                    text = page.read_text("utf-8")
                    self.assertEqual('data-ga4=' in text, bool(build.CONFIG["ga4_id"]))
                    self.assertIn('rel="icon"', text)
                    if page.name == "index.html" and page.parent != output:
                        self.assertIn('<summary>Menú</summary>', text)
                    parser = Links()
                    parser.feed(text)
                    for href in parser.hrefs:
                        path = urlsplit(href)
                        if path.scheme or path.netloc or not path.path:
                            continue
                        target = (page.parent / unquote(path.path)).resolve()
                        self.assertTrue(target.is_relative_to(output.resolve()), (page, href))
                        self.assertTrue(target.exists(), (page, href))
            finally:
                build.OUT = original

    def config(self, **updates):
        config = dict(responsable="", correo_contacto="", ga4_id="", adsense_publisher_id="", fecha_privacidad="2026-11-10")
        config.update(updates)
        with tempfile.TemporaryDirectory(prefix="test-config-", dir=ROOT) as tmp:
            src = pathlib.Path(tmp)
            (src / "sitio.json").write_text(json.dumps(config), "utf-8")
            return load_config(src)

    def test_measurement_requires_real_owner_fields(self):
        with self.assertRaisesRegex(ValueError, "responsable"):
            self.config(ga4_id="G-TEST123456")
        with self.assertRaisesRegex(ValueError, "ga4_id"):
            self.config(ga4_id="not-a-property")
        with self.assertRaisesRegex(ValueError, "adsense_publisher_id"):
            self.config(adsense_publisher_id="pub-placeholder")

    def test_policy_matches_enabled_services_and_escapes_owner(self):
        config = self.config(responsable="Titular <ejemplo>", correo_contacto="prueba@example.org")
        pages = info_pages(config)
        self.assertIn("privacidad", pages)
        self.assertIn("Titular &lt;ejemplo&gt;", pages["privacidad"][2])
        self.assertIn("no carga Google Analytics", pages["privacidad"][2])
        config["ga4_id"] = "G-TEST123456"
        self.assertIn("Si aceptas la medición", info_pages(config)["privacidad"][2])
        self.assertIn("_ga", info_pages(config)["cookies"][2])

    def test_legal_notice_requires_complete_data_and_escapes_it(self):
        config = self.config(responsable="Titular", correo_contacto="prueba@example.org")
        self.assertNotIn("aviso-legal", info_pages(config))
        with self.assertRaisesRegex(ValueError, "NIF y domicilio"):
            self.config(responsable="Titular", correo_contacto="prueba@example.org", nif="ID-PRUEBA")
        config = self.config(responsable="Titular", correo_contacto="prueba@example.org",
                             nif="ID <prueba>", domicilio="Dirección <prueba>")
        legal = info_pages(config)["aviso-legal"][2]
        self.assertIn("ID &lt;prueba&gt;", legal)
        self.assertIn("Dirección &lt;prueba&gt;", legal)


if __name__ == "__main__":
    unittest.main()
