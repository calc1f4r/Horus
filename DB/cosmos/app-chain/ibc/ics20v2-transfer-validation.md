---
protocol: generic
chain: cosmos
category: ibc
vulnerability_type: ics20v2_transfer_validation

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_validation | ics20_transfer | ics20v2_transfer_validation

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - TransferKeeper (ICS20 v2)
  - IBCMiddleware (packet-forward / hooks)
  - EscrowModule
path_keys:
  - missing_timeout_cap | OnRecvPacket | PFM retry loop | stuck_escrow
  - missing_denom_validation | token trace | denom escaping | invalid_denom
  - missing_memo_validation | forwarding memo | unbounded parse | dos

# Attack Vector Details
attack_type: logical_error|dos
affected_component: ics20_transfer|token_transfer_middleware

# Technical Primitives
primitives:
  - fungible_token_packet
  - denom_trace_validation
  - memo_forwarding
  - escrow_refund
  - timeout_handling
  - multi_denom_coin

# Grep / Hunt-Card Seeds
code_keywords:
  - FungibleTokenPacketData
  - OnRecvPacket
  - OnTimeoutPacket
  - RefundPacketKey
  - ProcessedKey
  - GetDenomPrefix
  - UnbondingDenom
  - forwardTimeoutTimestamp
  - retries
  - Memo
  - receiver
  - sender
  - TokenTransfer
  - denomHash

# Impact Classification
severity: medium
impact: dos|fund_lock|incorrect_escrow
exploitability: 0.5
financial_impact: medium

# Context Tags
tags:
  - cosmos
  - appchain
  - ibc
  - ics20
  - token-transfer
  - packet-forwarding
  - escrow

language: go|rust
version: ibc-go v8/v9 (ICS20 v2), PFM forks

---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### ICS20 v2 Feature Assessment (clean core)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| ICS20 v2 New Features Assessment — zero findings; ValidateBasic/MsgChannelOpenInit test surface documented | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-20-token-transfer-atredis-partners-interchain-ics20-v2-new-features-assessment-report-v1-0-pdf.md` | NONE | Atredis Partners |

### Transfer Middleware Timeout / Refund Validation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| No upper limit to the time-out on PFM packets (255 retries, packet cannot be cancelled) | `reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md` | MEDIUM | Zellic |
| RefundPacketKey function defect (refund accounting) | `reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md` | MEDIUM | Zellic |
| ProcessedKey unset in context → receiveFunds incorrect behavior | `reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md` | INFO | Zellic |

### IBC Transfer App Permissioning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect permissioning of IbcExecuteProposal execution — failed proposal execution + elevated owner privileges | `reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-02-14-audit-report-astroport-ibc-v1-0-pdf.md` | MAJOR | Astrovault (SR) |

---

## ICS20 v2 / Token-Transfer Validation Vulnerabilities [MEDIUM]

### Overview

ICS20 v2 (multi-denom `Coin[]` packets, simplified denom traces, forwarding-native memo) is the value-moving core of Cosmos IBC. The reference implementation passed a dedicated Atredis assessment with **zero findings**, which makes the *delta* introduced by chains the real risk surface: middleware stacked on transfer (packet-forward, hooks, custom refunds) that re-parses `FungibleTokenPacketData`, relaxes timeout handling, or mismanages escrow/refund keys. Zellic's audit of the packet-forward middleware found exactly this class: unbounded effective packet lifetime (no upper limit on timeout × 255 retries) and refund-key handling defects.

#### Agent Quick View

- Root cause statement: "Transfer-adjacent middleware re-implements ICS20 packet validation (memo parse, timeout bounds, refund/processed keys) without the core's invariant checks — untrusted packet fields flow into escrow accounting and retry loops."
- Pattern key: `missing_validation | ics20_transfer | ics20v2_transfer_validation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `transfer module OnRecvPacket/OnTimeoutPacket, PFM middleware, escrow keeper`
- High-signal code keywords: `OnRecvPacket`, `RefundPacketKey`, `ProcessedKey`, `forwardTimeoutTimestamp`, `retries`, `FungibleTokenPacketData`, `denomHash`
- Typical sink / impact: `stuck escrow / unbounded packet lifetime / refund to wrong party / DoS on recv`
- Validation strength: `strong for core (clean dedicated audit), moderate for middleware`

#### Contract / Boundary Map

- Entry surface(s): `OnRecvPacket(packet)` — fully attacker-controlled `data` JSON (sender/receiver/memo/tokens), `OnTimeoutPacket`, `OnAcknowledgementPacket`
- Contract hop(s): `transfer keeper → middleware stack (PFM/hooks) → escrow/bank`; memo fields recurse into *new* packets (forwarding) — validation must survive recursion
- Trust boundary crossed: `counterparty chain JSON → local state mutation`; `relayer-chosen delivery timing (timeout windows)`
- Shared state or sync assumption: `escrow balance ≥ in-flight packets; refund path is the only recovery for failed sends`

#### Valid Bug Signals

- Signal 1: `OnTimeoutPacket`/refund path writes refunds without checking `RefundPacketKey`/`ProcessedKey` correctness (double refund or lost refund)
- Signal 2: Timeout validation checks only `timeoutTimestamp > now` (lower bound) with **no upper bound**, combined with a retry mechanism → packet effectively immortal, escrow locked
- Signal 3: Denom prefix/trace parsing accepts empty or oversized components (v1 traces) — v2 `denomHash` bypass
- Signal 4: Memo (`string`) parsed without size cap before JSON unmarshal → unbounded gas/memory per packet
- Signal 5: Middleware processes packet before checking it owns the channel/version → processes foreign packets (see ibc-protocol-vulnerabilities M-14 class)

#### False Positive Guards

- Not this bug when: core ibc-go v8/v9 transfer keeper is used unmodified (dedicated audit clean — cite Atredis as evidence of hardening, not as an unfixed issue)
- Safe if: timeout upper-bounded by a protocol constant AND retries bounded AND escrow reclaim possible after final timeout
- Requires attacker control of: packet `data` fields (any counterparty user) or relayer timing

### Vulnerable Pattern Examples

**Example 1: Unbounded packet lifetime in packet-forward middleware** [MEDIUM]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md`
```
// OnRecvPacket() checks the time-out on the packet cannot be negative,
// however there is not an upper limit set on the time-out.
// Since there is no way to cancel a packet once it is sent, and because the
// maximum amount of retries possible is 255, it is possible for a packet to
// get stuck in a time-out for an extremely long time.
```

**Example 2: Refund key accounting defect** [MEDIUM]
> 📖 Reference: same Zellic PFM report — `RefundPacketKey` function defect (medium, coding mistake) breaks refund routing; `ProcessedKey` unset in context makes `receiveFunds` misbehave (informational companion).

**Example 3: Transfer-app proposal permissioning (CosmWasm variant)** [MAJOR]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-02-14-audit-report-astroport-ibc-v1-0-pdf.md`
"Incorrect permissioning of IbcExecuteProposal execution leads to failure of proposal execution and elevated owner privileges" — governance-proposal execution path on the IBC transfer app mis-permissioned.

### Secure Implementation

```go
// ✅ SECURE: bounded forwarding with explicit refund accounting
func (im IBCMiddleware) OnRecvPacket(ctx sdk.Context, packet ibcexported.PacketI) ibcexported.Acknowledgement {
    var data transfertypes.FungibleTokenPacketData
    if err := json.Unmarshal(packet.GetData(), &data); err != nil || len(data.Memo) > MaxMemoLen {
        return channeltypes.NewErrorAcknowledgement(err)   // cap memo before parse
    }
    if !im.implementsForwarding(data.Memo) {              // ownership check first
        return im.app.OnRecvPacket(ctx, packet)
    }
    fwd := parseForwardMemo(data.Memo)                     // strict schema
    if fwd.Timeout > ctx.BlockTime().Add(MaxForwardTimeout).UnixNano() {
        return channeltypes.NewErrorAcknowledgement(errors.New("timeout exceeds max")) // upper bound
    }
    if fwd.Retries > MaxRetries { fwd.Retries = MaxRetries }
    // refund: write RefundPacketKey + set ProcessedKey in same cacheCtx commit
}
```

### Impact Analysis

- **Frequency**: core v2 feature audit clean; middleware audits (PFM) 2 Medium + 1 Info; CosmWasm transfer apps 1 Major
- **Severity Distribution**: MAJOR: 1, MEDIUM: 2, INFO: 1, NONE (core): 1 report
- **Affected Protocols**: ibc-go ICS20 v2 (clean), packet-forward-middleware forks, CosmWasm IBC transfer apps
- **Validation Strength**: Strong (2 independent firms across core + middleware)

**Cross-references**: `ibc/ibc-protocol-vulnerabilities.md` (middleware bypass), `ibc/ibc-v2-eureka-client-status.md` (stuck-fund refund failure on frozen clients), `fund-safety/fund-locking-insolvency.md`.
