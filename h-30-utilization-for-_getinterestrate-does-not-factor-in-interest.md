---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27520
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1057

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - ItsNio
  - SaeedAlipoor01988
---

## Vulnerability Title

[H-30] `utilization` for `_getInterestRate()` does not factor in interest

### Overview


A bug has been identified in the `SGLCommon.sol` contract in the `_getInterestRate()` function. The calculation for `utilization` does not factor in the accrued interest, which leads to `_accrueInfo.interestPerSecond` being under-represented. This results in an incorrect interest rate calculation and potentially endangering conditions such as `utilization > maximumTargetUtilization` on line 124. 

The calculation for `utilization` occurs on lines 61-64 as a portion of the `fullAssetAmount` and the `_totalBorrow.elastic`. The `_totalBorrow.elastic` is accrued by interest on line 99, however this accrued amount is not factored into the calculation for `utilization`.

To mitigate this bug, the interest accrual should be factored into the `utilization` calculation. This has been confirmed by 0xRektora (Tapioca).

### Original Finding Content


The calculation for `utilization` in `_getInterestRate()` does not factor in the accrued interest. This leads to `_accrueInfo.interestPerSecond` being under-represented, and leading to incorrect interest rate calculation and potentially endangering conditions such as `utilization > maximumTargetUtilization` on line [124](https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/singularity/SGLCommon.sol#L124).

### Proof of Concept

The calculation for `utilization` in the `_getInterestRate()` function for `SGLCommon.sol` occurs on lines [61-64](https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/singularity/SGLCommon.sol#L61-L64) as a portion of the `fullAssetAmount` (which is also problematic) and the `_totalBorrow.elastic`. However, `_totalBorrow.elastic` is accrued by interest on line [99](https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/singularity/SGLCommon.sol#L99). This accrued amount is not factored into the calculation for `utilization`, which will be used to update the new interest rate, as purposed by the comment on line [111](https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/singularity/SGLCommon.sol#L111).

### Recommended Mitigation Steps

Factor in the interest accrual into the `utilization` calculation:

    ...
            // Accrue interest
            extraAmount =
                (uint256(_totalBorrow.elastic) *
                    _accrueInfo.interestPerSecond *
                    elapsedTime) /
                1e18;
            _totalBorrow.elastic += uint128(extraAmount);
            
        +    uint256 fullAssetAmount = yieldBox.toAmount(    
        +        assetId,
        +        _totalAsset.elastic,
        +        false
        +    ) + _totalBorrow.elastic;
            //@audit utilization factors in accrual
        +    utilization = fullAssetAmount == 0
        +   ? 0
        +        : (uint256(_totalBorrow.elastic) * UTILIZATION_PRECISION) /
        +        fullAssetAmount;
    ...

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1057#issuecomment-1701770815)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | ItsNio, SaeedAlipoor01988 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1057
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

