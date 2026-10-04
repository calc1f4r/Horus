---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25569
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident-2
source_link: https://code4rena.com/reports/2021-09-sushitrident-2
github_link: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/25

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
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-09] range fee growth underflow

### Overview


This bug report was submitted by broccoli and affects the function `RangeFeeGrowth` in the ConcentratedLiquidityPool.sol file. When a pool crosses a tick, it only updates either `feeGrowthOutside0` or `feeGrowthOutside1`. This can cause a problem when `feeGrowthBelow + feeGrowthAbove` is not necessarily smaller than `_feeGrowthGlobal` as the user would not be able to mint or withdraw funds from the pool, causing them to become stuck in the contract. 

A proof of concept was provided using Hardhat, which demonstrated how the bug could be triggered. The bug was disputed by sarangparikh22 (Sushi), who suggested the example was invalid and needed to be corrected. alcueca (judge) asked if the example or the whole issue needed to be fixed, to which sarangparikh22 (Sushi) confirmed that the example was invalid but the issue was valid. The suggested fix is to swap the condition of feeGrowthGlobal.

### Original Finding Content

_Submitted by broccoli_

#### Impact
The function `RangeFeeGrowth` ([ConcentratedLiquidityPool.sol#L601-L633](https://github.com/sushiswap/trident/blob/c405f3402a1ed336244053f8186742d2da5975e9/contracts/pool/concentrated/ConcentratedLiquidityPool.sol#L601-L633)) would revert the transaction in some cases.

When a pool cross a tick, it only updates either `feeGrowthOutside0` or `feeGrowthOutside1`. [Ticks.sol#L23-L53](https://github.com/sushiswap/trident/blob/c405f3402a1ed336244053f8186742d2da5975e9/contracts/libraries/concentratedPool/Ticks.sol#L23-L53)

`RangeFeeGrowth` calculates the fee as follow:

```solidity
    feeGrowthInside0 = _feeGrowthGlobal0 - feeGrowthBelow0 - feeGrowthAbove0;
    feeGrowthInside1 = _feeGrowthGlobal1 - feeGrowthBelow1 - feeGrowthAbove1;
```

`feeGrowthBelow + feeGrowthAbove` is not necessary smaller than `_feeGrowthGlobal`. Please see `POC`.

Users can not provide liquidity or burn liquidity. Fund will get stocked in the contract. I consider this is a high-risk issue.

#### Proof of Concept
```python
    # This is the wrapper.
    # def add_liquidity(pool, amount, lower, upper)
    # def swap(pool, buy, amount)

    add_liquidity(pool, deposit_amount, -800, 500)
    add_liquidity(pool, deposit_amount, 400, 700)
    # We cross the tick here to trigger the bug.

    swap(pool, False, deposit_amount)
    # Only tick 700's feeGrowthOutside1 is updated

    swap(pool, True, deposit_amount)
    # Only tick 500's feeGrowthOutside0 is updated

    # current tick at -800

    # this would revert
    # feeGrowthBelow1 = feeGrowthGlobal1
    # feeGrowthGlobal1 - feeGrowthBelow1 - feeGrowthAbove1 would revert
    # user would not be able to mint/withdraw/cross this tick. The pool is broken
    add_liquidity(pool, deposit_amount, 400, 700)
```

#### Tools Used
Hardhat

#### Recommended Mitigation Steps
It's either modify the tick's algo or `RangeFeeGrowth`. The quick-fix I come up with is to deal with the fee in `RangeFeeGrowth`. However, I recommend the team to go through tick's logic again.

**[sarangparikh22 (Sushi) disputed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/25#issuecomment-942800266):**
 > The example is wrong, you can't add use upper tick as odd, correct the example and resubmit please.

**[alcueca (judge) commented](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/25#issuecomment-967128882):**
 > @sarangparikh22 (Sushi), is the example invalid, or the whole issue? Is this something that you would consider fixing?

**[sarangparikh22 (Sushi) confirmed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/25#issuecomment-972242461):**
 > @alcueca (judge) The example is invalid, but the issue is valid, the fix is to swap the condition of feeGrowthGlobal



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident-2
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/25
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident-2

### Keywords for Search

`vulnerability`

