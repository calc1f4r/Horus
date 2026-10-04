---
protocol: generic
chain: cosmos
category: ibc
vulnerability_type: channel_upgrade_validation

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_validation | ibc_channel_upgrade | channel_upgrade_validation

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - ChannelUpgradeKeeper
  - ConnectionKeeper
  - HandshakeKeeper
  - GovModule (authority)
path_keys:
  - missing_validation | ChanUpgradeTry | ConnectionHops[0] | index_oob
  - missing_state_check | upgrade_timeout | FLUSHING→FLUSHCOMPLETE | stuck_channel
  - missing_authority_check | ChanUpgradeConfirm | governance bypass | unauthorized_upgrade

# Attack Vector Details
attack_type: logical_error|dos
affected_component: ibc_channel_upgrade|channel_handshake

# Technical Primitives
primitives:
  - channel_upgrade_handshake
  - connection_hops_validation
  - upgrade_timeout
  - flushing_state
  - validate_basic_ordering
  - governance_authority

# Grep / Hunt-Card Seeds
code_keywords:
  - ChanUpgradeInit
  - ChanUpgradeTry
  - ChanUpgradeAck
  - ChanUpgradeConfirm
  - ChanUpgradeOpen
  - ChanUpgradeTimeout
  - ConnectionHops
  - UpgradeFields
  - STATE_FLUSHING
  - STATE_FLUSHCOMPLETE
  - WriteUpgradeTimeoutChannel
  - MustVerifyUpgradeChannel
  - RestoreChannel

# Impact Classification
severity: medium
impact: dos|state_corruption|channel_bricking
exploitability: 0.5
financial_impact: medium

# Context Tags
tags:
  - cosmos
  - appchain
  - ibc
  - channel-upgrade
  - ibc-go
  - handshake
  - dos

language: go
version: ibc-go v7.3+ (channel upgades feature)

---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Channel Upgrade ValidateBasic Ordering
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Possible Out-of-Bounds Slice Access (ConnectionHops[0] accessed before length validation in ChanUpgradeTry) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-04-channel-upgrades-atredis-partners-interchain-foundation-ibc-go-channel-upgrade-feature-assessment-report-v1-1-pdf.md` | INFO | Atredis Partners |
| RPC Communication over Plaintext HTTP (Hermes relayer default for channel-upgrade e2e) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-04-channel-upgrades-atredis-partners-interchain-foundation-ibc-go-channel-upgrade-feature-assessment-report-v1-1-pdf.md` | INFO | Atredis Partners |
| Deprecated Protobuf Package in Use | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-04-channel-upgrades-atredis-partners-interchain-foundation-ibc-go-channel-upgrade-feature-assessment-report-v1-1-pdf.md` | INFO | Atredis Partners |

---

## Channel Upgrade Validation Vulnerabilities [MEDIUM]

### Overview

The IBC channel-upgrade handshake (IBC-Go `04-channel` upgrades, introduced ~v7.3/v8) lets an authority (governance) mutate live channel parameters — order, connection hops, version — through an INIT/TRY/ACK/CONFIRM/OPEN dance while the channel passes through `STATE_FLUSHING` / `STATE_FLUSHCOMPLETE`. Because the upgrade path mutates an already-live channel rather than a fresh one, every invariant that the original handshake enforced at OPEN time (connection exists and is OPEN, hops non-empty, counterparty unchanged, timeout counters) must be *re-enforced* on the upgrade path. Audits of this feature (Atredis Partners assessment for Interchain Foundation) show the classic failure mode: unvalidated slice/index access (`ConnectionHops[0]`) whose safety silently depends on `ValidateBasic()` having run earlier in the message lifecycle.

#### Agent Quick View

- Root cause statement: "Channel upgrade handlers index and dereference upgrade fields (ConnectionHops, UpgradeFields) whose validity is only guaranteed if ValidateBasic() ran earlier in a different code path — any new entry point that skips it turns an Info-level index access into a panic/DoS on a live channel."
- Pattern key: `missing_validation | ibc_channel_upgrade | channel_upgrade_validation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `04-channel keeper upgrade.go, connection keeper, gov authority`
- High-signal code keywords: `ChanUpgradeTry`, `ConnectionHops[0]`, `STATE_FLUSHING`, `UpgradeFields`, `ChanUpgradeTimeout`
- Typical sink / impact: `node panic / stuck channel in FLUSHING / governance-bricked channel`
- Validation strength: `moderate (1 dedicated third-party assessment + continued Informal review)`

#### Contract / Boundary Map

- Entry surface(s): `MsgChannelUpgradeInit` (authority-gated), `MsgChannelUpgradeTry` (relayer, anyone), `MsgChannelUpgradeAck`, `MsgChannelUpgradeConfirm`, `MsgChannelUpgradeTimeout`
- Contract hop(s): `msg_server → keeper.ChanUpgradeTry → connectionKeeper.GetConnection(channel.ConnectionHops[0])` — hop validity assumed from ValidateBasic, not re-checked
- Trust boundary crossed: `relayer-submitted message (untrusted) → state-mutating upgrade handler (trusted)`; `timeout path can restore channel from FLUSHING`
- Shared state or sync assumption: `counterparty chain executes matching upgrade steps; timeout must correctly roll back to pre-upgrade channel state`

#### Valid Bug Signals

- Signal 1: `channel.ConnectionHops[0]` (or any `[0]`/`[1]` index into upgrade fields) dereferenced before a length check *in the same function*
- Signal 2: Upgrade handler reads connection/channel state without verifying the connection is in `OPEN` state (cf. classic `channelOpenAck` flaw)
- Signal 3: `ChanUpgradeTimeout` / restore path writes channel state without verifying the counterparty actually failed (griefing vector to revert a legit upgrade)
- Signal 4: `UpgradeFields.ProposalHeight` / timeout timestamps compared with `ctx.BlockTime()` using wrong units (nanoseconds vs seconds)
- Signal 5: Capability check (`ScopedKeeper.AuthenticateCapability`) missing on any of the 5 upgrade msgs

#### False Positive Guards

- Not this bug when: `ValidateBasic()` provably runs on every path to the dereference (baseapp routing guarantees) AND the field is immutable between validation and use
- Safe if: length checks are inline (`if len(channel.ConnectionHops) == 0 { return err }`) rather than assumed
- Requires attacker control of: a relayer account (TRY/ACK/CONFIRM are permissionless) or governance majority (INIT)
- Note: the Atredis assessment found NO high/critical issues — the feature was assessed as reasonably hardened; treat this entry as a *hunt card for forks/middleware that re-implement upgrade handlers*, not as evidence of a live ibc-go bug.

### Vulnerable Pattern Examples

**Example 1: Unvalidated ConnectionHops index access in upgrade path** [INFO — latent]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-04-channel-upgrades-atredis-partners-interchain-foundation-ibc-go-channel-upgrade-feature-assessment-report-v1-1-pdf.md`
```go
// modules/core/04-channel/keeper/upgrade.go:96
// Direct index [0] access; safety depends on ValidateBasic having run earlier
connection, found := k.connectionKeeper.GetConnection(ctx, channel.ConnectionHops[0])
```
Atredis: "an array element is directly accessed without validating the length first... Atredis was unable to identify an exploit path during testing" because `ValidateBasic()` (which enforces `len(ConnectionHops) == 1` for UNORDERED/ORDERED upgrade msgs) runs first. The bug class matters for any fork/middleware that adds a new entry into the upgrade keeper.

**Example 2: Plaintext RPC for upgrade relaying (operational)**
> 📖 Reference: same report — Hermes default setup exposes plaintext HTTP/WS RPCs; a local MITM can read/alter channel-upgrade relay traffic.

### Secure Implementation

```go
// ✅ SECURE: re-validate at point of use in every upgrade handler
func (k Keeper) ChanUpgradeTry(ctx sdk.Context, ...) error {
    if len(channel.ConnectionHops) == 0 {          // inline guard, don't trust caller
        return channeltypes.ErrInvalidChannel
    }
    conn, found := k.connectionKeeper.GetConnection(ctx, channel.ConnectionHops[0])
    if !found || conn.State != connectiontypes.OPEN { // re-check state, not just existence
        return connectiontypes.ErrInvalidConnection
    }
    // verify counterparty via connection end as in the canonical handshake
    // authenticate capability for the msg sender
    // on timeout: only restore after verifying counterparty proof of failure
}
```

### Impact Analysis

- **Frequency**: 1 dedicated assessment (3 Info findings); feature also covered by ongoing ibc-go review cycle
- **Severity Distribution**: INFO: 3 (in core; forks may escalate)
- **Affected Protocols**: ibc-go channel upgades, Hermes relayer ops; any app-chain forking the upgrade keeper
- **Validation Strength**: Single specialized auditor (Atredis) with vendor engagement

**Cross-references**: `ibc/ibc-protocol-vulnerabilities.md` (handshake state checks), `lifecycle/upgrade-migration-vulnerabilities.md` (state migration invariants).
