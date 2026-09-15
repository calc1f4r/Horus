---
# Core Classification
protocol: Asymmetry Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30020
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-09-asymmetry
source_link: https://code4rena.com/reports/2023-09-asymmetry
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

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-05] Missing check for zero address value in constructor or setter

### Overview

See description below for full details.

### Original Finding Content


Address parameters should be validated to guard against the default value `address(0)`.

*Instances (6)*:

- `vEthAddress` in [`AfEth::setStrategyAddress()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/AfEth.sol#L81)
- `feeAddress` in [`AfEth::setFeeAddress()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/AfEth.sol#L98)
- `rewarder` in [`VotiumStrategyCore::initialize()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/strategies/votium/VotiumStrategyCore.sol#L112)
- `manager` in [`VotiumStrategyCore::initialize()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/strategies/votium/VotiumStrategyCore.sol#L113)
- `chainlinkCvxEthFeed` in [`VotiumStrategyCore::setChainlinkCvxEthFeed()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/strategies/votium/VotiumStrategyCore.sol#L76)
- `rewarder` in [`VotiumStrategyCore::setRewarder()`](https://github.com/code-423n4/2023-09-asymmetry/blob/main/contracts/strategies/votium/VotiumStrategyCore.sol#L125)



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Asymmetry Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-09-asymmetry
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-09-asymmetry

### Keywords for Search

`vulnerability`

