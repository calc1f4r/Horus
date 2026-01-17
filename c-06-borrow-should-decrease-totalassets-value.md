---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53317
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-06] `borrow()` should decrease `totalAssets` value

### Overview


The OmoVault contract has a bug in the `borrow()` function, which is only used by the agent. This function transfers assets to the agent, but there is no system in place to keep track of these debts. This means that the contract relies on off-chain security, which is not ideal. Additionally, the `_totalAssets` variable is not being updated, which affects the calculation of `totalAssets()`. The current implementation counts the borrowed assets by the agent twice, when it should only be the sum of all assets in the vault and all Uni V3 position values in DynamicAccounts. To fix this, it is recommended to update the `_totalAssets` variable in the `borrow()` function to subtract the borrowed assets from the total. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The `OmoVault.sol` contract has a `borrow()` used only by the agent, which transfers assets to the Agent.
It has no tracking system for those debts (it depends on off-chain security).
Also, it does not update the `_totalAssets` variable

```solidity
File: OmoVault.sol

403:     function borrow(uint256 assets, address receiver) external nonReentrant onlyAgent {
407:         address msgSender = msg.sender;
409:         require(assets != 0, "ZERO_ASSETS");
411:         asset.safeTransfer(receiver, assets);
414:     }

```

This will affect the `totalAssets()` calculation,because The current implementation computes the borrowed assets by the agent two times.
But the `totalAssets()` should be the sum of all assets in the vault and all Uni V3 position values in DynamicAccounts.

## Recommendations

```diff
File: OmoVault.sol

403:     function borrow(uint256 assets, address receiver) external nonReentrant onlyAgent {
407:         address msgSender = msg.sender;
409:         require(assets != 0, "ZERO_ASSETS");
+410:      _totalAssets =  _totalAssets - assets;
411:         asset.safeTransfer(receiver, assets);
414:     }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

