# Workflow docs

Short guides for what Horus does and which skills do what. Read the one that matches the job you have.

| Doc | When to read it |
|---|---|
| [full-audit.md](full-audit.md) | You have a codebase and want a full security review of it |
| [../agents-reference.md](../agents-reference.md) | You want to know what one specific agent does and when to use it |
| [db-lookup.md](db-lookup.md) | You want to check one vulnerability topic against the DB |
| [bulk-scan.md](bulk-scan.md) | You want to grep a whole codebase with every hunt card at once |
| [db-authoring.md](db-authoring.md) | You want to add or edit vulnerability entries |
| [invariants-and-fv.md](invariants-and-fv.md) | You want to extract invariants and verify them with fuzzers or provers |
| [mitigation-review.md](mitigation-review.md) | A sponsor shipped fixes and you need to verify them |
| [db-health.md](db-health.md) | You changed DB files or want to know if the DB is healthy |

Two things apply to every workflow here.

First, retrieval goes through tiers. `DB/index.json` routes you to a manifest, the manifest gives you line ranges, you read those lines and nothing else. The full tier flow is in [db-lookup.md](db-lookup.md).

Second, edit sources, not artifacts. The manifests, hunt cards, graph JSON, and Codex mirrors are all generated. Change the `DB/**/*.md` files or the `.claude/` playbooks, then run the generators. Hand-edited generated files get overwritten and fail CI.
