---
# Core Classification
protocol: Definer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13535
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/02/definer/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Wade
  - Shayan Eskandari
---

## Vulnerability Title

Overcomplicated unit conversions

### Overview


This bug report is about the unit conversions in the system which are implemented in a confusing way and could lead to mistakes in the conversion and accounting. This could result in loss of funds. The report provides three examples of unit conversion in the system. The first example is related to the function getBorrowRatePerBlock, the second example is related to the compoundPool depositRatePerBlock and the third example is related to the lastDepositeRateIndex. The report recommends simplifying the unit conversions in the system either by using a function wrapper for units to convert all values to the same unit before including them in any calculation or by better documenting every line of unit conversion.

### Original Finding Content

#### Description


There are many instances of unit conversion in the system that are implemented in a confusing way. This could result in mistakes in the conversion and possibly failure in correct accounting. It’s been seen in the ecosystem that these type of complicated unit conversions could result in calculation mistake and loss of funds.


#### Examples


Here are a few examples:


* /contracts/Bank.sol#L216-L224



```
    function getBorrowRatePerBlock(address \_token) public view returns(uint) {
        if(!globalConfig.tokenInfoRegistry().isSupportedOnCompound(\_token))
        // If the token is NOT supported by the third party, borrowing rate = 3% + U \* 15%.
            return getCapitalUtilizationRatio(\_token).mul(globalConfig.rateCurveSlope()).div(INT\_UNIT).add(globalConfig.rateCurveConstant()).div(BLOCKS\_PER\_YEAR);

        // if the token is suppored in third party, borrowing rate = Compound Supply Rate \* 0.4 + Compound Borrow Rate \* 0.6
        return (compoundPool[\_token].depositRatePerBlock).mul(globalConfig.compoundSupplyRateWeights()).
            add((compoundPool[\_token].borrowRatePerBlock).mul(globalConfig.compoundBorrowRateWeights())).div(10);
    }

```
* /contracts/Bank.sol#L350-L351



```
                compoundPool[\_token].depositRatePerBlock = cTokenExchangeRate.mul(UNIT).div(lastCTokenExchangeRate[cToken])
                    .sub(UNIT).div(blockNumber.sub(lastCheckpoint[\_token]));

```
* /contracts/Bank.sol#L384-L385



```
        return lastDepositeRateIndex.mul(getBlockNumber().sub(lcp).mul(depositRatePerBlock).add(INT\_UNIT)).div(INT\_UNIT);


```
#### Recommendation


Simplify the unit conversions in the system. This can be done either by using a function wrapper for units to convert all values to the same unit before including them in any calculation or by better documenting every line of unit conversion

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Definer |
| Report Date | N/A |
| Finders | Alex Wade, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/02/definer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

