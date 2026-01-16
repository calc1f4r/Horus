---
# Core Classification
protocol: Fei Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11004
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fei-protocol-audit/
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M04] Incorrect proposal and quorum thresholds for voting

### Overview


A bug report has been filed regarding the `Tribe` tokens used for governance. The `totalSupply` of `Tribe` tokens is set to 1 billion tokens with 18 decimals. The `proposalThreshold` and `quoromVotes` require only 0.01% and 0.1% of `Tribe` supply respectively, while the comments in the code indicate this should be 1% and 10% respectively. This inconsistency has been resolved in a Pull Request (#49) where the amount of quorum votes was changed to 25,000,000 (2.5% of Tribe’s total supply) and the proposal threshold was changed to 2,500,000 (0.25% of Tribe’s total supply).

### Original Finding Content

`Tribe` tokens are used for governance, with the [`totalSupply`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/dao/Tribe.sol#L22) set to 1 billion tokens with [`18 decimals`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/dao/Tribe.sol#L18). The amount of `Tribe` required to reach the [`proposalThreshold`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/dao/GovernorAlpha.sol#L15) for a vote is only `0.01%` of `Tribe` supply, although the comments indicate this should be `1%`. Likewise, in order for a vote to succeed, the [`quoromVotes`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/dao/GovernorAlpha.sol#L12) requires only `0.1%` of `Tribe` supply, although the comments indicate this should be `10%`. These inconsistencies should be resolved.


**Update:** *Fixed in [PR#](https://github.com/fei-protocol/fei-protocol-core/pull/49). The amount of quorum votes was changed to 25,000,000 (2.5% of Tribe’s total supply), and the proposal threshold was changed to 2,500,000 (0.25% of Tribe’s total supply).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Fei Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fei-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

