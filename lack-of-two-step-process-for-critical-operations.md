---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17882
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of two-step process for critical operations

### Overview


This bug report is about several critical operations being executed in one function call in Frax.sol, veFXS.vy, FXS.sol, FraxPool.sol, and CurveAMO_V3.sol. This can lead to irrevocable mistakes, such as the incorrect setting of an owner address, which could result in the protocol permanently losing the ability to execute critical operations. To prevent this issue, Trail of Bits recommends using a two-step process for all non-recoverable critical operations in the short term, and identifying and documenting all possible actions that can be taken by privileged accounts and their associated risks in the long term. This will help to facilitate reviews of the codebase and prevent future mistakes.

### Original Finding Content

## Auditing and Logging

**Type:** Auditing and Logging  
**Target:** Frax.sol, veFXS.vy, FXS.sol, FraxPool.sol, CurveAMO_V3.sol

**Difficulty:** Low  

## Description
Several critical operations are executed in one function call. This schema is error-prone and can lead to irrevocable mistakes. For example, the `owner_address` variable defines the address that can add/remove pools, set parameters in the system, and update oracles. The setter function for this address immediately sets the new owner address:

```solidity
function setOwner(address _owner_address) external onlyByOwnerOrGovernance {
    owner_address = _owner_address;
}
```
*Figure 2.1: contracts/Frax/Frax.sol#L259-L261*

If the address is incorrect, the protocol could permanently lose the ability to execute critical operations. This issue is also present in the following contracts:
- FraxPool.sol - setOwner
- FXS.sol - setOwner

## Exploit Scenario
Alice, a member of the Frax Finance team, sets a new address as the owner. However, because the new address includes a typo, the Frax Finance team loses the ability to add new pools. To address the issue, the team must deploy a new set of contracts with the correct owner.

## Recommendations
Short term, use a two-step process for all non-recoverable critical operations (such as `setNewOwner` and `acceptNewOwner`) to prevent irrevocable mistakes.

Long term, identify and document all possible actions that can be taken by privileged accounts and their associated risks. This will facilitate reviews of the codebase and prevent future mistakes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

