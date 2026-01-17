---
# Core Classification
protocol: Pike
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47964
audit_firm: OtterSec
contest_link: https://www.pike.finance/
source_link: https://www.pike.finance/
github_link: https://github.com/nutsfinance/pike-universal

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Bypass Of Over-Collateralization Checks

### Overview


The processBorrow function in the HubMessageHandler contract has a bug that allows users to open loans without enough collateral. This is because the function skips over assets with zero collateral amounts, resulting in incorrect calculations for the total collateral and borrow amount. This can be exploited by an attacker to steal all funds from the hub. The recommended fix is to remove the highlighted portion of the code in the processBorrow function.

### Original Finding Content

## Vulnerability Report: processBorrow Function

The `processBorrow` function exhibits an exploitable defect in its loan value computation logic, which allows users to open under-collateralized debts. The `hub` iterates over each of the whitelisted assets with non-zero collateral amounts, and in each iteration, it adds the loan amount read from the `collateralBalances` mapping. However, assets with zero collateral amounts become neglected, resulting in both `totalCollateralInUsd` and `borrowAmountInUSD` accumulating to zero for a borrower with no collateral, regardless of the true loan amount.

### Affected Code Snippet

Located in `src/contracts/hub/HubMessageHandler.sol`:

```solidity
function processBorrow(
    /* ... */
)
/* ... */
{
    // Accumulating the total user's collateral in USD according to oracle
    uint256 totalCollateralInUSD;
    uint256 borrowAmountInUSD;
    uint256 numChains = chains.length;
    for (uint16 i; i < numChains;) {
        PythStructs.Price memory asset =
            pikeOracle.getAssetPrice(chains[i], address(0), 0);
        require(asset.price > 0, Errors.NEGATIVE_PRICE_FOUND);
        // Skipping chains where user hasn't supplied any collateral
        if (collateralBalances[chains[i]][params.user] == 0) {
            continue;
        }
        // Getting borrowAmount on target chain denominated for comparison
        if (chains[i] == params.targetChainId) {
            borrowAmountInUSD = uint256(uint64(asset.price));
        }
        totalCollateralInUSD +=
            collateralBalances[chains[i]][params.user] *
            uint256(uint64(asset.price));
        unchecked {
            ++i;
        }
    }
    // Check if enough collateral to begin with
    require(totalCollateralInUSD >= borrowAmountInUSD, Errors.NOT_ENOUGH_COLLATERAL);
    /* ... */
}
```

### Impact

An attacker may steal all funds from the hub by depositing no assets and borrowing large amounts.

### Remediation

To fix the vulnerability, remove the highlighted portion of the code in `processBorrow`.

© 2023 Otter Audits LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pike |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://www.pike.finance/
- **GitHub**: https://github.com/nutsfinance/pike-universal
- **Contest**: https://www.pike.finance/

### Keywords for Search

`vulnerability`

