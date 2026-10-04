# Agent reference

Every agent in Horus, what it does, and when to reach for it. 49 of them live in `.claude/agents/`; each has a skill of the same name in `.claude/skills/` that is just a thin invocation wrapper. The agent file holds the real instructions.

If you want the flow instead of the catalog (who runs in what order during an audit), read [workflows/full-audit.md](workflows/full-audit.md).

## Languages

The pipeline is language-agnostic. `recon-specialist` records the target's `language` and `ecosystem` in the scope block, and every agent reads them — no agent assumes Solidity. Patterns documented in one language get translated to the target (an EVM `msg.sender` spoofing pattern becomes a missing signer/authority check in a Rust handler); hunt cards carry an informational `languages` tag for exactly this. Nothing filters cards by language.

| Target | language | ecosystem | PoC command | FV |
|---|---|---|---|---|
| Foundry/Hardhat contracts | solidity / vyper | evm | `forge test` | full EVM suite |
| Solana programs | rust | solana | `anchor test` | gated off |
| Sui / Aptos | move | sui / aptos | `sui move test` | Sui provers |
| Cosmos SDK chains | go | cosmos | `go test` | gated off |
| Rust services, L1 nodes | rust | native | `cargo test` | gated off |
| Go services | go | native | `go test` | gated off |
| C++ nodes / clients | cpp | native | `ctest` | gated off |

The EVM/Sui formal-verification and fuzzing agents (`chimera-setup`, `medusa-fuzzing`, `halmos-verification`, the Certora pair, `sui-prover-verification`) are tool-specific by design; the orchestrator skips them with a logged reason when the target is outside their ecosystem.

## Quick picker

| You want to... | Reach for |
|---|---|
| Audit a codebase end to end | `audit-orchestrator` |
| Check one known vulnerability topic | `invariant-catcher` |
| Find novel bugs reasoning can catch but patterns cannot | `protocol-reasoning` |
| Check a known fork against its incident history | `prior-art-matcher` |
| Verify a sponsor's shipped fixes | `mitigation-reviewer` |
| Write properties and prove them | `invariant-writer`, then the FV skills |
| Add DB entries from audit reports | `variant-template-writer` |
| Add DB entries from real exploits | `defihacklabs-indexer` |
| Decide severity for one platform | that platform's judge |
| Compare severity across platforms | `judge-orchestrator` |
| Know if the DB is healthy | `db-quality-monitor` |

## Orchestration and context

| Agent | What it does | When to use |
|---|---|---|
| `audit-orchestrator` | Runs the whole 11-phase pipeline: recon through report, with judges, PoCs, and gates in between | Any full audit. Everything below is either spawned by it or usable standalone |
| `recon-specialist` | Phase 1. Detects protocol type, resolves in/out-of-scope files with reasons, maps external surface, computes diff blast radius. Writes `00-scope.md` with the JSON block the scan scripts consume | Start of any audit, or standalone when scope must be settled before hunting |
| `audit-context-building` | Phase 2 coordinator. Fans out per-contract analysis, then synthesizes | When you need deep architecture context, threat models, or before invariant work |
| `function-analyzer` | Line-by-line analysis of one contract. Pure context, no hunting | Spawned by the coordinator above; run it yourself only for a single-file deep read |
| `system-synthesizer` | Merges per-contract notes into one global context doc | Spawned by the coordinator; not useful standalone |
| `multi-persona-orchestrator` | Runs six analysis strategies over the same code: BFS, DFS, working backward from sinks, state machine, mirror pairs (deposit vs withdraw), re-implementation diff | Phase 4 lane 4C, or standalone when you want many reading strategies on one target |
| `persona-*` (six of them) | The individual strategies above | Only through the orchestrator |
| `finding-merger` | Phase 5. Clusters findings by root cause, falsifies each cluster against the code, guarantees nothing is silently dropped | After any multi-source discovery pile; also standalone to triage findings from anywhere |
| `attack-coverage-tracker` | Tracks which functions each lane attacked in which round; emits round targets pointing at unattacked surface | Between discovery rounds. Finds no bugs itself; makes the other lanes find more |

## Discovery

| Agent | What it does | When to use |
|---|---|---|
| `invariant-catcher` | Hunts known DB patterns: pulls hunt cards, greps the target, writes cited findings | One topic or a full bulk scan. The pattern-matching workhorse |
| `protocol-reasoning` | Decomposes the code into domains and reasons from first principles, seeded by generalized DB root causes (not keywords). Four rounds: standard, cross-domain, edge cases, completeness | Novel and compositional bugs. Requires reasoning seeds first; the agent can generate them itself |
| `missing-validation-reasoning` | Zero-address checks, stale oracle reads, array length mismatches, unvalidated inputs in constructors and setters | Hygiene pass; cheap and specific |
| `prior-art-matcher` | Fingerprints the target against protocol lineages (Aave, Compound, Uniswap, Curve, and others), then pulls prior audits and DeFiHackLabs incidents for that lineage, with inherited/modified/fixed verdicts | Before discovery when the target is a fork or fork-adjacent. "Audit an Aave fork" is won with Aave's incident history |
| `attack-graph-synthesizer` | Walks the code graph against the invariant suite to enumerate multi-step attack chains | After discovery, when a graph exists. Produces candidates for `protocol-reasoning` to validate |
| `finding-chain-synthesizer` | Chains already-confirmed findings into emergent multi-step exploits no single finding shows | After triage or judging, when you have confirmed findings worth composing |
| `tokenomics-auditor` | Token supply, emission, vesting, treasury, fee splits: value flows over time, math checked against documented tokenomics | Phase 4 lane 4E, when scope has token or vesting contracts |
| `risk-parameter-reviewer` | LTV, liquidation thresholds and bonuses, IRM kinks, peg mechanics; sweeps scenarios for the breaking regime | Phase 4 lane 4F, when lending or stablecoin mechanics are in scope |
| `manipulation-feasibility-analyst` | For every price feed: capital required to move it versus profit extractable from its consumers; MEV surface ranking | Phase 4 lane 4G, when anything reads a price. Turns "uses TWAP, safe" into numbers |

## Proof and validation

| Agent | What it does | When to use |
|---|---|---|
| `economic-attack-simulator` | Profit model per candidate attack: flash-loan cost, slippage, gas, MEV competition. Verdict PROFITABLE, CONDITIONAL, or UNPROFITABLE with the binding constraint named | Phase 6a gate before PoC spend, or to quantify impact for judges |
| `poc-writing` | Writes and runs minimal exploit tests that reproduce on-chain conditions | Any finding that needs proof. A passing PoC ends arguments |
| `chimera-setup` | One property-test scaffold that runs Echidna, Medusa, and Halmos from the same codebase | When you want all three fuzzers on one invariant spec |
| `medusa-fuzzing` | Medusa harnesses: property tests, ghost variables, actor proxies | When Medusa specifically |
| `halmos-verification` | Halmos symbolic tests (`check_` prefix, symbolic cheatcodes) | Exhaustive input-space verification inside Foundry |
| `certora-verification` | Certora CVL specs and configs | When you need a prover rather than a fuzzer |
| `certora-mutation-testing` | Mutates the code under test and checks the spec catches the mutants; triages survivors into equivalent, setup artifact, or true spec gap | After a baseline CVL spec exists, to find out if it actually says anything |
| `certora-sui-move-verification` | CVLM specs for Sui Move | Sui targets, Certora flavor |
| `sui-prover-verification` | Sui Prover specs, requires/ensures style | Sui targets, the other flavor |

## Invariants

| Agent | What it does | When to use |
|---|---|---|
| `invariant-writer` | Extracts all system properties into one spec, positive mode and adversarial mode | Before fuzzing or FV; also early in audits to define what "broken" means |
| `invariant-reviewer` | Re-derives the protocol, checks the spec against canonical invariants for its type, fixes over- and under-specification | Always after the writer. First drafts of invariants are half right |
| `invariant-indexer` | Builds reference libraries of invariants from major protocols and their FV specs | Growing `invariants/`; on demand for a named protocol |

## Judging and reporting

| Agent | What it does | When to use |
|---|---|---|
| `judge-orchestrator` | Runs all three platform judges in parallel, resolves divergences, keeps a verdict memory log | Cross-platform severity consensus, or deciding where to submit |
| `sherlock-judging` / `cantina-judge` / `code4rena-judge` | One platform's validity and severity rules each | When the target platform is already decided |
| `issue-writer` | Polishes a validated finding into a submission-ready write-up | After triage. Accepts profitability figures from the simulator as impact evidence |
| `report-aggregator` | Assembles `CONFIRMED-REPORT.md` from judge-verified findings, citations checked | End of an audit, or standalone to compile findings from any source |
| `remediation-safety-checker` | Verifies the fixes your own report recommends: root-cause coverage, blast radius, honest-flow impact, fix interactions, invariant compliance, and whether the fix pattern is itself in the DB as vulnerable | Between polishing and report assembly. UNSAFE remediations cannot ship |
| `mitigation-reviewer` | Verifies a sponsor's applied fix diff: FIXED, PARTIALLY FIXED, NOT FIXED, or FIXED BUT INTRODUCED NEW ISSUE, plus a regression hunt | Separate engagement after fixes ship |

## DB maintenance

| Agent | What it does | When to use |
|---|---|---|
| `solodit-fetching` | Pulls raw findings from the Solodit API by topic into `reports/` | Raw material for entry writing |
| `variant-template-writer` | Synthesizes 5+ reports per pattern into TEMPLATE-compliant entries with cross-report severity consensus | Turning fetched reports into DB growth |
| `defihacklabs-indexer` | Builds attack-graph entries from executable exploit PoCs, extracting multi-step flow rather than summaries | Indexing the DeFiHackLabs corpus |
| `findings-db-synthesizer` | Turns your own confirmed findings into DB entries and invariants; dedups first | After a report ships. Opt-in flywheel |
| `db-quality-monitor` | Runs all DB health checks with diagnosis, can auto-remediate, and does gap analysis into `_drafts/` and `_telemetry/` | Periodic checks, after entry changes, or when an audit got wrong context from the DB |

## Non-security

| Agent | What it does | When to use |
|---|---|---|
| `improve-codebase-architecture` | Reads domain language and ADRs, proposes refactors that improve locality and navigability | When the target is software quality, not vulnerabilities |

## How they relate

Agents talk through `audit-output/` files only. One agent's output file is the next one's input contract; the schemas live in `.claude/resources/inter-agent-data-format.md`. The orchestrator owns the phase order and the state file. Everything else can run standalone when you feed it the files it names in its own doc.
