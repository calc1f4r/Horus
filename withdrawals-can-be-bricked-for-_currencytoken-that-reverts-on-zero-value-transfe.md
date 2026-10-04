---
# Core Classification
protocol: MetaStreet Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54565
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7a8af297-2633-4a86-b325-22e4e3a670d7
source_link: https://cdn.cantina.xyz/reports/cantina_metastreet_aug2023.pdf
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
finders_count: 2
finders:
  - HickupHH3
  - Anurag Jain
---

## Vulnerability Title

Withdrawals can be bricked for _currencyToken that reverts on zero value transfers 

### Overview

See description below for full details.

### Original Finding Content

## Context
- **Files**: `Pool.sol#L1167-L1168`, `MstWrapper.sol#L291-L292`

## Description
The redemption queue scanning limit increases the likelihood of the withdrawn amount to be zero. In such scenarios, should the `_currencyToken` revert on zero value transfers, both withdrawals and rebalances would fail for the user, causing their funds to be stuck. Consider the following example:

- Alice has a pending redemption of 1018
- Bob is next in queue (his redemption target is 1018)
- Attack proceeds to create `MAX_REDEMPTION_QUEUE_SCAN_COUNT = 150` redemptions (e.g., do 150 deposits), where total redemption amount is less than 1018.
- Bob will be unable to withdraw and advance his queue index because `processedIndices` will be 150, but amount will be 0. He's also unable to rebalance because `_deposit()` checks for 0 shares.

## Recommendation
Only execute the transfer for non-zero amounts.

```solidity
_currencyToken.safeTransfer(msg.sender, amount);
```

Should be changed to:

```solidity
if (amount > 0) _currencyToken.safeTransfer(msg.sender, amount);
```

## Metastreet
Resolved in commit `2dbd05f` and commit `c3e32f1`.

## Cantina
The aforementioned commits fixed the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MetaStreet Labs |
| Report Date | N/A |
| Finders | HickupHH3, Anurag Jain |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_metastreet_aug2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7a8af297-2633-4a86-b325-22e4e3a670d7

### Keywords for Search

`vulnerability`

