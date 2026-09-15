---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33569
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#1-no-slippage-protection
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
  - MixBytes
---

## Vulnerability Title

No Slippage Protection

### Overview


The bug report discusses an issue with the `ExternalRequestsManagerBetaV1` contract in the `resolv-contracts` repository. The problem is that the amounts of tokens being minted and transferred in the `completeMint()` and `completeBurn()` functions are not being checked against an on-chain oracle, which can result in users receiving less tokens than they expected due to slippage. The recommendation is to add the `minAmountOut` and `deadline` parameters to the workflow to prevent this issue.

### Original Finding Content

##### Description

- https://github.com/resolv-im/resolv-contracts/blob/a36e73c4be0b5f233de6bfc8d2c276136bf67573/contracts/beta/ExternalRequestsManagerBetaV1.sol#L234
- https://github.com/resolv-im/resolv-contracts/blob/a36e73c4be0b5f233de6bfc8d2c276136bf67573/contracts/beta/ExternalRequestsManagerBetaV1.sol#L175

The amounts of tokens to mint and transfer in `completeMint()` and `completeBurn()` in the `ExternalRequestsManagerBetaV1` are not related to any on-chain oracle and are prone to slippage: users may receive less tokens than they expected.

##### Recommendation
We recommend adding the `minAmountOut` and `deadline` parameters to the workflow.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#1-no-slippage-protection
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

