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
solodit_id: 53313
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

[C-02] Passing the wrong value to `_burn()` function

### Overview


The report is about a bug in the `OmoVault.sol` contract that affects the `topOff()` function. This function is used to transfer assets to users who have requested to redeem them. The bug causes the wrong amount of shares to be burned. The severity and likelihood of this bug are high, meaning it can have a significant impact and is likely to occur. The recommended solution is to replace the `agentBalance` variable with `record.shares` to ensure the correct amount of shares is burned.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The agent will call `topOff()` function in `OmoVault.sol` contract to transfer the asset to users who have filled the requests to redeem.
The user shares are still not burned yet. `topOff()` will burn them here

```solidity
File: OmoVault.sol

453:         _totalAssets -= agentBalance;
454:         _burn(address(this), agentBalance);

```

But it burns the wrong amount of share. because `agentBalance` is the amount of asset that gets transferred to the user.

## Recommendations

```diff
File: OmoVault.sol

453:         _totalAssets -= agentBalance;
-454:         _burn(address(this), agentBalance);
+454:         _burn(address(this), record.shares);

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

