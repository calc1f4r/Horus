---
vulnerability_class: cross_client_gas_divergence
title: "Cross-Client Gas Divergence: geth vs Nethermind (memory-expansion word cap, 30M edge)"
protocol: eth-l1-clients
category: Execution / Gas Metering
vulnerability_type: spec_divergence
attack_type: edge_case_gas_mismatch|chain_split_via_gas_limit_raise|trace_divergence
affected_component: memory_expansion_gas|gas_calculation|uint_casts
chain: ethereum
severity: medium
impact: consensus_divergence|chain_split|trace_divergence
severity_range: "LOW to HIGH (active when gas limit > 30M)"
source: Immunefi Ethereum Protocol Attackathon 2024-2025

primitives:
  - memory_word_cap_int32_vs_uint32
  - edge_case_memory_expansion_gas_mismatch
  - eof_push_opcode_trace_discrepancy
  - push0_missing_in_ispush

affected_components:
  - EVM memory expansion gas calculators
  - uint width casts in gas math
  - trace/debug output generation

tags:
  - gas
  - divergence
  - geth
  - nethermind
  - evm
  - memory_expansion
  - consensus
  - attackathon

total_reports_analyzed: 4

# Pattern Identity (Required)
root_cause_family: integer_width_or_bound_mismatch_in_gas_math
pattern_key: gas_divergence | memory_word_cap_int32_uint32 | chain_split_on_gas_limit_raise

# Interaction Scope
interaction_scope: consensus_math

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - memoryExpansion
  - toWordSize
  - uint32
  - int32
  - "0x1FFFFFFFE"
  - memoryGas
  - gasLimit
  - 30M / 30000000
  - PUSH0
  - IsPush
  - EOF
---

# Cross-Client Gas Divergence: geth vs Nethermind

## Overview

When two clients compute different gas for the same opcode input, every transaction hitting that
edge becomes a consensus bomb. The flagship case from the Attackathon:

**Immunefi #38319 [BC-Insight] — Edge case difference for GETH and NETHERMIND when calculating memory expansion gas (Omik, nethermind)**

Nethermind caps memory word size at **int32 max (2^31-1)** where geth caps at **uint32 max
(2^32-1)**. For memory-hungry opcodes with huge offsets, the two clients compute different
expansion gas once gas limits exceed ~30M. At the time of reporting the 30M mainnet gas limit kept
it dormant — the report explicitly scopes it under "opcode behavior at extremes". Any gas-limit
raise (gas limit is miner/vote-controlled, historically raised well beyond 30M — now 36M+ and
climbing) re-activates the divergence: a crafted tx with extreme memory offset charges different
gas in the two clients → different execution outcomes/state roots → chain split between client
classes.

**Root Cause Statement**: This vulnerability exists because gas-metering math uses different
integer widths/bounds per client (int32 vs uint32 word cap; differing overflow handling), so at
extreme-but-valid opcode inputs the clients charge different gas and diverge on execution results
— a latent chain split that activates when block gas limits rise enough to make the edge reachable.

**Observed Frequency**: structural (every gas formula is a per-client reimplementation; 4 accepted
divergence findings in one competition)
**Consensus Severity**: LOW today → HIGH/CRITICAL when reachable (gas limit dependent)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of integer_width_or_bound_mismatch_in_gas_math (int32 vs uint32 memory word cap)"
- Pattern key: `gas_divergence | memory_word_cap_int32_uint32 | chain_split_on_gas_limit_raise`
- Interaction scope: `consensus_math`
- Primary affected component(s): `memory_expansion_gas`
- High-signal code keywords: `toWordSize`, `int32`, `uint32`, `0x1FFFFFFFE`, `memoryExpansion`
- Typical sink / impact: `consensus_divergence` / `chain_split`
- Validation strength: `high` (differential test methodology in report)

#### Contract / Boundary Map

- Entry surface(s): any EVM opcode touching memory expansion (MLOAD/MSTORE*/CALLDATALOADCOPY/COPY family/CREATE/EXTCODE*, returns)
- Contract hop(s): `offset,size -> toWordSize (cap!) -> expansion cost -> total gas -> include/reject tx`
- Trust boundary crossed: `attacker-crafted transaction` (needs block gas limit ≥ edge threshold)
- Shared state or sync assumption: `identical gas math across all clients at ALL input sizes`

#### Valid Bug Signals

- Signal 1: `toWordSize`/equivalent saturates at different constants per client (grep `0x1FFFFFFFE` geth vs `int32.MaxValue` nethermind — nethermind uses Math/C# int casts)
- Signal 2: Any gas formula casting through a narrower signed type (`(int)`, `int32`, `i32`) where peers use unsigned
- Signal 3: Differential fuzz (goevmlab / statetest) shows same tx, different gas-used or post-state between two clients at extreme offsets
- Signal 4: Gas math documented as unreachable under "current gas limit" — flag as latent, activation-gated

#### False Positive Guards

- Not this bug when: divergence requires gas limit beyond any plausible raise AND opcode input beyond uint64 offsets (truly unreachable)
- Safe if: shared gas crate/library (evmone/revm-style) used by both clients — still verify per-client wrappers
- Requires attacker control of: tx calldata/offsets + network gas-limit conditions (vote/miner, not attacker-only — hence "latent")
- Trace-only divergences (debug_* output differs, consensus same) are LOW severity — but see #37483 EOF/PUSH trace discrepancy as the canonical example

## Real Reports

### 1. Immunefi #38319 [BC-Insight] — Edge case difference for GETH and NETHERMIND when calculating memory expansion gas

Report: `reports/eth-l1-clients_findings/38319-bc-insight-edge-case-difference-for-geth-and-nethermind-when-calculating-memory-expansion-gas.md`
Nethermind int32 cap vs geth uint32 cap; reachable when gas limit > 30M; flagged under
"opcode behavior at extremes" impact class.

### 2. Immunefi #37483 [BC-Insight] — Trace discrepancy for Nethermind when handling EOF from PUSH opcode

Report: `reports/eth-l1-clients_findings/37483-bc-insight-there-is-a-trace-discrepancy-for-nethermind-when-handling-eof-from-push-opcode.md`
Trace-level divergence (lower severity, same cross-client-diff methodology).

### 3. Immunefi #38557 [BC-Insight] — Function IsPush() misses opcode PUSH0

Report: `reports/eth-l1-clients_findings/38557-bc-insight-function-ispush-misses-opcode-push0.md`
Opcode classification gap post-EIP-3855 — affects tooling/traces built on IsPush.

### 4. Immunefi #38958 [BC-Low] — EELS can't handle overflow gas calculation in modexp precompile

Report: `reports/eth-l1-clients_findings/38958-bc-low-eels-cant-handle-overflow-gas-calculation-in-modexp-precompile.md`
Reference (EELS) vs geth/Nethermind divergence — the reference itself diverges; cross-listed in
`DB/eth-l1-clients/crypto/kzg-blob-validation.md`.

### Related: Berachain PoL gas consensus mismatch (Sigma Prime)

`reports/eth-l1-clients_findings/berachain-reth-geth-sigp-2025.md` — BRG4-02 "PoL Gas Limit
Consensus Mismatch Between Clients" (Critical): same class on a fork — two client implementations
disagree on gas limits for protocol-injected txs.

## Vulnerable Code Pattern (generic)

```csharp
// NETHERMIND (vulnerable class): word size capped at int32 max
long ToWordSize(long size) {
    size = Math.Max(size, 0);
    long words = (size + 31) / 32;
    return Math.Min(words, int.MaxValue);   // int32 cap  (2^31 - 1)
}
// GETH (reference): capped at uint32 max
func toWordSize(size uint64) uint64 {
    if size > math.MaxUint32-31 { return math.MaxUint32/32 + 1 } // uint32 cap (2^32 - 1)
    return (size + 31) / 32
}
// divergence window: offsets whose word count lands in (2^31-1, 2^32/32] => different gas
```

## Detection & Hunt Strategy

1. Build a gas-math diff matrix per opcode family (memory expansion, copy, create, call, log,
   precompiles) across geth / nethermind / besu / erigon / evmone / EELS — compare saturation
   constants and cast widths, not just formulas.
2. Grep every gas function for narrowing casts (`(int)`, `int32`, `i32`, `to_int`) and boundary
   constants (`0xFFFFFFFF`, `0x7FFFFFFF`, `MaxUint64/32`).
3. Differential fuzz with goevmlab/Statetest at extreme offset/size values
   (2^31±k, 2^32±k, 2^35...) — assert identical gasUsed and post-state across ≥3 clients.
4. Track activation gates: for each divergence, compute the minimum block gas limit that makes it
   reachable, and compare to current/plausible limits (the 30M guard in #38319 is a time bomb, not
   a fix).
5. For fork clients (berachain/geth forks), re-run the matrix on protocol-injected txs (PoL/system
   txs) — BRG4-02 shows these bypass normal gas plumbing.

## References

- `reports/eth-l1-clients_findings/38319-bc-insight-edge-case-difference-for-geth-and-nethermind-when-calculating-memory-expansion-gas.md`
- `reports/eth-l1-clients_findings/37483-bc-insight-there-is-a-trace-discrepancy-for-nethermind-when-handling-eof-from-push-opcode.md`
- `reports/eth-l1-clients_findings/38557-bc-insight-function-ispush-misses-opcode-push0.md`
- `reports/eth-l1-clients_findings/38958-bc-low-eels-cant-handle-overflow-gas-calculation-in-modexp-precompile.md`
- `reports/eth-l1-clients_findings/berachain-reth-geth-sigp-2025.md` (BRG4-02)
- `reports/eth-l1-clients_findings/38292-sc-medium-incorrect-sqrt-calculation-result.md`- `reports/eth-l1-clients_findings/38682-sc-medium-augassign-evaluation-order-causing-oob-write-within-the-object.md`- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/erigon-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/erigon-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/erigon-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/go-ethereum-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/go-ethereum-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/go-ethereum-docs-audits-2018-09-14-clef-audit-ncc-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-berachain-sigma-prime-berachain-reth-geth-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commitboost-multiplexer-signer-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commitboost-multiplexer-signer-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commitboost-multiplexer-signer-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commitboost-multiplexer-signer-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-eth-docker-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-2-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-2-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-2-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-drand-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-proofs-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-proofs-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/publications-audit-reports-peckshield-audit-report-bscstationstartpools-v1-0-pdf.md`- `reports/eth-l1-clients_findings/publications-ebridge-ethereum-bridge-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-ebridge-ethereum-bridge-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-2023-04-prysm-securityreview-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-eth2depositcli-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-eth2depositcli-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-eth2depositcli-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-erd-ethereum-reserve-dollar-smart-contract-security-assessment-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-seascape-lighthouse-smart-contract-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-seascape-lighthouse-smart-contract-security-audit-report-halborn-final-pdf.md`- `reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-bridge-ethereum-smart-contract-security-audit-halborn-v-1-1-pdf.md`- `reports/eth-l1-clients_findings/publicreports-solidity-smart-contract-audits-yieldly-finance-bridge-ethereum-smart-contract-security-audit-halborn-v-1-1-pdf.md`
- EIP-3855 (PUSH0), EIP-3860 (initcode gas), EVM gas specs (yellow paper appendix H)
- Immunefi/audit `37442` [BC-Insight] (erigon, INFO): Potential address collision with precompile contract during contract deployment — `reports/eth-l1-clients_findings/37442-bc-insight-potential-address-collision-with-precompile-contract-during-contract-deployment.md` (Immunefi (CertiK))
- Immunefi/audit `37593` [BC-Insight] (reth, INFO): Inconsistent address collision check against precompile contracts during contract deployment — `reports/eth-l1-clients_findings/37593-bc-insight-inconsistent-address-collision-check-against-precompile-contracts-during-contract-d.md` (Immunefi (CertiK))
