# Copilot instructions for this repository

This project is a Spanish-language AI glossary website built with Flask.

## Scope
- Maintain the glossary as a data-first project.
- Keep the underlying data in `glosario_ia.py` aligned with the UI and exports.
- Favor simple Flask patterns and avoid over-engineering.

## Constraints
- Do not break the web routes defined in `app.py`.
- Preserve support for category filters, live search, and the static export produced by `exportar_estatico.py`.
- Keep content in Spanish and English aligned with the glossary entries.
- Prefer compatibility with existing templates and static assets.

## Verification
Run a Python syntax check after edits:

```bash
python -m compileall app.py glosario_ia.py exportar_estatico.py
```
