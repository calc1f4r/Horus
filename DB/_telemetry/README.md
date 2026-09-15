# Hunt Card Telemetry

This directory is for sidecar performance notes about generated hunt cards.

Use it for:

- cards that repeatedly produce false positives
- cards that missed confirmed findings
- cards that correctly caught findings and should be kept strong
- suggested grep, triage, or source Markdown improvements

Rules:

- Telemetry files do not change runtime behavior by themselves.
- Telemetry must not be loaded into manifests, hunt cards, or graph artifacts.
- Any actual hunt-card improvement must be made in canonical `DB/**/*.md` source content or generator logic, then regenerated.

The generator currently ignores `DB/_telemetry/`.

The current durable enrichment inventory lives under:

```text
DB/_telemetry/huntcard-enrichment/
```

The cross-DB checklist lives at:

```text
DB/_telemetry/huntcard-enrichment/CHECKLIST.md
```
