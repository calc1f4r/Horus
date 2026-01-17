---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18895
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-3 disordered fee calculated causes collateral changes to be inaccurate

### Overview


This bug report concerns the `_increasePosition()` function in a Hedger’s GMX position. The function changes the Hedger’s GMX position by the amount of **sizeDelta** and **collateralDelta**. There are two **collateralDelta** corrections - one for swap fees and one for position fees. The current order of the calculations was leading to the leverage ratio being higher than intended, as **collateralDelta** sent to GMX was lower than it should be. 

The recommended mitigation for this bug was to flip the order of `getSwapFeeBP()` and `_getPositionFee()`. The team responded that this bug has been fixed.

### Original Finding Content

**Description:**
`_increasePosition()` changes the Hedger’s GMX position by **sizeDelta** amount and 
**collateralDelta** collateral. There are two **collateralDelta** corrections - one for swap fees and 
one for position fees. Since the swap fee depends on up-to-date **collateralDelta**, it’s important 
to calculate it after the position fee, contrary to the current state. In practice, it may lead to 
the leverage ratio being higher than intended as **collateralDelta** sent to GMX is lower than it 
should be.
```solidity
      if (isLong) {
          uint swapFeeBP = getSwapFeeBP(isLong, true, collateralDelta);
           collateralDelta = (collateralDelta * (BASIS_POINTS_DIVISOR + swapFeeBP)) / BASIS_POINTS_DIVISOR;
      }
      // add margin fee
      // when we increase position, fee always got deducted from collateral
          collateralDelta += _getPositionFee(currentPos.size, sizeDelta, currentPos.entryFundingRate);
``` 

**Recommended Mitigation:**
Flip the order of `getSwapFeeBP()` and `_getPositionFee()`. 

**Team response:**
Fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

