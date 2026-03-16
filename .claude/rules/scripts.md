---
paths:
  - "scripts/**/*.py"
  - "generate_manifests.py"
  - "solodit_fetcher.py"
  - "generate_diagram.py"
---

# Python Script Rules

When editing Python scripts in this repo:

- Use `python3` explicitly (not `python`)
- Always activate venv first: `source .venv/bin/activate`
- `generate_manifests.py` is the canonical manifest generator — changes here affect the entire 4-tier search system
- `solodit_fetcher.py` fetches from the Cyfrin Solodit API — never apply quality filters
- Scripts in `scripts/` are utilities: classification, conversion, quality checks
- Do not add dependencies without updating `requirements.txt`
