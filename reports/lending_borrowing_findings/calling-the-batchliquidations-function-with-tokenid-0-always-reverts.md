---
# Core Classification
protocol: Core, Strategies and Periphery
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51007
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/gammaswap-labs/core-strategies-and-periphery-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/gammaswap-labs/core-strategies-and-periphery-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

CALLING THE BATCHLIQUIDATIONS FUNCTION WITH TOKENID 0 ALWAYS REVERTS

### Overview


The `_batchLiquidations` function in the `LiquidationStrategy` contract is meant to perform multiple liquidations at once. However, there is a bug where it is not possible to use `0` as the `tokenId` when using this function. This results in an error when the function tries to calculate the `liquidity` variable. The impact and likelihood of this bug are both rated as 3 out of 5. The recommendation is marked as "not applicable" because the team has confirmed that this error is intended.

### Original Finding Content

##### Description

The `_batchLiquidations` function implemented in the `LiquidationStrategy` contract is designed to perform more than one liquidation in a go. The `tokenId > 0` check on the `payLoanAndRefundLiquidator` function assures that users can use `0` as `tokenId` for batch liquidation operation. However, it is not possible to use `0` as `tokenId` in the `_batchLiquidations` function.

The `_batchLiquidations` function makes an internal call to the `sumLiquidity` function. During the calculation of the `liquidity` variable, the execution is reverted with the **Division or modulo by 0** error since the `_loan.rateIndex` is also zero for `tokenId` 0.

Code Location
-------------

#### LiquidationStrategy.sol

```
function sumLiquidity(uint256[] calldata tokenIds) internal virtual returns(uint256 liquidityTotal, uint256 collateralTotal, uint256 lpTokensPrincipalTotal, uint128[] memory tokensHeldTotal) {
    address[] memory tokens = s.tokens;
    uint128[] memory tokensHeld;
    address cfmm = s.cfmm;
    tokensHeldTotal = new uint128[](tokens.length);
    (uint256 accFeeIndex,,) = updateIndex();
    for(uint256 i = 0; i < tokenIds.length; i++) {
        LibStorage.Loan storage _loan = s.loans[tokenIds[i]];
        uint256 liquidity = uint128((_loan.liquidity * accFeeIndex) / _loan.rateIndex);
        tokensHeld = _loan.tokensHeld;
        lpTokensPrincipalTotal = lpTokensPrincipalTotal + _loan.lpTokens;
        _loan.liquidity = 0;
        _loan.initLiquidity = 0;
        _loan.rateIndex = 0;
        _loan.lpTokens = 0;
        uint256 collateral = calcInvariant(cfmm, tokensHeld);
        canLiquidate(collateral, liquidity, 950);
        collateralTotal = collateralTotal + collateral;
        liquidityTotal = liquidityTotal + liquidity;
        for(uint256 j = 0; j < tokens.length; j++) {
            tokensHeldTotal[j] = tokensHeldTotal[j] + tokensHeld[j];
            _loan.tokensHeld[j] = 0;
        }
    }
}

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**NOT APPLICABLE:** The `GammaSwap team` confirmed that throwing the "Division or modulo by zero" error is the intended behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Core, Strategies and Periphery |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/gammaswap-labs/core-strategies-and-periphery-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/gammaswap-labs/core-strategies-and-periphery-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

