---
protocol: generic
chain: cosmos
category: infrastructure
vulnerability_type: security_infrastructure_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: infrastructure_logic

primitives:
  - ssrf
  - private_key
  - tss
  - keyring
  - error_handling
  - deprecated_usage
  - logging_info_leak
  - config_exposure
  - api_abuse

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - infrastructure
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | infrastructure_logic | security_infrastructure_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - GetSigners
  - accounting
  - api_abuse
  - config_exposure
  - deposit
  - deprecated_usage
  - error_handling
  - keyring
  - logging_info_leak
  - mint
  - private_key
  - ssrf
  - tss
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Infra Ssrf
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Risk of server-side request forgery attacks | `reports/cosmos_cometbft_findings/risk-of-server-side-request-forgery-attacks.md` | MEDIUM | TrailOfBits |
| The db backup endpoint may be triggered via SSRF or when vis | `reports/cosmos_cometbft_findings/the-db-backup-endpoint-may-be-triggered-via-ssrf-or-when-visiting-an-attacker-we.md` | MEDIUM | TrailOfBits |

### Infra Private Key
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Peggo takes an Ethereum private key as a command-line argume | `reports/cosmos_cometbft_findings/peggo-takes-an-ethereum-private-key-as-a-command-line-argument.md` | MEDIUM | TrailOfBits |

### Infra Tss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Elected TSS Nodes Can Act Without Any Deposit | `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md` | HIGH | SigmaPrime |
| Lack Of Slashing/Penalty Mechanism | `reports/cosmos_cometbft_findings/lack-of-slashingpenalty-mechanism.md` | HIGH | Halborn |
| TSS Manager Is A Single Point Of Failure | `reports/cosmos_cometbft_findings/tss-manager-is-a-single-point-of-failure.md` | MEDIUM | SigmaPrime |
| TSS Nodes Reporting Slashing Are Vulnerable To Front Running | `reports/cosmos_cometbft_findings/tss-nodes-reporting-slashing-are-vulnerable-to-front-running.md` | MEDIUM | SigmaPrime |

### Infra Keyring
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Insecure storage of price-feeder keyring passwords | `reports/cosmos_cometbft_findings/insecure-storage-of-price-feeder-keyring-passwords.md` | MEDIUM | TrailOfBits |
| Peggo allows the use of non-local unencrypted URL schemes | `reports/cosmos_cometbft_findings/peggo-allows-the-use-of-non-local-unencrypted-url-schemes.md` | MEDIUM | TrailOfBits |

### Infra Error Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RemoveStakes and RemoveDelegateStakes silently handle errors | `reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md` | HIGH | Sherlock |
| Unhandled error in emergency clawback execution may prevent  | `reports/cosmos_cometbft_findings/unhandled-error-in-emergency-clawback-execution-may-prevent-accounting-lost-fund.md` | MEDIUM | Spearbit |
| Unhandled Stake Recovery Failure Leads to Potential Accounti | `reports/cosmos_cometbft_findings/unhandled-stake-recovery-failure-leads-to-potential-accounting-inconsistencies.md` | MEDIUM | Quantstamp |

### Infra Deprecated Usage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deprecated GetSigners Usage | `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md` | HIGH | OtterSec |

---

# Security Infrastructure Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Security Infrastructure Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Infra Ssrf](#1-infra-ssrf)
2. [Infra Private Key](#2-infra-private-key)
3. [Infra Tss](#3-infra-tss)
4. [Infra Keyring](#4-infra-keyring)
5. [Infra Error Handling](#5-infra-error-handling)
6. [Infra Deprecated Usage](#6-infra-deprecated-usage)

---

## 1. Infra Ssrf

### Overview

Implementation flaw in infra ssrf logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This bug report is about the price-feeder module which sends HTTP requests to configured providers' APIs. If any of the HTTP responses is a redirect response, the module will automatically issue a new request to the address provided in the response's header. This could be exploited by an attacker to



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | infrastructure_logic | security_infrastructure_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `infrastructure_logic`
- High-signal code keywords: `GetSigners`, `accounting`, `api_abuse`, `config_exposure`, `deposit`, `deprecated_usage`, `error_handling`, `keyring`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in infra ssrf logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra ssrf in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: Risk of server-side request forgery attacks** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/risk-of-server-side-request-forgery-attacks.md`
```go
HTTP/1.1 301 Moved Permanently
Location: http://localhost:26657/remove_tx?txKey=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Example 2: The db backup endpoint may be triggered via SSRF or when visiting an attacker we** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/the-db-backup-endpoint-may-be-triggered-via-ssrf-or-when-visiting-an-attacker-we.md`
```
// Vulnerable pattern from Prysm:
## Diﬃculty: High
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra ssrf logic allows exploitation through missing validation, incorrect st
func secureInfraSsrf(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Prysm, Umee
- **Validation Strength**: Single auditor

---

## 2. Infra Private Key

### Overview

Implementation flaw in infra private key logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about an issue with Peggo's command line, which could allow an attacker to gain access to a user's Ethereum private key if they gain access to a user account on a system running Peggo. This could potentially allow the attacker to steal funds from the Ethereum account. The problem 

### Vulnerability Description

#### Root Cause

Implementation flaw in infra private key logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra private key in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: Peggo takes an Ethereum private key as a command-line argument** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/peggo-takes-an-ethereum-private-key-as-a-command-line-argument.md`
```
// Vulnerable pattern from Umee:
## Diﬃculty: High
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra private key logic allows exploitation through missing validation, incor
func secureInfraPrivateKey(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Umee
- **Validation Strength**: Single auditor

---

## 3. Infra Tss

### Overview

Implementation flaw in infra tss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: This bug report is about a potential security issue in the TSS node system. The issue is that a node can remove its insurance deposit and still be elected as a TSS node. As a result, there is no means of punishing the node for inactivity or malicious behaviour. This is possible because election resu

### Vulnerability Description

#### Root Cause

Implementation flaw in infra tss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra tss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: Elected TSS Nodes Can Act Without Any Deposit** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md`
```
// Vulnerable pattern from Mantle Network:
## Description

A node can remove its insurance deposit and still be elected as an active TSS node. TSS nodes are voted for by the BITDAO, which then pushes the currently elected nodes on-chain. Nodes that wish to be voted for must provide a deposit as insurance that they will perform their role honestly if elected. By timing a withdrawal correctly, a node can remove their deposit and still be elected as an active TSS node. As a result, there is no means of punishing the node for inactivity or m
```

**Example 2: Lack Of Slashing/Penalty Mechanism** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-slashingpenalty-mechanism.md`
```go
While we currently do not have a technical slashing mechanism in place, our network operates within a permissioned environment with carefully vetted validators. Any malicious activity would be addressed through the enforcement of our contractual agreements, ensuring the immediate removal of any offending validators. This contractual framework provides a strong layer of security, maintaining the integrity and trustworthiness of the consortium.
```

**Example 3: TSS Manager Is A Single Point Of Failure** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/tss-manager-is-a-single-point-of-failure.md`
```
// Vulnerable pattern from Mantle Network:
## Description

The TSS manager represents a centralised point of failure within the system as it is responsible for coordinating and facilitating communication among TSS nodes. The threshold signature scheme (TSS) relies on a TSS manager role to coordinate TSS nodes for signing messages to verify transaction batches produced by the sequencer and slash inactive or malicious TSS nodes. Without the TSS manager, state roots cannot be transitioned from Mantle L2 to be recorded on Ethereum L1.

Furth
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra tss logic allows exploitation through missing validation, incorrect sta
func secureInfraTss(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: Mantle Network, Consortium
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Infra Keyring

### Overview

Implementation flaw in infra keyring logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: A bug has been identified in the price-feeder, a data validation target, which has a high difficulty level. The bug is that the price-feeder stores keyring passwords in plaintext and does not provide a warning if the configuration file has overly broad permissions. Furthermore, neither the README no

### Vulnerability Description

#### Root Cause

Implementation flaw in infra keyring logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra keyring in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: Insecure storage of price-feeder keyring passwords** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insecure-storage-of-price-feeder-keyring-passwords.md`
```go
**Figure 25.1:** The `price-feeder` does not warn the user if the configuration file used to store the keyring password in plaintext has overly broad permissions.

### Trail of Bits

#### UMEE Security Assessment
**PUBLIC**
```

**Example 2: Peggo allows the use of non-local unencrypted URL schemes** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/peggo-allows-the-use-of-non-local-unencrypted-url-schemes.md`
```go
$ peggo orchestrator {gravityAddress}  \
--eth-pk=  $ETH_PK  \
--eth-rpc=  $ETH_RPC  \
--relay-batches=  true  \
--relay-valsets=  true  \
--cosmos-chain-id=...  \
--cosmos-grpc=  "tcp://..."  \
--tendermint-rpc=  "http://..."  \
--cosmos-keyring=...  \
--cosmos-keyring-dir=...  \
--cosmos-from=...
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra keyring logic allows exploitation through missing validation, incorrect
func secureInfraKeyring(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Umee
- **Validation Strength**: Single auditor

---

## 5. Infra Error Handling

### Overview

Implementation flaw in infra error handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: The bug report highlights an issue with the RemoveStakes and RemoveDelegateStakes functions in the Allora network's code. These functions are responsible for removing stakes from users' accounts. The bug allows for errors to occur during the removal process, which can result in an inconsistent state

### Vulnerability Description

#### Root Cause

Implementation flaw in infra error handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra error handling in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: RemoveStakes and RemoveDelegateStakes silently handle errors in EndBlocker** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md`
```go
[RemoveStakes](https://github.com/sherlock-audit/2024-06-allora/blob/main/allora-chain/x/emissions/module/stake_removals.go#L13-L63)
```

**Example 2: Unhandled error in emergency clawback execution may prevent accounting lost fund** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/unhandled-error-in-emergency-clawback-execution-may-prevent-accounting-lost-fund.md`
```
// Vulnerable pattern from Sonic Staking:
## Vulnerability Report
```

**Example 3: Unhandled Stake Recovery Failure Leads to Potential Accounting Inconsistencies** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/unhandled-stake-recovery-failure-leads-to-potential-accounting-inconsistencies.md`
```
// Vulnerable pattern from Hipo Finance:
**Update**
While the client's statements are accurate for the current state of the elector contract, there is potential for the elector contract to be upgraded. This issue is not problematic now, but could be in the future.

![Image 13: Alert icon](https://certificate.quantstamp.com/full/hipo-finance/62651b32-2b58-4ac1-88c4-f06978bf993d/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Marked as "Unresolved" by the client. The client provided the following explanatio
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra error handling logic allows exploitation through missing validation, in
func secureInfraErrorHandling(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Hipo Finance, Sonic Staking, Allora
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Infra Deprecated Usage

### Overview

Implementation flaw in infra deprecated usage logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The bug report discusses an issue with the GetSigners() method in the MsgSubmitConsumerMisbehaviour and MsgSubmitConsumerDoubleVoting messages. This method is no longer supported and is incompatible with newer versions of the Cosmos SDK. The problem arises because the Cosmos SDK has evolved and now 

### Vulnerability Description

#### Root Cause

Implementation flaw in infra deprecated usage logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies infra deprecated usage in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to infra operations

### Vulnerable Pattern Examples

**Example 1: Deprecated GetSigners Usage** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md`
```go
// File: ethos-chain/x/ccv/provider/types/msg.go
func (msg MsgSubmitConsumerMisbehaviour) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}

func (msg MsgSubmitConsumerDoubleVoting) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in infra deprecated usage logic allows exploitation through missing validation, 
func secureInfraDeprecatedUsage(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Ethos Cosmos
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Infra Ssrf
grep -rn 'infra|ssrf' --include='*.go' --include='*.sol'
# Infra Private Key
grep -rn 'infra|private|key' --include='*.go' --include='*.sol'
# Infra Tss
grep -rn 'infra|tss' --include='*.go' --include='*.sol'
# Infra Keyring
grep -rn 'infra|keyring' --include='*.go' --include='*.sol'
# Infra Error Handling
grep -rn 'infra|error|handling' --include='*.go' --include='*.sol'
# Infra Deprecated Usage
grep -rn 'infra|deprecated|usage' --include='*.go' --include='*.sol'
```

## Keywords

`abuse`, `accounting`, `after`, `allows`, `api`, `appchain`, `argument`, `attacker`, `attacks`, `backup`, `cause`, `clawback`, `config`, `cosmos`, `deposit`, `deprecated`, `elected`, `emergency`, `endblocker`, `endpoint`, `error`, `errors`, `ethereum`, `execution`, `exposure`, `failure`, `forgery`, `funds`, `getsigners`, `handle`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`GetSigners`, `accounting`, `api_abuse`, `appchain`, `config_exposure`, `cosmos`, `defi`, `deposit`, `deprecated_usage`, `error_handling`, `infrastructure`, `keyring`, `logging_info_leak`, `mint`, `private_key`, `security_infrastructure_vulnerabilities`, `ssrf`, `staking`, `tss`
