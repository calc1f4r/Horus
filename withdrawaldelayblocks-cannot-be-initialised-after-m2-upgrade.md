---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53719
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

withdrawalDelayBlocks Cannot Be Initialised After M2 Upgrade

### Overview


The bug report is about a storage variable called `withdrawalDelayBlocks` that cannot be initialized in the `DelegationManager` contract. This means that there will be no delay in completing withdrawals, which could potentially lead to a security risk in the future. To fix this issue, it is recommended to deploy and initialize a new `DelegationManager` proxy. Alternatively, the `withdrawalDelayBlocks` variable has been changed to `minWithdrawalDelayBlocks` and a new function has been added to update it after initialization. This bug has been addressed in PR #439.

### Original Finding Content

## Description

The `withdrawalDelayBlocks` storage variable will not be able to be initialized; hence there will be no delay on completing withdrawals in `DelegationManager`.

In the M2 upgrade, the `withdrawalDelayBlocks` storage variable has been moved from `StrategyManager` to the `DelegationManager`. However, `withdrawalDelayBlocks` can only be initialized in the `initialize()` function, which cannot be called again as the `DelegationManager` contract has already been initialized.

It is worth noting that currently, the risk to funds on the EigenLayer Beacon Chain Strategy might not be present. However, depending on future integrations with an AVS, default values for `withdrawalDelayBlocks` may prevent an AVS from responding to same block withdrawals of malicious restaked operators. This would significantly increase the severity of this bug from what is reported currently.

## Recommendations

Since the `DelegationManager` contract is not being used on the Ethereum mainnet, this issue can be avoided by deploying and initializing a new `DelegationManager` proxy that points to the M2 `DelegationManager` implementation. 

- Avoid upgrading and using the current `DelegationManager` proxy on mainnet.
- Keep in mind that the M2 `StrategyManager` and `EigenPodManager` implementation contracts will need to reference the new `DelegationManager` proxy address, so the `DelegationManager` should be upgraded first.
- An alternative fix is to use the `reinitialize()` modifier on a function that sets `withdrawalDelayBlocks`.

## Resolution

The `withdrawalDelayBlocks` variable was changed to `minWithdrawalDelayBlocks`. An `onlyOwner` function `setMinWithdrawalDelayBlocks()` was added to update this variable after initialization. This issue has been addressed in PR #439.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf

### Keywords for Search

`vulnerability`

