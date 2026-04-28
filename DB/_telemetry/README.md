# Hunt Card Telemetry

This directory stores per-hunt-card telemetry sidecars produced by
`db-quality-monitor --gap-analysis`.

Telemetry is advisory only. It tracks hits, misses, false positives, last audit,
and suggested refinements so humans can improve hunt cards without automatically
changing canonical DB entries.

These files are not part of runtime search and must not be indexed into
manifests.
