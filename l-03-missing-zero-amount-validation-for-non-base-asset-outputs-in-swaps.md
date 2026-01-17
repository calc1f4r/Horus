---
# Core Classification
protocol: Covenant_2025-08-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62830
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] Missing zero amount validation for non-base asset outputs in swaps

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The `checkSwapOutputs` function in ValidationLogic only validates zero output amounts when assetOut is `AssetType.BASE`, but fails to perform the same validation when the output asset is `AssetType.LEVERAGE` or `AssetType.DEBT`. This inconsistency could allow swaps that result in zero synthetic tokens being minted, leading to poor user experience and potential loss of input tokens.

```solidity
    function checkSwapOutputs(
        SwapParams calldata swapParams,
        uint256 baseSupply,
        uint256 amountCalculated
    ) internal pure {
        ...
        if ((swapParams.assetOut == AssetType.BASE) && (amountCalculated == 0)) revert Errors.E_InsufficientAmount(); // @audit Only checks zero for BASE tokens
}
    }
```

It's recommended to add a zero amount check for all asset types:

```solidity
if (amountCalculated == 0) revert Errors.E_InsufficientAmount();
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Covenant_2025-08-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

