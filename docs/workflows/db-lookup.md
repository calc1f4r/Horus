# DB lookup

Use this when you have one vulnerability topic in mind and want to know what Horus already knows about it. Takes minutes, not hours.

## The four tiers

```
Tier 1    DB/index.json                     router, ~430 lines
Tier 1.5  DB/manifests/huntcards/*.json     one compressed card per pattern
Tier 2    DB/manifests/*.json               pattern index with line ranges
Tier 2.5  DB/graphify-out/graph.json        related-variant expansion
Tier 3    DB/**/*.md                        the entries themselves
```

Start at tier 1 and go down only as far as you need. Reading whole entry files defeats the design.

## Walkthrough: oracle manipulation on a lending fork

Open `DB/index.json`. Under `protocolContext.mappings`, `lending_protocol` lists its manifests: `lending`, `oracle`, `general-defi`, `tokens`, `general-security`. It also lists focus patterns: liquidation, bad debt, health factor, self liquidation, interest accrual, and more.

Load the matching hunt cards, say `DB/manifests/huntcards/oracle-huntcards.json`. Each card carries a `grep` pattern, `detect` and `check` micro-directives, a severity, and a `ref` pointing back into a `DB/*.md` entry with `lines`.

When a card matches your situation, open the manifest at tier 2 (`DB/manifests/oracle.json`), find the pattern, and read exactly the `lineStart` to `lineEnd` range in the entry file. That slice has the root cause, detection patterns, false-positive guards, exploit scenarios, and references.

## Two shortcuts

The keyword index: `DB/manifests/keywords.json` maps code terms to manifests. Seeing `getPriceUnsafe` in the target points you straight at the `oracle` manifest.

The graph: `graphify query oracle flash loan --graph DB/graphify-out/graph.json` returns related nodes across categories you might have missed, like sequencer-downtime patterns that hit oracle consumers. Graph results expand your search. They never remove baseline hunt cards.

## The skill that does this for you

`invariant-catcher` runs this flow end to end. Give it a topic and a codebase and it pulls the right hunt cards, greps the target, and writes structured findings with citations back to the DB. For one topic on one codebase, that is the whole job:

```
/agent invariant-catcher <codebase-path> --topic "oracle staleness"
```

For scanning a codebase against every card at once, see [bulk-scan.md](bulk-scan.md).
