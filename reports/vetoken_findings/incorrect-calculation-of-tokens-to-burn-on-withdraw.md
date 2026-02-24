---
# Core Classification
protocol: Radiant V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32847
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant
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
  - OpenZeppelin
---

## Vulnerability Title

Incorrect Calculation of Tokens to Burn on withdraw

### Overview


The `withdraw` function in the `MultiFeeDistribution` contract is used to withdraw earned and unlocked tokens. However, there is a bug in the code where the `burnAmount` is incorrectly calculated, leading to an inflated value. This bug can be fixed by replacing `penaltyAmount` with the individual penalty for the current loop iteration. The bug has been resolved in a recent pull request.

### Original Finding Content

The [`withdraw`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol#L805-L862) function of the `MultiFeeDistribution` contract implements the logic for withdrawing earned and unlocked tokens from the protocol. It loops through all earnings to sum the amount of earned tokens, [penalties](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol#L838) for the early withdrawal, and the [burn amounts](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol#L839).


The problem is that `burnAmount` is [incorrectly calculated](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol#L839) by using the total [`penaltyAmount`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol#L838) instead of the individual penalty for the current loop iteration, which leads to an inflated value of `burnAmount`.


It is recommended to correct the calculation of `burnAmount` by replacing `penaltyAmount` with the individual penalty associated with the current loop iteration.


***Update:** Resolved in [pull request #208](https://github.com/radiant-capital/v2-core/pull/208) at commit [65220b8](https://github.com/radiant-capital/v2-core/commit/65220b8fc57d26d820a7897278bba20ae4c5c9a2).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

