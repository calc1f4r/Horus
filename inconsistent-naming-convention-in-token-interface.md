---
# Core Classification
protocol: EVM Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52025
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/apro/evm-smart-contracts
source_link: https://www.halborn.com/audits/apro/evm-smart-contracts
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
  - Halborn
---

## Vulnerability Title

Inconsistent Naming Convention in Token Interface

### Overview

See description below for full details.

### Original Finding Content

##### Description

The smart contract under review contains an interface named `LinkTokenInterface` in file AproTokenInterface.sol which is a direct copy from the Chainlink project. However, this project is named APRO, and the interface name has not been updated to reflect this fact. The current implementation is as follows:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

interface LinkTokenInterface {
// ... (interface functions)
}
```

  

This naming inconsistency is present throughout the interface, including comments that directly reference Chainlink:

```
// The client constructs and makes a request to a known Chainlink oracle through the transferAndCall function, implemented by the LINK token
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N (0.0)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N)

##### Recommendation

To address this issue, the following changes are recommended:

1. Rename the interface to reflect the APRO project
2. Update all references to Chainlink in comments and documentation within the interface

Remediation Plan
----------------

**SOLVED :** Naming conventions has been modified.

##### Remediation Hash

<https://github.com/APRO-Oracle/apro_contract/commit/3d6483f8f5d0cef2ef0b24c0f92cb7c28fbbd86e>

##### References

[APRO-Oracle/apro\_contract/contracts/offchain-aggregator/LinkTokenInterface.sol#L4](https://github.com/APRO-Oracle/apro_contract/blob/main/contracts/offchain-aggregator/LinkTokenInterface.sol#L4)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Smart Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/apro/evm-smart-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/apro/evm-smart-contracts

### Keywords for Search

`vulnerability`

