# DB health

Run these checks after touching any DB file, or any time you want to know the DB is in shape. CI runs them on every push, so a red check here will block you there.

## The daily three

```bash
python3 scripts/generate_manifests.py       # rebuild index, manifests, hunt cards
python3 scripts/db_quality_check.py         # the verdict
python3 scripts/build_db_graph.py           # rebuild the related-variant graph
```

`db_quality_check.py` prints one of three overall ratings: HEALTHY, DEGRADED, or BROKEN. HEALTHY means zero critical issues and zero warnings. As of this writing the DB sits at 337 entries with 2,002 patterns and 1,560 hunt cards across 18 manifests: 337/337 on frontmatter coverage, 296/337 on structural compliance, 0 critical issues and 97 warnings — an overall DEGRADED rating driven entirely by the structural warnings.

What the check covers, in its own nine skills: entry compliance against TEMPLATE.md, manifest integrity, hunt-card consistency, router integrity, pipeline script presence, context delivery (line ranges actually point at pattern headings), coverage and orphan detection, graph artifact health, and partition bundle health.

## When things drift

Symptoms and fixes, from most to least common:

Stale manifests after editing entries. You edited `DB/**/*.md` and did not regenerate. Run `generate_manifests.py` and commit the result. The CI freshness step catches this and names the stale file.

Line-range mismatches. Same cause. Manifests store `lineStart` per pattern heading; editing an entry above a pattern shifts the line. Regeneration fixes all of them at once, which is why you never fix ranges by hand.

Artifacts disagree about content. Both `generate_manifests.py` and `generate_micro_directives.py` write hunt-card metadata. If someone changes one without the other, the committed artifact depends on generator order and the CI freshness check fails. The two writers are kept in sync deliberately; if you add a third writer, make it emit the same strings.

Graph out of date after entry changes. Run `build_db_graph.py`. The CLI equivalent is `horus db graph`, which rebuilds and validates in one step. The graph is gitignored and rebuilt on demand; the wiki files under `DB/graphify-out/wiki/` are tracked and regenerate with it.

## The monitoring skill

`db-quality-monitor` runs the same checks with diagnosis attached, and can fix what it finds by spawning sub-agents for entry repair, migration, or manifest regeneration. It also does gap analysis: entries with weak signal or missing guards become drafts in `DB/_drafts/`, and per-card miss rates land in `DB/_telemetry/` so the catcher can prioritize cards with a history of being missed.

## Retrieval validation

```bash
python3 scripts/validate_retrieval_pipeline.py
```

The end-to-end version: compiles the scripts, runs the unit tests, runs the quality check, validates hunt-card regexes (1,560 of them), smoke-tests grep-prune and partitioning, checks graph queries, verifies generated artifacts are fresh, and checks Codex surface parity. If this passes locally, CI will pass.
