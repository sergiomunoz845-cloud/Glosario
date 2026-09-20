# AGENTS.md

## Project overview
This repository contains a Flask-based glossary of artificial intelligence terms. The app shares its source data with the console version and exposes the content through routes, templates, and static assets.

## Key files
- `app.py`: Flask server, routes, filters, and error handling.
- `glosario_ia.py`: canonical glossary data and helper functions.
- `exportar_estatico.py`: builds a single-file static HTML export.
- `templates/`: Jinja templates for the site.
- `static/`: CSS and JavaScript for front-end behavior.

## Development rules
- Treat `glosario_ia.py` as the single source of truth for glossary entries.
- Keep `id`, `termino`, `ingles`, `categoria`, `definicion`, and `ejemplo` consistent when updating content.
- Preserve the current site behavior: search, category filters, and the individual term detail page.
- Prefer small, clear changes. Do not introduce unnecessary dependencies.
- If changing routes or data structures, update the related template usage and README references.

## Validation
Before considering work complete, run a syntax check for the Python files:

```bash
python -m compileall app.py glosario_ia.py exportar_estatico.py
```

If the app behavior was changed, also run a quick local smoke test with:

```bash
python app.py
```

Then confirm the home page loads and the filtered search still works in the browser.
