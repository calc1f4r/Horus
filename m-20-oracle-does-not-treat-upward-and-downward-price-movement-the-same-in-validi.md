---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16003
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/487

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-20] Oracle does not treat upward and downward price movement the same in validity checks, causing safety issues in oracle usage

### Overview


The NFTFloorOracle in the code retrieves ERC721 prices for ParaSpace. It has a parameter called maxPriceDeviation which limits the change percentage from current price to a new feed update. However, the way it is calculated means price decrease is much more sensitive and likely to be invalid than a price increase. This behavior can cause safety issues in the oracle usage and should be addressed. 

The recommended mitigation step is to use a percentage base calculation for both upward and downward price movements. This bug was discovered through manual audit.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/misc/NFTFloorOracle.sol#L365>

NFTFloorOracle retrieves ERC721 prices for ParaSpace. maxPriceDeviation is a configurable parameter, which limits the change percentage from current price to a new feed update. We can see how priceDeviation is calculated and compared to maxPriceDeviation in \_checkValidity:

    priceDeviation = _twap > _priorTwap
        ? (_twap * 100) / _priorTwap
        : (_priorTwap * 100) / _twap;
    // config maxPriceDeviation as multiple directly(not percent) for simplicity
    if (priceDeviation >= config.maxPriceDeviation) {
        return false;
    }
    return true;

The large number minus small number must be smaller than maxPriceDeviation. However, the way it is calculated means price decrease is much more sensitive and likely to be invalid than a price increase.

`10 -> 15, priceDeviation = 15 / 10 = 1.5`<br>
`15 -> 10, priceDeviation = 15 / 10 = 1.5`

From 10 to 15, price rose by 50%. From 15 to 10, price  dropped by 33%. Both are the maximum change that would be allowed by deviation parameter. The effect of this behavior is that the protocol will be either too restrictive in how it accepts price drops, or too permissive in how it accepts price rises.

### Impact

Oracle does not treat upward and downward price movement the same in validity checks, causing safety issues in oracle usage.

### Recommended Mitigation Steps

Use a percentage base calculation for both upward and downward price movements.

**[WalidOfNow (Paraspace) commented](https://github.com/code-423n4/2022-11-paraspace-findings/issues/487#issuecomment-1404056674):**
 > Going from 10 to 15 is 50% and from 15 to 10 is 33% percent. This is desired behaviour here. Why should we treat 33% as 50%?

**[Trust (warden) commented](https://github.com/code-423n4/2022-11-paraspace-findings/issues/487#issuecomment-1404113039):**
 > That is exactly the point of this submission. Right now, you are treating both price movements (10-15, 15-10) the same, even though one is 50% and the other is 33%. 
> 
> You are being far too permissive in upward price changes compared to downward changes, when accepting deviations.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/487
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

