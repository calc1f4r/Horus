---
# Core Classification
protocol: apDAO_2024-10-03
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44406
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] Failure of entropy source callback

### Overview


The `ApiologyAuctionHouse` contract relies on an external source called `Pyth Entropy` to generate random numbers for creating auctions. However, if the function responsible for handling the random number response, `ApiologyAuctionHouse::entropyCallback`, is not called, the contract cannot create new auctions. This creates a high impact on the contract's functionality and a low likelihood of occurrence. To fix this issue, a fallback mechanism should be implemented to re-request a random number if the callback is not received within a certain timeframe. This can be done using a timeout or a retry counter.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `ApiologyAuctionHouse` contract relies on an external entropy source, implemented through the `Pyth Entropy` contract, to provide random numbers necessary for creating auctions. The main function responsible for handling the random number response is `ApiologyAuctionHouse::entropyCallback`, which is supposed to be invoked by the entropy source. If this callback function is not called, the contract cannot proceed with creating new auctions that require randomness.

```solidity
File: ApiologyDAOAuctionHouse.sol
358:     function entropyCallback(uint64 sequenceNumber, address _providerAddress, bytes32 randomNumber) internal override {
359:         emit RandomNumberReceived(sequenceNumber, randomNumber);
360:>>>      _createAuctionWithRandomNumber(randomNumber);
361:     }
```

Without the callback, the auction creation process halts, preventing new auctions from being initiated. The inability to proceed automatically necessitates manual intervention, where the owner must pause and unpause the contract to reset auction creation mechanisms which introduces a central point of failure and potential misuse if the owner is unavailable or acts maliciously.

## Recommendations

Implement a fallback mechanism to re-request a random number if the callback is not received within a certain timeframe. This can be done using a timeout or a retry counter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | apDAO_2024-10-03 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

