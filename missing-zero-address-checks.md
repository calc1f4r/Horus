---
# Core Classification
protocol: Across Protocol OFT Integration Differential Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58428
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Missing Zero-Address Checks

### Overview

See description below for full details.

### Original Finding Content

When operations with address parameters are performed, it is crucial to ensure the address is not set to zero. Setting an address to zero is problematic because it has special burn/renounce semantics. This action should be handled by a separate function to prevent accidental loss of access during value or ownership transfers.

Throughout the codebase, there are multiple instances where operations are missing a zero address check:

* The [`_setMessenger(messengerType, dstDomainId, srcChainToken, srcChainMessenger)`](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/AdapterStore.sol#L34) operation within the contract `AdapterStore` in `AdapterStore.sol`.
* The [`_setMessenger(messengerTypes[i], dstDomainIds[i], srcChainTokens[i], srcChainMessengers[i])`](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/AdapterStore.sol#L52) operation within the contract `AdapterStore` in `AdapterStore.sol`.
* The [`_adapterStore`](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapterWithStore.sol#L17) operation within the contract `OFTTransportAdapterWithStore` in `OFTTransportAdapterWithStore.sol`.
* The [`_setOftMessenger(token, messenger)`](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/SpokePool.sol#L363) operation within the contract `SpokePool` in `SpokePool.sol`.

Consider adding a zero address check before assigning a state variable.

***Update:** Acknowledged, not resolved. The team stated:*

> *After internal discussion, we think that zero-address checks here are a bit of overkill because all the functions mentioned are only callable by admin (except for `_adapterStore` case, but that's contract creation, and this contract can only be used within the system after admin action)*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Protocol OFT Integration Differential Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

