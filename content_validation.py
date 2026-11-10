"""Comprobaciones estructurales antes de publicar novedades; no verifican los hechos."""
from datetime import datetime
import re
from urllib.parse import urlsplit


def validate_content(base, dyn):
    if not isinstance(dyn.get("meta"), dict) or not isinstance(dyn.get("noticias"), list):
        raise ValueError("Las novedades deben incluir meta y la lista noticias")
    updated = datetime.fromisoformat(dyn["meta"]["actualizado"])
    if updated.tzinfo is None:
        raise ValueError("meta.actualizado debe incluir la zona horaria")
    groups = [dyn["noticias"], base.get("articulos", []) + dyn.get("articulos_nuevos", [])]
    for group in groups:
        ids = set()
        for item in group:
            identifier = item.get("id", "")
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", identifier) or identifier in ids:
                raise ValueError("ID de noticia o reportaje inválido o duplicado: " + identifier)
            ids.add(identifier)
            if not item.get("titulo") or not item.get("fuentes"):
                raise ValueError("Cada noticia o reportaje necesita título y fuentes: " + identifier)
            if item.get("fecha"):
                datetime.fromisoformat(item["fecha"])
    # Los datos se insertan en enlaces del navegador: no aceptar URLs ejecutables.
    def check_links(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                if key == "url" and isinstance(nested, str):
                    parsed = urlsplit(nested)
                    if parsed.scheme not in ("https", "http") or not parsed.netloc:
                        raise ValueError("Enlace externo inválido: " + nested)
                else:
                    check_links(nested)
        elif isinstance(value, list):
            for nested in value:
                check_links(nested)
    check_links(base)
    check_links(dyn)
