# Draft DB Entries

This directory holds auto-generated draft vulnerability entries from
`db-quality-monitor --gap-analysis`.

Drafts are not part of the runtime DB and must not be indexed into manifests.
To promote a draft:

1. Review it against `TEMPLATE.md`.
2. Move it into the appropriate `DB/<category>/...` directory.
3. Remove `status: draft` from frontmatter.
4. Run `python3 scripts/generate_manifests.py`.
5. Run `python3 scripts/db_quality_check.py`.

