---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57933
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#4-missing-zero-address-validation-and-boundaries-check-in-diarewardsdistribution-constructor
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
  - MixBytes
---

## Vulnerability Title

Missing zero-address validation and boundaries check in `DIARewardsDistribution` constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
The constructor in `DIARewardsDistribution` does not validate that `rewardsTokenAddress` or `newRewardsWallet` parameters are non-zero addresses. Setting either parameter to address(0) during deployment would create a non-functional contract: a zero token address would cause all reward distribution calls to fail, while a zero rewards wallet would prevent any reward transfers. This creates an inconsistency with the `updateRewardsWallet()` function which properly validates against zero addresses using `require(newWalletAddress != address(0))`. While the contract would naturally revert when attempting to interact with zero addresses, explicit validation provides clearer error messages for debugging deployment issues and prevents deploying immediately non-functional contracts.

There is also a `rewardRatePerDay` parameter being set, which should be checked not to exceed some organic values. If this value is mistakenly set too high, it is possible for any staker to claim unproportional amount of rewards before this rate get reset back to normal value by the contract owner.
<br/>
##### Recommendation
We recommend adding zero-address validation in the constructor: `require(rewardsTokenAddress != address(0), "Invalid token address")` and `require(newRewardsWallet != address(0), "Invalid wallet address")` to maintain consistency with other validation patterns in the contract.
Also, it is important to check that `rewardRatePerDay` parameter fits into some pre-defined range aligned with the staking logic.

> **Client's Commentary:**
> checks are added

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#4-missing-zero-address-validation-and-boundaries-check-in-diarewardsdistribution-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

