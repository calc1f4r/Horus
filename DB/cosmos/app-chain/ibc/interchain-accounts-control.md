---
protocol: generic
chain: cosmos
category: ibc
vulnerability_type: interchain_accounts_control

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_validation | ica_host_controller | interchain_accounts_control

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - ICAControllerKeeper
  - ICAHostKeeper
  - MsgServer (core keeper executeTx)
  - InterchainAccount (module account on host)
path_keys:
  - regex_bypass | IsClientIDFormat | newline injection | malformed identifiers
  - all_or_nothing_execution | executeTx | cacheCtx writeCache | packet frontrun cancel
  - legacy_amino_deserialize | untrusted tx | panic crash | host DoS
  - ordering_metadata | interchain account address derivation | wrong account control

# Attack Vector Details
attack_type: logical_error|dos
affected_component: ica_host|ica_controller|packet_execution

# Technical Primitives
primitives:
  - interchain_account_registration
  - controller_packet_creation
  - host_execute_tx
  - validate_basic_regex
  - amino_codec_deserialization
  - atomic_message_batches

# Grep / Hunt-Card Seeds
code_keywords:
  - RegisterInterchainAccount
  - executeTx
  - writeCache
  - IsClientIDFormat
  - IsRevisionFormat
  - IsValidAddr
  - OnChanOpenTry
  - GetInterchainAccountAddress
  - interpolateAccountAddress
  - MsgSendTx
  - PacketData
  - amino
  - targetClient
  - validateEnabled

# Impact Classification
severity: high
impact: dos|state_corruption|potential_fund_loss
exploitability: 0.6
financial_impact: medium

# Context Tags
tags:
  - cosmos
  - appchain
  - ibc
  - ica
  - interchain-accounts
  - host-module
  - regex
  - amino

language: go
version: ibc-go 27-interchain-accounts (ToB audit target)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### Trail of Bits ICA Audit (primary)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| TOB-IBCICA-5: Deserializing untrusted cosmos transactions with the legacy amino codec can crash the application (DoS) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | HIGH | Trail of Bits |
| TOB-IBCICA-2: Revision and client identifier regexes accept newlines (`[^-]` should be `[^\n-]`) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | UNDETERMINED | Trail of Bits |
| TOB-IBCICA-3: IsValidAddr regex accepts 0-length and excessively long addresses | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | UNDETERMINED | Trail of Bits |
| TOB-IBCICA-4: Invalid ConsensusStateWithHeight.ConsensusState struct tag could cause [deserialization issues] | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | UNDETERMINED | Trail of Bits |
| TOB-IBCICA-7: If the host fails a single message, none of the messages in the packet are committed (frontrun-cancel griefing) | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | UNDETERMINED | Trail of Bits |
| TOB-IBCICA-6: Incorrectly formatted error string in OnChanOpenTry | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | INFO | Trail of Bits |
| TOB-IBCICA-1: Outdated and vulnerable dependencies | `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md` | LOW | Trail of Bits |

### ICA-Adjacent Audit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Stride stakeibc ICA callbacks audit | `reports/cosmos-l1-nodes_findings/audits-stride-2022-11-30-audit-report-stride-stakeibc-icacallbacks-pdf.md` | multi | Informal Systems |
| Stride ICA oracle | `reports/cosmos-l1-nodes_findings/audit-reports-stride-2023-08-20-audit-report-stride-ica-oracle-v1-0-pdf.md` | multi | (Astrovault/SR-class) |

---

## Interchain Accounts Host/Controller Control Vulnerabilities [HIGH]

### Overview

ICA lets a controller chain own an account on a host chain; packets carry arbitrary `sdk.Msg` batches executed by the host module account. The Trail of Bits audit of `27-interchain-accounts` (1 High, 1 Low, 3 Info, 4 Undetermined) maps the control-plane bug classes: untrusted packet data reaching permissive parsers (amino codec → node crash), regex validators accepting newline-injected identifiers, and all-or-nothing batch execution that an attacker can frontrun to cancel a controller's entire message batch.

#### Agent Quick View

- Root cause statement: "ICA hosts deserialize and execute fully counterparty-controlled message batches; validators/parsers in the path (regexes, amino codec, address checks) are the last line of defense, and batch atomicity converts any single injectable failure into cancellation of the whole packet."
- Pattern key: `missing_validation | ica_host_controller | interchain_accounts_control`
- Interaction scope: `multi_contract`
- Primary affected component(s): `host keeper relay.go executeTx, controller msgs, 02-client/24-host validators`
- High-signal code keywords: `executeTx`, `writeCache`, `IsClientIDFormat`, `IsRevisionFormat`, `IsValidAddr`, `amino`, `RegisterInterchainAccount`
- Typical sink / impact: `full-node crash via amino panic / malformed identifiers stored / griefing cancellation of ICA tx batches`
- Validation strength: `strong (dedicated Trail of Bits audit)`

#### Contract / Boundary Map

- Entry surface(s): `OnRecvPacket` on host (relayer-submitted, counterparty-crafted `PacketData` with `msgs [][]byte`), `MsgRegisterInterchainAccount`, `MsgSendTx` on controller
- Contract hop(s): `controller msg_server → packet → host OnRecvPacket → amino/proto unmarshal → executeTx loop over msgs (cacheCtx; writeCache only if all succeed)`
- Trust boundary crossed: `counterparty chain user → host-chain state mutation via module account`; codec boundary (amino legacy paths)
- Shared state or sync assumption: `ICA address derivation (controller portID/connectionID → host account) must be collision-free; batch executes atomically`

#### Valid Bug Signals

- Signal 1: Any `regexp.MustCompile` used for identifiers where char class `[^-]` or `.` permits `\n` (TOB-IBCICA-2 pattern) — inject newlines into chainID/clientID
- Signal 2: Host deserializes packet msgs with legacy amino codec (panic-capable) instead of proto (TOB-IBCICA-5, HIGH)
- Signal 3: Address/identifier validators accept zero-length or unbounded-length inputs (`IsValidAddr`, TOB-IBCICA-3)
- Signal 4: `executeTx` loops msgs in one `cacheCtx` and any `ValidateBasic`/execute failure aborts all (TOB-IBCICA-7) — combined with mempool frontrunning of a deliberately-failing msg = packet cancellation grief
- Signal 5: ICA address interpolation uses unvalidated connection/port identifiers → potential account derivation collision

#### False Positive Guards

- Not this bug when: host only accepts msgs on an allow-list (`HostEnabledParams.AllowMessages`) AND all allow-listed msgs have proto-only codecs
- Safe if: batch failure semantics are intentional (documented atomic batches) and controller retries on ack-failure
- Requires attacker control of: a controller-chain account (to craft packets) or mempool ordering (for TOB-IBCICA-7 frontrun)

### Vulnerable Pattern Examples

**Example 1: Amino deserialization of untrusted transactions crashes node** [HIGH]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-27-interchain-accounts-trail-of-bits-audit-final-report-pdf.md`
"untrusted cosmos transactions, when deserialized [with legacy amino codec], could cause application crashes and denials of service" (TOB-IBCICA-5).

**Example 2: Newline-accepting identifier regexes** [UNDETERMINED]
> 📖 Reference: same report (TOB-IBCICA-2)
```go
// IsRevisionFormat: `^.*[^-]-{1}[1-9][0-9]*$`  — "[^-]" also matches '\n'
// IsClientIDFormat: `^.*[^-]-[0-9]{1,20}$`
// Fix: "[^-]" → "[^\n-]"
var IsClientIDFormat = regexp.MustCompile(`^.*[^-]-[0-9]{1,20}$`).MatchString
```

**Example 3: All-or-nothing batch + frontrun = packet cancellation** [UNDETERMINED]
> 📖 Reference: same report (TOB-IBCICA-7)
```go
func (k Keeper) executeTx(ctx sdk.Context, sourcePort, destPort, destChannel string, msgs []sdk.Msg) error {
    cacheCtx, writeCache := ctx.CacheContext()
    for _, msg := range msgs {
        if err := msg.ValidateBasic(); err != nil { return err }
        if _, err := k.executeMsg(cacheCtx, msg); err != nil { return err }
    }
    writeCache()
    return nil
}
```
"an attacker [could] cancel the execution of all messages sent to the host by front-running the execution of the messages to trigger a failure."

### Secure Implementation

```go
// ✅ SECURE: strict parsers, proto-only codecs, per-msg error aggregation
var IsClientIDFormat = regexp.MustCompile(`^.*[^\n-]-[0-9]{1,20}$`).MatchString // no \n

func (k Keeper) OnRecvPacket(ctx sdk.Context, packet ibcexported.PacketI) ibcexported.Acknowledgement {
    var data icahosttypes.InterchainAccountPacketData
    if err := json.Unmarshal(packet.GetData(), &data); err != nil { /* error ack */ }
    for _, anyMsg := range data.Messages {
        var msg sdk.Msg
        if err := k.cdc.Unmarshal(anyMsg, &msg); err != nil { // proto codec only, never amino
            return icahosttypes.NewErrorAcknowledgement(err)
        }
        if !k.params.Get(isHostEnabled()) || !k.isAllowedMsg(msg) { /* error ack, skip */ }
    }
    // execute atomically but document semantics; ack carries per-msg results
}
```

### Impact Analysis

- **Frequency**: 9 findings in dedicated audit (1H/1L/3I/4 undetermined)
- **Severity Distribution**: HIGH: 1, UNDETERMINED: 4, LOW: 1, INFO: 3
- **Affected Protocols**: ibc-go 27-interchain-accounts; Stride stakeibc/ICA-callback integrations; all chains enabling ICA host
- **Validation Strength**: Strong (Trail of Bits dedicated engagement)

**Cross-references**: `ibc/ibc-protocol-vulnerabilities.md`, `validation/input-validation-vulnerabilities.md` (regex hygiene), `dos/chain-halt-consensus-dos.md` (node crash class).
