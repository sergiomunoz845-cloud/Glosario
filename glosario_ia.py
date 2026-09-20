#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glosario de Inteligencia Artificial
===================================

Aplicación de consola que muestra, busca y permite estudiar 20 términos
fundamentales de Inteligencia Artificial.

Las definiciones fueron redactadas a partir de la documentación pública de
IBM Think (secciones "Inteligencia artificial" y "Modelos de lenguaje grandes"),
citando en cada término la página de referencia.

Uso:
    python3 glosario_ia.py                  -> menú interactivo
    python3 glosario_ia.py --listar         -> imprime el glosario completo
    python3 glosario_ia.py --buscar red     -> busca un término o palabra clave
    python3 glosario_ia.py --exportar g.csv -> exporta el glosario a CSV

Requisitos: Python 3.8+ (solo biblioteca estándar).
"""

import argparse
import csv
import random
import sys
import textwrap
import unicodedata

# --------------------------------------------------------------------------- #
# Datos del glosario: 20 términos organizados por categoría
# --------------------------------------------------------------------------- #

FUENTE_IA = "https://www.ibm.com/mx-es/think/topics/artificial-intelligence"
FUENTE_LLM = "https://www.ibm.com/mx-es/think/topics/large-language-models"

GLOSARIO = [
    {
        "id": 1,
        "termino": "Inteligencia artificial (IA)",
        "ingles": "Artificial Intelligence",
        "categoria": "Fundamentos",
        "definicion": (
            "Tecnología que permite a computadoras y máquinas imitar capacidades "
            "humanas como aprender, comprender, resolver problemas, tomar decisiones, "
            "crear contenido y actuar con cierta autonomía. Agrupa a todas las demás "
            "ramas de este glosario."
        ),
        "ejemplo": "Un vehículo autónomo que interpreta su entorno y conduce sin chofer.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 2,
        "termino": "Machine learning (aprendizaje automático)",
        "ingles": "Machine Learning (ML)",
        "categoria": "Fundamentos",
        "definicion": (
            "Rama de la IA que construye modelos entrenando algoritmos con datos para "
            "predecir resultados o tomar decisiones, sin que se programe explícitamente "
            "cada regla. Incluye técnicas como regresión lineal y logística, árboles de "
            "decisión, bosques aleatorios, SVM, KNN y agrupamiento."
        ),
        "ejemplo": "Un modelo que estima el precio de una casa a partir de datos históricos.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 3,
        "termino": "Aprendizaje profundo",
        "ingles": "Deep Learning",
        "categoria": "Fundamentos",
        "definicion": (
            "Subconjunto del machine learning que usa redes neuronales de muchas capas "
            "(redes neuronales profundas). Frente a los modelos clásicos, que suelen tener "
            "una o dos capas ocultas, estas redes acumulan cientos, lo que les permite "
            "extraer características por sí mismas de grandes volúmenes de datos sin "
            "etiquetar."
        ),
        "ejemplo": "El reconocimiento de voz de un asistente virtual.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 4,
        "termino": "Red neuronal artificial",
        "ingles": "Artificial Neural Network",
        "categoria": "Fundamentos",
        "definicion": (
            "Algoritmo inspirado en la estructura del cerebro humano: capas interconectadas "
            "de nodos, análogos a las neuronas, que procesan datos en conjunto. Es "
            "especialmente útil para detectar patrones y relaciones complejas en "
            "cantidades grandes de información."
        ),
        "ejemplo": "Una red convolucional que clasifica imágenes médicas.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 5,
        "termino": "IA débil frente a IA fuerte (AGI)",
        "ingles": "Narrow AI vs. Strong AI / AGI",
        "categoria": "Fundamentos",
        "definicion": (
            "La IA débil o estrecha está diseñada para una tarea concreta o un conjunto "
            "limitado de tareas, y es la que existe hoy. La IA fuerte o general (AGI) sería "
            "capaz de comprender y aplicar conocimiento en cualquier ámbito a un nivel igual "
            "o superior al humano; por ahora es un concepto teórico."
        ),
        "ejemplo": "IA débil: un asistente de voz. IA fuerte: aún no existe ningún sistema así.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 6,
        "termino": "Aprendizaje supervisado",
        "ingles": "Supervised Learning",
        "categoria": "Tipos de aprendizaje",
        "definicion": (
            "Forma más sencilla de machine learning: se entrena el algoritmo con conjuntos "
            "de datos etiquetados, donde cada ejemplo viene acompañado de su respuesta "
            "correcta. El modelo aprende la relación entre entradas y salidas para poder "
            "etiquetar datos nuevos."
        ),
        "ejemplo": "Clasificar correos como spam usando miles de correos ya etiquetados.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 7,
        "termino": "Aprendizaje no supervisado",
        "ingles": "Unsupervised Learning",
        "categoria": "Tipos de aprendizaje",
        "definicion": (
            "Entrenamiento con datos sin etiquetar ni estructurar: el modelo automatiza la "
            "extracción de características y propone por su cuenta qué representan los "
            "datos. Es lo que permite escalar el aprendizaje profundo sin intervención "
            "humana constante."
        ),
        "ejemplo": "Segmentar clientes en grupos de comportamiento sin definirlos de antemano.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 8,
        "termino": "Aprendizaje por refuerzo",
        "ingles": "Reinforcement Learning",
        "categoria": "Tipos de aprendizaje",
        "definicion": (
            "El modelo aprende por ensayo y error mediante funciones de recompensa, en vez "
            "de extraer información de patrones ocultos en un conjunto de datos. Cada acción "
            "recibe una señal positiva o negativa que orienta el comportamiento futuro."
        ),
        "ejemplo": "Un programa que aprende a jugar Go compitiendo millones de partidas.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 9,
        "termino": "Aprendizaje por transferencia",
        "ingles": "Transfer Learning",
        "categoria": "Tipos de aprendizaje",
        "definicion": (
            "Técnica en la que el conocimiento obtenido al resolver una tarea o al procesar "
            "un conjunto de datos se reutiliza para mejorar el desempeño en otra tarea "
            "relacionada. Ahorra datos y tiempo de cómputo frente a entrenar desde cero."
        ),
        "ejemplo": "Reutilizar una red entrenada con fotos generales para detectar fallas industriales.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 10,
        "termino": "IA generativa",
        "ingles": "Generative AI",
        "categoria": "IA generativa",
        "definicion": (
            "Modelos de aprendizaje profundo capaces de crear contenido original complejo "
            "—texto, imágenes, video, audio o código— en respuesta a una instrucción del "
            "usuario. Codifican una representación simplificada de sus datos de "
            "entrenamiento y generan obras similares, pero no idénticas, a ellos."
        ),
        "ejemplo": "Generar el borrador de un cartel publicitario a partir de una descripción.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 11,
        "termino": "Modelo fundacional",
        "ingles": "Foundation Model",
        "categoria": "IA generativa",
        "definicion": (
            "Modelo de aprendizaje profundo entrenado con volúmenes enormes de datos sin "
            "etiquetar que sirve de base para muchas aplicaciones distintas. Su "
            "entrenamiento exige miles de GPU, semanas de procesamiento y costos muy altos, "
            "por lo que suele reutilizarse en lugar de crearse desde cero."
        ),
        "ejemplo": "Un modelo base al que después se le ajusta para atención al cliente.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 12,
        "termino": "Modelo de lenguaje grande (LLM)",
        "ingles": "Large Language Model",
        "categoria": "IA generativa",
        "definicion": (
            "Categoría de modelos fundacionales entrenados con cantidades inmensas de texto "
            "para comprender y generar lenguaje natural. Funcionan prediciendo "
            "estadísticamente el siguiente fragmento de texto (token) una y otra vez, "
            "apoyados en la arquitectura transformador."
        ),
        "ejemplo": "Resumir un artículo largo o redactar un correo a partir de una instrucción.",
        "fuente": FUENTE_LLM,
    },
    {
        "id": 13,
        "termino": "Transformador",
        "ingles": "Transformer",
        "categoria": "IA generativa",
        "definicion": (
            "Arquitectura de red neuronal, presentada en 2017, entrenada con datos "
            "secuenciales para generar secuencias largas de contenido. Su pieza central es "
            "el mecanismo de autoatención, que calcula qué tan relacionado está cada token "
            "con los demás, incluso si están lejos en el texto, y permite paralelizar el "
            "entrenamiento."
        ),
        "ejemplo": "Es la base de la mayoría de los modelos de IA generativa actuales.",
        "fuente": FUENTE_LLM,
    },
    {
        "id": 14,
        "termino": "Ajuste fino",
        "ingles": "Fine-tuning",
        "categoria": "IA generativa",
        "definicion": (
            "Proceso de adaptar un modelo ya entrenado a una tarea o dominio específico "
            "usando un conjunto de datos etiquetados mucho más pequeño. Una variante muy "
            "usada es el RLHF (aprendizaje por refuerzo con retroalimentación humana), donde "
            "personas califican las respuestas y el modelo aprende a preferir las mejor "
            "evaluadas."
        ),
        "ejemplo": "Especializar un modelo general con documentos médicos de un hospital.",
        "fuente": FUENTE_LLM,
    },
    {
        "id": 15,
        "termino": "Generación aumentada por recuperación (RAG)",
        "ingles": "Retrieval-Augmented Generation",
        "categoria": "IA generativa",
        "definicion": (
            "Técnica que conecta un modelo ya entrenado con fuentes de conocimiento externas. "
            "La información recuperada se entrega al modelo junto con la pregunta, de modo "
            "que responde con datos actualizados y más precisos sin necesidad de volver a "
            "entrenarlo."
        ),
        "ejemplo": "Un asistente que consulta el manual interno de la empresa antes de responder.",
        "fuente": FUENTE_LLM,
    },
    {
        "id": 16,
        "termino": "Procesamiento de lenguaje natural (PLN)",
        "ingles": "Natural Language Processing (NLP)",
        "categoria": "Aplicaciones",
        "definicion": (
            "Campo de la IA que permite a las máquinas interpretar, analizar y producir "
            "lenguaje humano. Es una de las áreas donde el aprendizaje profundo resulta más "
            "adecuado y sostiene a chatbots, traductores y buscadores."
        ),
        "ejemplo": "Un chatbot que entiende la pregunta de un cliente sobre su pedido.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 17,
        "termino": "Visión artificial",
        "ingles": "Computer Vision",
        "categoria": "Aplicaciones",
        "definicion": (
            "Área de la IA dedicada a que los sistemas vean e identifiquen objetos en "
            "imágenes y video. Abarca tareas como clasificación de imágenes, detección de "
            "objetos, segmentación y reconocimiento óptico de caracteres."
        ),
        "ejemplo": "Inspección visual automática que detecta piezas defectuosas en una línea de producción.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 18,
        "termino": "Agente de IA e IA agéntica",
        "ingles": "AI Agent / Agentic AI",
        "categoria": "Aplicaciones",
        "definicion": (
            "Un agente de IA es un programa autónomo que cumple objetivos en nombre de un "
            "usuario: diseña su propio flujo de trabajo y usa herramientas externas sin "
            "supervisión constante. La IA agéntica es un sistema de varios agentes "
            "coordinados para resolver tareas más complejas que las de un agente solo."
        ),
        "ejemplo": "Un agente que compara vuelos, elige el mejor y realiza la reservación.",
        "fuente": FUENTE_IA,
    },
    {
        "id": 19,
        "termino": "Alucinación de IA",
        "ingles": "AI Hallucination",
        "categoria": "Ética y riesgos",
        "definicion": (
            "Situación en la que un modelo genera información falsa o engañosa pero "
            "expresada de forma convincente. Es una de las limitaciones principales de los "
            "LLM y obliga a verificar sus respuestas antes de usarlas."
        ),
        "ejemplo": "Un modelo que inventa una cita bibliográfica que nunca existió.",
        "fuente": FUENTE_LLM,
    },
    {
        "id": 20,
        "termino": "Sesgo y gobernanza de la IA",
        "ingles": "AI Bias & AI Governance",
        "categoria": "Ética y riesgos",
        "definicion": (
            "El sesgo aparece cuando los datos de entrenamiento favorecen sistemáticamente a "
            "unos grupos sobre otros, por ejemplo reforzando estereotipos en procesos de "
            "contratación. La gobernanza de la IA es el conjunto de políticas, controles y "
            "mecanismos de supervisión —explicabilidad, equidad, robustez, transparencia y "
            "privacidad— que buscan que los sistemas sean seguros y éticos."
        ),
        "ejemplo": "Auditar un modelo de selección de personal para verificar que no discrimine.",
        "fuente": FUENTE_IA,
    },
]

ANCHO = 78  # Ancho de línea para el formato de la consola


# --------------------------------------------------------------------------- #
# Utilidades de presentación
# --------------------------------------------------------------------------- #

def normalizar(texto):
    """Pasa el texto a minúsculas y le quita acentos, para buscar sin tildes."""
    texto = texto.lower()
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def titulo(texto, caracter="="):
    """Imprime un encabezado centrado entre líneas decorativas."""
    print()
    print(caracter * ANCHO)
    print(texto.center(ANCHO))
    print(caracter * ANCHO)


def parrafo(texto, sangria=4):
    """Imprime un texto ajustado al ancho de la consola con sangría."""
    espacios = " " * sangria
    print(textwrap.fill(texto, width=ANCHO, initial_indent=espacios,
                        subsequent_indent=espacios))


def mostrar_termino(entrada, detallado=True):
    """Muestra una ficha del término del glosario."""
    print()
    print(f"[{entrada['id']:02d}] {entrada['termino'].upper()}")
    print(f"     ({entrada['ingles']}) · Categoría: {entrada['categoria']}")
    print("-" * ANCHO)
    parrafo(entrada["definicion"])
    if detallado:
        print()
        parrafo(f"Ejemplo: {entrada['ejemplo']}")
        parrafo(f"Fuente:  {entrada['fuente']}")


def categorias():
    """Devuelve la lista de categorías en el orden en que aparecen."""
    vistas = []
    for entrada in GLOSARIO:
        if entrada["categoria"] not in vistas:
            vistas.append(entrada["categoria"])
    return vistas


# --------------------------------------------------------------------------- #
# Funciones del glosario
# --------------------------------------------------------------------------- #

def listar_todo(detallado=True):
    """Muestra los 20 términos agrupados por categoría."""
    titulo("GLOSARIO DE INTELIGENCIA ARTIFICIAL (20 TÉRMINOS)")
    for categoria in categorias():
        print()
        print(f">> {categoria.upper()}")
        for entrada in GLOSARIO:
            if entrada["categoria"] == categoria:
                mostrar_termino(entrada, detallado)


def listar_indice():
    """Muestra solo la lista numerada de términos."""
    titulo("ÍNDICE DE TÉRMINOS")
    for entrada in GLOSARIO:
        print(f" {entrada['id']:02d}. {entrada['termino']:<45} [{entrada['categoria']}]")


def buscar(texto):
    """Busca la palabra clave en el término, la traducción y la definición."""
    clave = normalizar(texto.strip())
    if not clave:
        print("\n  Escribe al menos una palabra para buscar.")
        return []

    resultados = [
        e for e in GLOSARIO
        if clave in normalizar(e["termino"])
        or clave in normalizar(e["ingles"])
        or clave in normalizar(e["definicion"])
    ]

    titulo(f"RESULTADOS PARA: '{texto.strip()}'")
    if not resultados:
        print("\n  Sin coincidencias. Intenta con otra palabra, por ejemplo: red, modelo, datos.")
    else:
        print(f"\n  {len(resultados)} término(s) encontrado(s).")
        for entrada in resultados:
            mostrar_termino(entrada)
    return resultados


def filtrar_por_categoria():
    """Permite elegir una categoría y muestra sus términos."""
    lista = categorias()
    titulo("CATEGORÍAS")
    for i, categoria in enumerate(lista, start=1):
        total = sum(1 for e in GLOSARIO if e["categoria"] == categoria)
        print(f"  {i}. {categoria} ({total} términos)")

    opcion = input("\n  Elige una categoría (0 para regresar): ").strip()
    if not opcion.isdigit() or not 1 <= int(opcion) <= len(lista):
        return

    elegida = lista[int(opcion) - 1]
    titulo(elegida.upper())
    for entrada in GLOSARIO:
        if entrada["categoria"] == elegida:
            mostrar_termino(entrada)


def ver_detalle():
    """Muestra un término a partir de su número."""
    listar_indice()
    opcion = input("\n  Número del término (0 para regresar): ").strip()
    if not opcion.isdigit() or not 1 <= int(opcion) <= len(GLOSARIO):
        return
    mostrar_termino(GLOSARIO[int(opcion) - 1])


def modo_estudio(rondas=5):
    """Cuestionario: se muestra una definición y hay que elegir el término."""
    titulo("MODO ESTUDIO")
    print("\n  Se mostrará una definición y deberás elegir a qué término corresponde.")

    preguntas = random.sample(GLOSARIO, k=min(rondas, len(GLOSARIO)))
    aciertos = 0

    for numero, correcta in enumerate(preguntas, start=1):
        distractores = random.sample([e for e in GLOSARIO if e["id"] != correcta["id"]], 3)
        opciones = distractores + [correcta]
        random.shuffle(opciones)

        print("\n" + "-" * ANCHO)
        print(f"  Pregunta {numero} de {len(preguntas)}")
        parrafo(correcta["definicion"])
        print()
        for letra, entrada in zip("abcd", opciones):
            print(f"    {letra}) {entrada['termino']}")

        respuesta = input("\n  Tu respuesta (a/b/c/d, o 's' para salir): ").strip().lower()
        if respuesta == "s":
            break
        elegida = None
        if respuesta in ("a", "b", "c", "d"):
            elegida = opciones["abcd".index(respuesta)]

        if elegida is not None and elegida["id"] == correcta["id"]:
            aciertos += 1
            print("  ¡Correcto!")
        else:
            print(f"  Incorrecto. La respuesta era: {correcta['termino']}.")

    print("\n" + "-" * ANCHO)
    print(f"  Resultado final: {aciertos} acierto(s).")


def exportar_csv(ruta="glosario_ia.csv"):
    """Guarda el glosario completo en un archivo CSV."""
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            campos = ["id", "termino", "ingles", "categoria", "definicion", "ejemplo", "fuente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(GLOSARIO)
    except OSError as error:
        print(f"\n  No se pudo escribir el archivo: {error}")
        return False
    print(f"\n  Glosario exportado en: {ruta}")
    return True


# --------------------------------------------------------------------------- #
# Menú principal
# --------------------------------------------------------------------------- #

MENU = """
  1. Ver el glosario completo
  2. Ver el índice de términos
  3. Consultar un término por número
  4. Buscar por palabra clave
  5. Filtrar por categoría
  6. Modo estudio (cuestionario)
  7. Exportar a CSV
  0. Salir
"""


def menu():
    """Ciclo principal de la aplicación."""
    titulo("GLOSARIO DE INTELIGENCIA ARTIFICIAL")
    print("\n  20 términos basados en la documentación de IBM Think sobre IA.")

    while True:
        print(MENU)
        try:
            opcion = input("  Opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Hasta luego.")
            break

        if opcion == "1":
            listar_todo()
        elif opcion == "2":
            listar_indice()
        elif opcion == "3":
            ver_detalle()
        elif opcion == "4":
            buscar(input("\n  Palabra a buscar: "))
        elif opcion == "5":
            filtrar_por_categoria()
        elif opcion == "6":
            modo_estudio()
        elif opcion == "7":
            exportar_csv(input("\n  Nombre del archivo [glosario_ia.csv]: ").strip() or "glosario_ia.csv")
        elif opcion == "0":
            print("\n  Hasta luego.")
            break
        else:
            print("\n  Opción no válida. Elige un número del menú.")


def main(argv=None):
    """Punto de entrada: procesa los argumentos de línea de comandos."""
    analizador = argparse.ArgumentParser(
        description="Glosario de 20 términos de Inteligencia Artificial."
    )
    analizador.add_argument("--listar", action="store_true", help="imprime el glosario completo")
    analizador.add_argument("--buscar", metavar="PALABRA", help="busca una palabra clave")
    analizador.add_argument("--exportar", metavar="ARCHIVO", help="exporta el glosario a CSV")
    args = analizador.parse_args(argv)

    if args.listar:
        listar_todo()
    elif args.buscar:
        buscar(args.buscar)
    elif args.exportar:
        exportar_csv(args.exportar)
    else:
        menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
