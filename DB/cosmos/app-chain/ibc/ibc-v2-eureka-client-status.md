---
protocol: generic
chain: cosmos|ethereum
category: ibc
vulnerability_type: ibc_v2_eureka_client_status

# Pattern Identity
root_cause_family: missing_state_check
pattern_key: missing_state_check | eureka_ics02 | ibc_v2_eureka_client_status

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - ICS26Router (Solidity)
  - ICS20Transfer / ICS20Escrow
  - ILightClient (Ethereum / SP1 zk / Tendermint)
  - ICS02ClientUpgradeable
path_keys:
  - missing_status_check | sendPacket | Frozen client sends | stuck_refund
  - wrong_storage_key | update_consensus_state | slot mismatch | orphaned_consensus_state
  - unbounded_loop | relayMissingPackets | frozen client griefing | relay_dos
  - missing_fork_check | SP1 update | fork version mismatch | invalid_membership

# Attack Vector Details
attack_type: logical_error|dos|fund_lock
affected_component: ibc_v2_router|light_client_interface|escrow

# Technical Primitives
primitives:
  - ics02_client
  - client_status_active_frozen_expired
  - consensus_state_storage_keying
  - membership_notFrozen
  - sp1_zk_update
  - packet_relay_loop

# Grep / Hunt-Card Seeds
code_keywords:
  - GetClientStatus
  - ErrClientNotActive
  - status is
  - update_consensus_state
  - updated_slot
  - ICS26Router
  - recvPacket
  - sendTransfer
  - membership
  - notFrozen
  - relayMissingPackets
  - Misbehaviour
  - handleSP1UpdateClientAndMembership
  - UpdateResult

# Impact Classification
severity: high
impact: fund_loss|fund_lock|dos|state_corruption
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - cosmos
  - ethereum
  - appchain
  - ibc
  - ibc-v2
  - eureka
  - light-client
  - ics02

language: solidity|rust|go
version: IBC-v2 / IBC-Eureka (solidity ibc-eureka 2025-02, SP1 programs)

---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Client Status / Active Checks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Issue M-3: Missing check to ensure client state is active in Solidity sendPacket flow (frozen/expired clients can send; refunds then stuck) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | HIGH-context MEDIUM | Collaborative (Sherlock 2025-02 interchain-labs-ibc-eureka) |
| Issue L-4: Freezing the client will always fail due to [missing precondition] | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | LOW | Collaborative |
| Issue M-6: Frozen clients are constantly relayed to (wasted gas / griefing) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | MEDIUM | Collaborative |

### Consensus State Keying
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Issue H-1: Mismatched slots cause Ethereum light client state to be stored under incorrect keys | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | HIGH | Collaborative |

### Relay / Gas Griefing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Issue M-1: ICS26Router::recvPacket can be DoSed via gas griefing (partial OutOfGas ack) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | MEDIUM | Collaborative |
| Issue L-7: Processing the same amount of packets in a loop can exceed block gas limit | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | LOW | Collaborative |
| Issue M-2: Rate limit for transfer channels can be [circumvented] | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | MEDIUM | Collaborative |

### Fork / ZK Validation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Issue M-7: Light client fork version mismatch during update | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | MEDIUM | Collaborative |
| Issue L-6: Hardcoded to 0 clock_drift in SP1 programs | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md` | LOW | Collaborative |

### Independent Eureka Audit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| IBC Eureka audit (Ethereum-side IBC-v2 stack) | `reports/cosmos-l1-nodes_findings/publications-ibc-eureka-zellic-audit-report-pdf.md` | multi | Zellic |

---

## IBC-v2 / Eureka Client-Status & Router Vulnerabilities [HIGH]

### Overview

IBC-v2 ("Eureka") removes channels and multihop connections: packets flow client-to-client through `ICS26Router` (Solidity) with `ICS02Client` light clients (Ethereum beacon, SP1-zk, Tendermint). The April-2025 collaborative audit (1 High, 7 Medium, 12 Low/Info — all fixed or acknowledged) plus the independent Zellic audit define the canonical bug population for this stack. The recurring root causes: (1) Go-side client-status checks (`GetClientStatus == Active`) that are **missing or inconsistent** in the Solidity mirrors, and (2) light-client storage/keying mismatches between the update path and the read path.

#### Agent Quick View

- Root cause statement: "IBC-v2's Solidity stack re-implements invariants that ibc-go enforces at send time (client must be Active; consensus state keyed by exact slot; membership must reject frozen clients) — each re-implementation that drifts from the Go reference creates a fund-locking or DoS path."
- Pattern key: `missing_state_check | eureka_ics02 | ibc_v2_eureka_client_status`
- Interaction scope: `multi_contract`
- Primary affected component(s): `ICS26Router.sendPacket/recvPacket, ICS02ClientUpgradeable, ICS20Escrow, SP1 update-client program`
- High-signal code keywords: `GetClientStatus`, `ErrClientNotActive`, `update_consensus_state`, `updated_slot`, `notFrozen`, `relayMissingPackets`, `UpdateResult.Misbehaviour`
- Typical sink / impact: `funds sent through frozen client and unrecoverable / consensus states orphaned under wrong keys / selective packet DoS via gas griefing`
- Validation strength: `strong (collaborative multi-firm audit + Zellic, all issues tracked to resolution)`

#### Contract / Boundary Map

- Entry surface(s): `ICS26Router.recvPacket` (permissionless), `sendTransfer` (user), `submitMisbehaviour`/`updateClient` (relayer), SP1 program verify path
- Contract hop(s): `sendTransfer → sendPacket → membership(ILightClient)` — the status check missing in sendPacket but present in membership creates the trap: send succeeds, refund later fails
- Trust boundary crossed: `relayer/any-EOA → router state mutation`; `zk proof → client state update` (SP1); `beacon sync committee → consensus state`
- Shared state or sync assumption: `consensus state write key must equal read key (slot); client status must gate BOTH send and membership paths symmetrically`

#### Valid Bug Signals

- Signal 1: Solidity `sendPacket`/`sendTransfer` flow lacks the Go-side `GetClientStatus(...) != Active → ErrClientNotActive` guard
- Signal 2: `update_consensus_state` return value `updated_slot` used as storage key while `ConsensusState` carries a different slot → orphaned consensus states (H-1)
- Signal 3: `recvPacket` wraps app callback in try/catch where inner OutOfGas still writes a success-style acknowledgement → selective packet censorship (M-1)
- Signal 4: Loop relaying packets (`relayMissingPackets` or batch `recvPacket`) has no per-batch gas bound (L-7) and no frozen-client short-circuit (M-6)
- Signal 5: SP1 `handleSP1UpdateClientAndMembership` handles `UpdateResult.Misbehaviour` without freezing downstream or checks fork version (M-7); `clock_drift` hardcoded 0 (L-6)

#### False Positive Guards

- Not this bug when: the exact Go-reference check exists on both send and membership paths and tests cover Frozen/Expired/Unknown statuses on each
- Safe if: escrow refunds don't depend on `membership` succeeding (decouple refund from frozen state) or client unfreeze/recovery path exists
- Note: all 20 issues in the April-2025 report were fixed/acknowledged — this card targets *forks and integrations* of the eureka stack (including custom SP1 programs), not the audited HEAD.

### Vulnerable Pattern Examples

**Example 1: Missing Active-status check on send → stuck refund loop** [M-3]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-ibc-v2-ibc-v2-april-2025-collaborative-audit-report-pdf.md`
```solidity
// Go (ibc-go) sendPacket:
// if status := k.ClientKeeper.GetClientStatus(ctx, sourceClient); status != exported.Active {
//     return 0, "", errorsmod.Wrapf(clienttypes.ErrClientNotActive, ...) }
// Solidity sendPacket: NO equivalent →
// 1) sendTransfer with Frozen client passes sendPacket
// 2) packet fails; refund calls membership() which has `notFrozen` → reverts
// 3) funds stuck: no way to refund
function membership(ILightClientMsgs.MsgMembership calldata msgMembership) public notFrozen ...
```

**Example 2: Slot mismatch orphans consensus state under wrong key** [H-1]
> 📖 Reference: same report, Issue H-1 — "The update_consensus_state function returns an updated_slot value that can be inconsistent with the slot in the returned ConsensusState. When this value is used as a storage key in the CosmWasm contract, it results in consensus states being stored under [the wrong keys]."

**Example 3: Gas-griefing DoS of recvPacket** [M-1]
> 📖 Reference: same report, Issue M-1 — attacker calls `recvPacket` with minimal gas so the inner `onRecvPacket` reverts OutOfGas but the outer call succeeds writing an ack; application never processes the packet; funds returned to sender; selective cross-chain packet censorship (e.g., arbitrage packets).

### Secure Implementation

```solidity
// ✅ SECURE: symmetric status gating + bounded loops
function sendPacket(IICS26RouterMsgs.Packet memory packet_) internal returns (uint32) {
    ILightClientMsgs.ClientStateData memory csd = ics02Client.getClientState(packet_.sourceClient);
    if (csd.status != ILightClientMsgs.Status.Active) revert ClientNotActive(); // mirror Go check
    ...
}
function recvPacketBatch(Msg[] calldata msgs) external {
    uint256 gasLeftStart = gasleft();
    for (uint256 i; i < msgs.length; i++) {
        recvPacket(msgs[i]);
        if (gasleft() < gasLeftStart / 10) revert BatchGasBound(); // L-7 class guard
    }
}
// refund path must not require membership() on a possibly-frozen client:
// escrow release keyed by timeout proof checked against stored packet commitment only
```

### Impact Analysis

- **Frequency**: 1 High + 7 Medium + 12 Low/Info in the collaborative audit; separate Zellic audit of eureka stack
- **Severity Distribution**: HIGH: 1, MEDIUM: 7, LOW/INFO: 12
- **Affected Protocols**: interchain-labs ibc-eureka (ICS26Router/ICS20/SP1), any IBC-v2 fork; CosmWasm eth-light-client gateway
- **Validation Strength**: Strong (multi-firm collaborative + independent second audit)

**Cross-references**: `ibc/ibc-protocol-vulnerabilities.md` (channel-era equivalents), `ibc/wasm-client-validation.md` (CosmWasm client wrappers), `consensus/light-client-detection.md`.
