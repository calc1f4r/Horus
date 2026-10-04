---
# Core Classification
protocol: LMCV part 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50711
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

DIVISION BY ZERO IN ISWITHINCREDITLIMIT

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `isWithinCreditLimit` function does not handle leveraged-only collateral properly. When leveraged-only collateral is passed, and the credit value exceeds the collateral value, the transaction fails with a `Division or modulo division by zero` error.

Code Location
-------------

[LMCV module](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/LMCV.sol#L575):

#### contracts/LMCV.sol

```
function isWithinCreditLimit(address user, uint256 rate) private view returns (bool) {
    bytes32[] storage lockedList = lockedCollateralList[user];
    uint256 creditLimit             = 0; // [rad]
    uint256 leverTokenCreditLimit   = 0; // [rad]
    uint256 noLeverageTotal         = 0; // [wad]
    uint256 leverageTotal           = 0; // [rad]
    for (uint256 i = 0; i < lockedList.length; i++) {
        Collateral memory collateralData = CollateralData[lockedList[i]];

        if(lockedCollateral[user][lockedList[i]] > collateralData.dustLevel){
            uint256 collateralValue = lockedCollateral[user][lockedList[i]] * collateralData.spotPrice; // wad*ray -> rad

            if(!collateralData.leveraged){
                creditLimit += _rmul(collateralValue, collateralData.creditRatio);
                noLeverageTotal += collateralValue / RAY;
            } else {
                leverageTotal += collateralValue;
                leverTokenCreditLimit += _rmul(collateralValue, collateralData.creditRatio);
            }
        }
    }

    // If only leverage tokens exist, just return their credit limit
    // Keep credit ratio low on levered tokens (60% or lower) to incentivize having non levered collateral in the vault
    if(noLeverageTotal == 0 && leverageTotal > 0 && leverTokenCreditLimit >= normalizedDebt[user] * rate){
        return true;
    }

    uint256 leverageMultiple = noLeverageTotal == 0 && leverageTotal == 0 ? RAY : RAY + leverageTotal / noLeverageTotal;

    if (_rmul(creditLimit, leverageMultiple) >= (normalizedDebt[user] * rate)) {
        return true;
    }
    return false;
}

```

##### Score

Impact: 2  
Likelihood: 3

##### Recommendation

**SOLVED**: The condition in the `isWithinLimit` function of the `LMCV.sol` contract was modified to handle correctly limits for leveraged tokens.

Reference: [LMCV.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/7feeca3e8d2659091aac25ac912dc034b4fbc719/contracts/lmcv/LMCV.sol#L605-L610)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

