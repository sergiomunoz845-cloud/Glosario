#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glosario de Inteligencia Artificial — versión web (Flask)
=========================================================

Reutiliza los datos y las utilidades de `glosario_ia.py` (la versión de
consola) y los publica como sitio web.

Rutas disponibles:
    GET  /                      página principal con buscador y filtros
    GET  /?q=red                búsqueda por palabra clave
    GET  /?categoria=Fundamentos  filtro por categoría
    GET  /termino/<numero>      ficha individual de un término (1 a 20)
    GET  /api/glosario          el glosario completo en formato JSON

Cómo ejecutarlo:
    pip install -r requirements.txt
    python app.py
    Abrir http://127.0.0.1:5000 en el navegador
"""

try:
    from flask import Flask, abort, jsonify, render_template, request
except ModuleNotFoundError as error:
    if error.name == "flask":
        raise ModuleNotFoundError(
            "No se encontró Flask. Instálalo con: python -m pip install Flask"
        ) from error
    raise

# Se importan los datos de la versión de consola: una sola fuente de verdad.
from glosario_ia import GLOSARIO, categorias, normalizar

app = Flask(__name__)


def filtrar(consulta="", categoria=""):
    """Aplica el filtro por categoría y la búsqueda por palabra clave."""
    entradas = GLOSARIO

    if categoria:
        entradas = [e for e in entradas if e["categoria"] == categoria]

    if consulta:
        clave = normalizar(consulta)
        entradas = [
            e for e in entradas
            if clave in normalizar(e["termino"])
            or clave in normalizar(e["ingles"])
            or clave in normalizar(e["definicion"])
        ]

    return entradas


@app.route("/")
def inicio():
    """Página principal: lista completa o resultados filtrados."""
    consulta = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()

    return render_template(
        "index.html",
        entradas=filtrar(consulta, categoria),
        glosario=GLOSARIO,
        total=len(GLOSARIO),
        categorias=categorias(),
        consulta=consulta,
        categoria_activa=categoria,
    )


@app.route("/termino/<int:numero>")
def termino(numero):
    """Ficha individual de un término."""
    for entrada in GLOSARIO:
        if entrada["id"] == numero:
            anterior = numero - 1 if numero > 1 else None
            siguiente = numero + 1 if numero < len(GLOSARIO) else None
            return render_template(
                "termino.html",
                entrada=entrada,
                anterior=anterior,
                siguiente=siguiente,
            )
    abort(404)


@app.route("/api/glosario")
def api_glosario():
    """Devuelve el glosario completo en JSON (útil para otras aplicaciones)."""
    return jsonify(GLOSARIO)


@app.errorhandler(404)
def no_encontrado(error):
    """Página de error para direcciones que no existen."""
    return render_template("404.html"), 404


@app.route('/etica-ia')
def etica_ia():
    ensayo = {
        "titulo": "Ética y Aspectos Sociales de la Inteligencia Artificial",
        "contenido": [
            "La Inteligencia Artificial (IA) ha dejado de ser una promesa de la ciencia ficción para convertirse en el motor de la Cuarta Revolución Industrial. Su capacidad para procesar datos a escala masiva, automatizar decisiones y predecir comportamientos plantea dilemas éticos y sociales que requieren atención inmediata. La tecnología no es neutral; hereda, procesa y amplifica los valores de quienes la diseñan y de los datos con los que es alimentada.",
            "Uno de los desafíos más urgentes es el sesgo algorítmico. Los modelos de IA aprenden de bases de datos históricas generadas por humanos, las cuales contienen prejuicios sistémicos y culturales. Si estos modelos no se auditan rigurosamente, corren el riesgo de perpetuar o amplificar la discriminación en áreas críticas como la selección de personal, la evaluación crediticia, el diagnóstico médico o los sistemas de justicia penal.",
            "Otro pilar fundamental es la transparencia y la explicabilidad. Muchos de los modelos más avanzados, como las redes neuronales profundas, operan como 'cajas negras'. Resulta extremadamente difícil rastrear el razonamiento exacto que llevó a una IA a una conclusión específica. Cuando la tecnología toma decisiones que afectan derechos fundamentales, el derecho a una explicación comprensible se vuelve una exigencia.",
            "En el ámbito socioeconómico, la automatización impulsada por la IA está reconfigurando el mercado laboral. Mientras que promete aumentar la productividad y crear nuevas categorías de empleo, también amenaza con el desplazamiento de trabajadores. Esta transición exige políticas públicas enfocadas en la reconversión laboral, garantizando que los beneficios no ensanchen la brecha de desigualdad económica.",
            "La privacidad y la gobernanza de datos representan otra tensión ética crítica. La recolección masiva de datos para entrenar estos sistemas genera preocupaciones sobre el consentimiento informado, la vigilancia y la propiedad de la información. Proteger la autonomía individual frente al perfilado predictivo requiere normativas estrictas desde el diseño.",
            "El verdadero desafío de la Inteligencia Artificial no es técnico, sino moral. Su desarrollo y despliegue deben estar acompañados de marcos regulatorios robustos y una ética centrada en el ser humano, asegurando que la IA actúe como una herramienta para el bienestar colectivo."
        ]
    }
    return render_template('ensayo.html', ensayo=ensayo)


if __name__ == "__main__":
    # debug=True recarga el servidor al guardar cambios; quítalo al entregar.
    app.run(host="127.0.0.1", port=5000, debug=True)