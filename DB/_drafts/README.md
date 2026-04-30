# Draft DB Entries

This directory is for automatically drafted or agent-suggested vulnerability entries that are not yet part of the live Horus database.

Rules:

- Files here must follow `TEMPLATE.md` before promotion.
- Files here must not be loaded into `DB/index.json`, manifests, hunt cards, or graph artifacts.
- Promotion is manual: move a reviewed draft into the appropriate `DB/<category>/` directory, then run:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
python3 scripts/build_db_graph.py
```

The generator currently ignores `DB/_drafts/`.

