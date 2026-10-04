---
# Core Classification
protocol: Ethos Network Social Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43742
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/584
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-ethos-network-judging/issues/206

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - shaflow01
  - DigiSafe
  - pkqs90
  - Kyosi
  - PNS
---

## Vulnerability Title

M-3: Corruptible Upgradability Pattern

### Overview


The report is about a bug found in the EthosContracts, specifically the EthosProfile, EthosReview, and other similar contracts. These contracts are supposed to be upgradeable, but the current implementation has multiple issues that can cause problems during upgrading. The root cause of the issue is that these contracts inherit other contracts that are not upgrade-safe. Additionally, the constructor in these contracts does not have initializers disabled, which is a best practice for proxy contracts. This can lead to storage corruption during upgrading. To fix this issue, the report suggests adding gaps in the AccessControl and SignatureControl contracts, using the upgradeable version from OpenZeppelin's library, and disabling initializers in the EthosContracts constructor. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-ethos-network-judging/issues/206 

## Found by 
DigiSafe, Kyosi, PNS, dobrevaleri, pkqs90, shaflow01, x0lohaclohell
### Summary

The EthosContracts (EthosProfile, EthosReview, ...) are UUPSUpgradeable. However, the current implementation has multiple issues regarding upgradability.

### Root Cause

Following is the inheritance chain of the EthosContracts.

```mermaid
graph BT;
    classDef nogap fill:#f96;
    AccessControl:::nogap-->Pausable:::nogap
    AccessControl:::nogap-->AccessControlEnumerable:::nogap
    AccessControl:::nogap-->SignatureControl:::nogap
    EthosProfile:::nogap-->AccessControl:::nogap
    EthosReview:::nogap-->AccessControl:::nogap
    EthosAttestation:::nogap-->AccessControl:::nogap
    EthosDiscussion:::nogap-->AccessControl:::nogap
    EthosVote:::nogap-->AccessControl:::nogap
```

The Ethos contracts are meant to be upgradeable. However, it inherits contracts that are not upgrade-safe.

The `AccessControl` and `SignatureControl` are both contracts written by Ethos team, both contain storage slots but there are no gaps implemented.

Also, AccessControl inherits the non-upgradeable version Pausable and AccessControlEnumerable from Openzeppelin's library, when it should use the upgradeable version from [openzeppelin-contracts-upgradeable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable) lib.

https://docs.openzeppelin.com/contracts/5.x/upgradeable

There is also another issue that in all EthosContract, the constructor does not have initializers disabled for the implementation contract. This is also a best practice for proxy contracts.

```solidity
  constructor() {
    _disableInitializers();
  }
```

- https://github.com/sherlock-audit/2024-10-ethos-network/blob/main/ethos/packages/contracts/contracts/utils/AccessControl.sol#L15
- https://github.com/sherlock-audit/2024-10-ethos-network/blob/main/ethos/packages/contracts/contracts/utils/SignatureControl.sol#L11

### Internal pre-conditions

If admin performs an upgrade and wants to add another storage slot in AccessControl or SignatureControl contract, the storage slot would mess up.

### External pre-conditions

N/A

### Attack Path

N/A

### Impact

Storage of vault contracts might be corrupted during upgrading.

### PoC

N/A

### Mitigation

1. Add gaps in AccessControl, SignatureControl
2. Use library from Openzeppelin-upgradeable instead, e.g. PausableUpgradeable, AccessControlEnumerableUpgradeable.
3. Disable initializers in EthosContracts constructor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Ethos Network Social Contracts |
| Report Date | N/A |
| Finders | shaflow01, DigiSafe, pkqs90, Kyosi, PNS, x0lohaclohell, dobrevaleri |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-ethos-network-judging/issues/206
- **Contest**: https://app.sherlock.xyz/audits/contests/584

### Keywords for Search

`vulnerability`

