# Bulk scan

Use this when you want to run the entire hunt-card corpus against a codebase and have humans or agents work through everything that matches. This is the 4A lane of a full audit, run standalone.

## The loop

Three scripts, in order:

```bash
# 1. Grep-prune: keep only cards whose pattern hits the target
python3 scripts/grep_prune.py <target_path> DB/manifests/huntcards/all-huntcards.json \
  --scope-file audit-output/00-scope.md \
  --output audit-output/hunt-card-hits.json

# 2. Partition the survivors into shards of 50-80 cards, grouped by category
python3 scripts/partition_shards.py audit-output/hunt-card-hits.json \
  --scope-file audit-output/00-scope.md \
  --output audit-output/hunt-card-shards.json

# 3. After the shard work, merge the findings back into one report
python3 scripts/merge_shard_findings.py audit-output
```

## What each step actually does

`grep_prune.py` runs every card's grep pattern against the target with ripgrep and records which files and lines hit. Cards with zero hits get dropped. Cards marked `neverPrune` survive no matter what, as a safety net. Cards whose search command errors survive too, flagged `searchError` for manual review instead of being silently lost.

`partition_shards.py` groups surviving cards by category tag and splits them into shards sized for one agent context. The neverPrune set is duplicated into every shard so each worker sees the safety-net cards.

The shard work itself is done by `invariant-catcher` sub-agents, one per shard. Each gets a shard file, reads only the code its cards point at, and writes findings in the shared schema. That part is parallel by construction: shards share no state.

`merge_shard_findings.py` stitches the per-shard outputs back together, deduplicating findings that multiple shards hit from different cards.

## Scope restriction

`--scope-file` takes a `00-scope.md` from `recon-specialist` and parses the JSON block at the bottom. Hits outside the in-scope, diff, or blast file sets get dropped before pruning, and cards whose hits are all out of scope get pruned with them. This is how you scan a 400-file monorepo without burning agent context on vendored dependencies. Skip the flag when there is no scope file and you want everything scanned.

## Feeding the next step

Surviving cards also seed reasoning work. `extract_reasoning_seeds.py` turns each card's `detect` and `check` fields into generalized assumptions across five layers (input, state, ordering, economic, environmental) and writes `reasoning-seeds.md`, the input `protocol-reasoning` requires before it starts:

```bash
python3 scripts/extract_reasoning_seeds.py audit-output/hunt-card-hits.json \
  --output audit-output/reasoning-seeds.md
```

On the full corpus this produces 638 seeds from 1,362 cards. After grep-pruning you see far fewer, which is the point.
