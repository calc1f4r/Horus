---
protocol: generic
chain: cosmos
category: ibc
vulnerability_type: wasm_client_validation

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_validation | 08_wasm_client | wasm_client_validation

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - WasmClientState (08-wasm)
  - wasmvm / CosmWasm-vm boundary
  - x/wasm governance approval flow
  - light-client wasm contract
path_keys:
  - missing_state_write | UpdateState | consensus state not set | client desync
  - missing_status_check | ClientState.Status | client marked Active | unverified client
  - missing_signer_validation | MsgPushNewWasmCode.ValidateBasic | signer unvalidated | governance bypass
  - vm_parameter_mismatch | wasmvm params unset | contract gas/memory limits | dos

# Attack Vector Details
attack_type: logical_error|dos
affected_component: wasm_light_client|wasmvm_boundary

# Technical Primitives
primitives:
  - wasm_light_client_contract
  - governance_code_approval
  - consensus_state_store
  - client_status_transition
  - vm_sandbox_parameters
  - gas_metering_in_vm

# Grep / Hunt-Card Seeds
code_keywords:
  - VerifyClientMessage
  - update_state
  - check_for_misbehaviour
  - ClientState.Status
  - StatusActive
  - MsgPushNewWasmCode
  - ValidateBasic
  - code_hash
  - wasmvm
  - StoreCode
  - GetConsensusState
  - SetConsensusState

# Impact Classification
severity: high
impact: state_corruption|dos|potential_fork_acceptance
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - cosmos
  - appchain
  - ibc
  - wasm
  - light-client
  - 08-wasm
  - cosmwasm
  - governance

language: go|rust
version: ibc-go 08-wasm (Feb 2023 Halborn audit; Jul 2023 Confio review)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### Halborn 08-wasm Audit (Feb 2023)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| HAL-01: Consensus state is not set in the WASM light client (UpdateState) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | MEDIUM | Halborn |
| HAL-02: wasmvm parameters are not set in the contract interaction | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | MEDIUM | Halborn |
| HAL-03: The status of client state is marked as Active by default | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | LOW | Halborn |
| HAL-04: Signer is not validated in the MsgPushNewWasmCode's ValidateBasic function | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | LOW | Halborn |
| HAL-05: gRPC-gateway routes are not registered | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | LOW | Halborn |
| HAL-08: Channel definition is missing on the MsgChannelOpen[...] | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | LOW | Halborn |
| HAL-09: Lack of conditional check when block height - block [time] | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md` | LOW | Halborn |

### Confio Architecture Review (Jul 2023)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| IBC Wasm Client Review — requirements, architecture, missing features (e.g., status check in ClientState.Status proposed) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-ethan-frey-wasm-client-review-pdf.md` | ADVISORY | Confio (Ethan Frey) |

---

## WASM Light-Client (08-wasm) Validation Vulnerabilities [HIGH]

### Overview

The 08-wasm client moves light-client verification *logic* into a governance-approved CosmWasm contract while ibc-go keeps only the storage/interface shell. Two audits define its bug classes. Halborn (Feb 2023): the Go shell forgot consensus-state writes in `UpdateState`, left client status defaulting to Active, skipped signer validation on code pushes, and didn't configure wasmvm execution parameters. Confio's review (Jul 2023) framed the deeper invariant: the contract must write data "to the provable store in the format defined by IBC" and "cannot call into other systems" — i.e., the *interface contract between Go shell and wasm contract* is the security boundary.

#### Agent Quick View

- Root cause statement: "The Go↔wasm client boundary assumes the wasm contract maintains IBC invariants (consensus-state writes, status transitions, no side effects) that the Go shell neither enforces nor verifies — every gap between shell assumptions and contract behavior is a client-desync or governance-bypass primitive."
- Pattern key: `missing_validation | 08_wasm_client | wasm_client_validation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `08-wasm client_state.go/msgs.go, x/wasm approval flow, wasmvm call configuration`
- High-signal code keywords: `update_state`, `VerifyClientMessage`, `check_for_misbehaviour`, `ClientState.Status`, `MsgPushNewWasmCode`, `wasmvm`, `code_hash`
- Typical sink / impact: `client tracks wrong consensus state → invalid proofs accepted/valid proofs rejected; unvetted client code activated; wasm contract resource exhaustion`
- Validation strength: `strong (2 independent reviews: Halborn + Confio)`

#### Contract / Boundary Map

- Entry surface(s): `UpdateClient` (relayer), `MsgPushNewWasmCode` / governance proposal (code approval), `VerifyMembership` calls during packet handling
- Contract hop(s): `ibc-go 02-client keeper → 08-wasm ClientState.UpdateState/VerifyClientMessage → wasmvm → contract (rust)` — three trust transitions in one call
- Trust boundary crossed: `governance-approved wasm blob executes with light-client authority`; `relayer-chosen client messages enter the VM`
- Shared state or sync assumption: `contract writes consensus states through the Go store under IBC-defined keys; status must reflect actual verifiability; one approved code hash per client`

#### Valid Bug Signals

- Signal 1: Shell `UpdateState` calls contract `update_state` but does not guarantee consensus state was persisted at the returned height (HAL-01)
- Signal 2: `ClientState.Status` returns `Active` without consulting contract/expiry (HAL-03) — expired or misbehaving clients stay Active
- Signal 3: `MsgPushNewWasmCode.ValidateBasic()` skips signer validity (HAL-04) — combined with permission assumptions = unvetted code push
- Signal 4: wasmvm invocation omits gas/memory limits (HAL-02) — contract can consume unbounded node resources
- Signal 5: Height/time arithmetic on client state without conditional checks (HAL-09); missing channel field validation on handshake msgs (HAL-08)

#### False Positive Guards

- Not this bug when: consensus-state writes are verified in the same transaction (read-after-write check) and status logic delegates to the contract
- Safe if: new code hashes require governance vote AND old clients pinned to old hashes (no silent migration)
- Requires attacker control of: relayer messages (for state confusion), a governance proposal (for malicious code), or counterparty chain (for misbehaviour)

### Vulnerable Pattern Examples

**Example 1: Consensus state never written by UpdateState** [MEDIUM]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md`
```go
// modules/light-clients/08-wasm/client_state.go (HAL-01)
func (c ClientState) UpdateState(ctx sdk.Context, cdc codec.BinaryCodec,
    clientStore sdk.KVStore, clientMsg exported.ClientMessage) []exported.Height {
    const VerifyClientMessage = "update_state"
    // ...calls into wasm contract; consensus state was not properly set,
    // "which can lead to inconsistencies ... forked chains, where different
    // nodes have different views of the network's state"
}
```

**Example 2: Client status defaults Active + unvalidated code push** [LOW ×2, chainable]
> 📖 Reference: same report (HAL-03, HAL-04) — status marked Active regardless of contract health; `MsgPushNewWasmCode{}.ValidateBasic()` did not validate the signer, weakening the governance-approval requirement ("New wasm client types must be approved by governance vote before clients can be made" — Confio requirements doc).

**Example 3: Interface-contract gaps (Confio)** [ADVISORY]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-ethan-frey-wasm-client-review-pdf.md` — requirements: "No DoS Attack vectors (for any wasm code)", "Client contracts ... cannot call into other systems or effect changes beyond the IBC state under their management"; review recommends adding equivalent checks in `ClientState.Status` (line ~729 discussion).

### Secure Implementation

```go
// ✅ SECURE: shell verifies contract fulfilled the IBC interface contract
func (c ClientState) UpdateState(ctx sdk.Context, cdc codec.BinaryCodec,
    clientStore sdk.KVStore, clientMsg exported.ClientMessage) []exported.Height {
    res := callContract(ctx, c.CodeHash, "update_state", payload,
        wasmvm.WithGasLimit(c.MaxGasLimit))            // HAL-02: bound VM resources
    for _, h := range res.Heights {
        cs, ok := readConsensusState(clientStore, cdc, h)
        if !ok { panicMarkClient(clientStore) }         // HAL-01: read-after-write verify
    }
    return res.Heights
}

func (c ClientState) Status(ctx, clientStore, ...) exported.Status {
    // HAL-03: delegate to contract; if contract errors or trusting period
    // expired => Expired/Frozen, never default-Active
}

func (m MsgPushNewWasmCode) ValidateBasic() error {
    if _, err := sdk.AccAddressFromBech32(m.Signer); err != nil { // HAL-04
        return errorsmod.Wrap(sdkerrors.ErrInvalidAddress, "signer")
    }
    ...
}
```

### Impact Analysis

- **Frequency**: 12 findings (Halborn) + architecture review (Confio)
- **Severity Distribution**: MEDIUM: 2, LOW: 5+ (HAL-05..09), ADVISORY: 1 report
- **Affected Protocols**: ibc-go 08-wasm; chains exposing arbitrary-wasm-client creation; wasmd-based app-chains
- **Validation Strength**: Strong (Halborn code audit + Confio architect review)

**Cross-references**: `ibc/ibc-v2-eureka-client-status.md` (status gating symmetry), `evm/precompile-state-vulnerabilities.md` (VM boundary patterns), `dos/gas-resource-exhaustion.md`.
