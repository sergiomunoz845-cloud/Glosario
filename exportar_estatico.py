#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta el glosario a un único archivo HTML que funciona sin servidor.

Sirve para entregar el trabajo como página suelta (abrirla con doble clic) o
para subirla a GitHub Pages, Netlify u otro alojamiento estático.

Uso:
    python exportar_estatico.py [archivo_de_salida.html]
"""

import re
import sys
from pathlib import Path

from app import app

BASE = Path(__file__).parent


def exportar(salida="glosario_ia_web.html"):
    """Genera el HTML de la portada con el CSS y el JS incrustados."""
    with app.test_client() as cliente:
        html = cliente.get("/").get_data(as_text=True)

    css = (BASE / "static" / "estilos.css").read_text(encoding="utf-8")
    js = (BASE / "static" / "glosario.js").read_text(encoding="utf-8")

    # 1. Incrustar la hoja de estilos y el script.
    # (se usa una función como reemplazo para que \u, \n, etc. del código no
    # se interpreten como secuencias de escape de las expresiones regulares)
    html = re.sub(
        r'<link rel="stylesheet" href="[^"]*estilos\.css">',
        lambda _: "<style>\n" + css + "\n</style>",
        html,
    )
    html = re.sub(
        r'<script src="[^"]*glosario\.js"></script>',
        lambda _: "<script>\n" + js + "\n</script>",
        html,
    )

    # 2. Sin servidor no hay rutas /termino/<id>: se enlaza dentro de la página.
    html = re.sub(r'href="/termino/(\d+)"', r'href="#t-\1"', html)

    # 3. La API JSON solo existe en la versión con Flask.
    html = re.sub(
        r'<a href="/api/glosario">formato JSON</a>',
        "formato JSON (en la versión con Flask)",
        html,
    )

    destino = Path(salida)
    destino.write_text(html, encoding="utf-8")
    print(f"Página exportada: {destino.resolve()}  ({destino.stat().st_size // 1024} KB)")
    return destino


if __name__ == "__main__":
    exportar(sys.argv[1] if len(sys.argv) > 1 else "glosario_ia_web.html")
