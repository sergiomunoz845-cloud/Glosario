# Glosario de Inteligencia Artificial — versión web

Sitio web hecho con **Flask** que publica los 20 términos de IA del proyecto de consola.
Las definiciones provienen de la documentación de IBM Think.

## Estructura del proyecto

```
glosario_web/
├── app.py                  Servidor Flask: rutas y filtros
├── glosario_ia.py          Datos del glosario (el mismo archivo de la versión de consola)
├── exportar_estatico.py    Genera un HTML autónomo, sin servidor
├── requirements.txt        Dependencias
├── static/
│   ├── estilos.css         Diseño de la página
│   └── glosario.js         Búsqueda en vivo y cuestionario
└── templates/
    ├── base.html           Plantilla común (encabezado, pie, tipografías)
    ├── index.html          Portada: buscador, índice, fichas, modo estudio
    ├── termino.html        Ficha individual de un término
    └── 404.html            Página de error
```

## Cómo ejecutarlo

En Windows, macOS o Linux, dentro de la carpeta del proyecto:

```bash
python -m venv venv                  # 1. entorno virtual (opcional pero recomendado)
source venv/bin/activate             # en Windows: venv\Scripts\activate
pip install -r requirements.txt      # 2. instalar Flask
python app.py                        # 3. arrancar el servidor
```

Luego abre **http://127.0.0.1:5000** en el navegador. Para detenerlo, `Ctrl + C`.

## Rutas

| Ruta | Qué hace |
|------|----------|
| `/` | Portada con los 20 términos, buscador y filtros |
| `/?q=red` | Busca la palabra en el término, su nombre en inglés y la definición |
| `/?categoria=Fundamentos` | Muestra solo una categoría |
| `/termino/12` | Ficha individual del término número 12 |
| `/api/glosario` | Los 20 términos en JSON |

La búsqueda funciona de dos maneras: con JavaScript filtra al instante sin recargar, y si el
navegador lo tiene desactivado el formulario se envía a Flask, que hace el filtrado en Python.

## Entregar la página sin servidor

Si necesitas subirla a GitHub Pages o entregar un solo archivo:

```bash
python exportar_estatico.py
```

Genera `glosario_ia_web.html` con el CSS, el JavaScript y los datos incrustados. Se abre con
doble clic y conserva la búsqueda, los filtros y el cuestionario. Lo único que deja de existir
es la ruta `/api/glosario`, porque ya no hay servidor de Python.

## Publicarlo en internet con Python

Opciones gratuitas donde corre Flask: **PythonAnywhere**, **Render** o **Railway**. En todas
se sube el proyecto, se instala `requirements.txt` y se indica `app.py` como punto de entrada.
Al desplegarlo, cambia la última línea de `app.py` a `app.run()` sin `debug=True`.

## La versión de consola

`glosario_ia.py` sigue funcionando por su cuenta:

```bash
python glosario_ia.py            # menú interactivo
python glosario_ia.py --listar   # glosario completo en la terminal
```

## Fuentes

- IBM Think, ¿Qué es la inteligencia artificial? — https://www.ibm.com/mx-es/think/topics/artificial-intelligence
- IBM Think, ¿Qué son los LLM? — https://www.ibm.com/mx-es/think/topics/large-language-models
