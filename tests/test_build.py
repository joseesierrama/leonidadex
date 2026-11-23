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
from guide_pages import load_guides
from site_support import info_pages, load_config, privacy_ready, legal_ready, head


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.references = []
        self.ids = set()
        self.metas = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("a", "link") and "href" in attrs:
            self.hrefs.append(attrs["href"])
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "meta":
            self.metas.append(attrs)
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.references.append((key, attrs[key]))


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
                expected = len(base["articulos"]) + len(dyn.get("articulos_nuevos", [])) + 10
                expected += len(info_pages(build.CONFIG))
                expected += 2 + len(load_guides(build.SRC)['guias'])
                self.assertEqual(len(pages), expected)
                map_page = (output / 'mapa/index.html').read_text('utf-8')
                self.assertIn('class="static map-page"', map_page)
                self.assertIn('data-map-status="done"', map_page)
                self.assertIn('SOLO GTA VI', map_page)
                self.assertIn('mapa-progreso.js', map_page)
                self.assertNotIn('__MANI__', map_page)
                self.assertNotIn('GTA V = 1', map_page)
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
                # Story solutions must remain in a closed, native disclosure.
                for article in base["articulos"] + dyn.get("articulos_nuevos", []):
                    if article.get("spoiler"):
                        text = (output / "reportajes" / article["id"] / "index.html").read_text("utf-8")
                        self.assertIn('<details class="spoiler-gate"><summary>', text)
                        self.assertNotIn('<details class="spoiler-gate" open', text)
                        self.assertIn(build.E(article["spoiler"]), text)
                parsed_pages = {}
                for page in pages:
                    parser = Links()
                    parser.feed(page.read_text("utf-8"))
                    parsed_pages[page.resolve()] = parser
                for page in pages:
                    text = page.read_text("utf-8")
                    self.assertEqual('data-ga4=' in text, bool(build.CONFIG["ga4_id"]))
                    self.assertIn('rel="icon"', text)
                    if page.name == "index.html" and page.parent != output:
                        self.assertIn('<summary>Menú</summary>', text)
                    parser = parsed_pages[page.resolve()]
                    verification = [m.get("content") for m in parser.metas if m.get("name") == "google-adsense-account"]
                    self.assertEqual(verification, ["ca-" + build.CONFIG["adsense_publisher_id"]] if build.CONFIG["adsense_publisher_id"] else [])
                    self.assertNotIn("pagead2.googlesyndication.com", text)
                    for key, href in parser.references:
                        path = urlsplit(href)
                        if path.scheme not in ("", "http", "https") or (path.netloc and path.netloc != urlsplit(build.base_url()[0]).netloc):
                            continue
                        target = (output / unquote(path.path).lstrip("/") if path.path.startswith("/") else page.parent / unquote(path.path) if path.path else page).resolve()
                        self.assertTrue(target.is_relative_to(output.resolve()), (page, href))
                        if target.is_dir():
                            target = target / "index.html"
                        self.assertTrue(target.exists(), (page, href))
                        if key == "href" and path.fragment and target in parsed_pages:
                            # These hashes select a point through the map's JS router.
                            if target in (output.resolve() / "index.html", output.resolve() / "mapa/index.html") and path.fragment.startswith(("l=", "g=")):
                                continue
                            self.assertIn(unquote(path.fragment), parsed_pages[target].ids, (page, href))
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

    def test_verification_does_not_activate_advertising(self):
        for config in ({}, {"adsense_publisher_id": "pub-placeholder"}):
            self.assertNotIn("google-adsense-account", head("", "https://example.org/", config))
        verified = head("", "https://example.org/", {"adsense_publisher_id": "pub-1234567890123456"})
        self.assertIn('name="google-adsense-account" content="ca-pub-1234567890123456"', verified)
        self.assertNotIn("<script", verified)

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
        with self.assertRaisesRegex(ValueError, "ocultación"):
            self.config(responsable="Titular", correo_contacto="prueba@example.org",
                        nif="ID-PRUEBA", domicilio="Dirección, <redacted>")
        config = self.config(responsable="Titular", correo_contacto="prueba@example.org",
                             nif="ID <prueba>", domicilio="Dirección <prueba>")
        legal = info_pages(config)["aviso-legal"][2]
        self.assertIn("ID &lt;prueba&gt;", legal)
        self.assertIn("Dirección &lt;prueba&gt;", legal)


if __name__ == "__main__":
    unittest.main()
