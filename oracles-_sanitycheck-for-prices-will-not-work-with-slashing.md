---
# Core Classification
protocol: Geodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20748
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/11/geodefi/
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
finders_count: 3
finders:
  - Sergii Kravchenko
  -  Christian Goll
  -  Chingiz Mardanov

---

## Vulnerability Title

Oracle’s _sanityCheck for prices will not work with slashing

### Overview


This bug report is about the `_sanityCheck` feature in the OracleUtilsLib.sol file. This feature is used to verify that the new price hasn’t changed significantly. The bug is that if there is a slashing event, the oracle will not be updated because of the sanity check, which could lead to an arbitrage opportunity and the devaluation of gETH to zero. The recommendation is to make sure that slashing can be adequately processed when updating the price.

### Original Finding Content

#### Description


The `_sanityCheck` is verifying that the new price didn’t change significantly:


**code/contracts/Portal/utils/OracleUtilsLib.sol:L405-L417**



```
uint256 maxPrice = curPrice +
 ((curPrice \*
 self.PERIOD\_PRICE\_INCREASE\_LIMIT \*
 \_periodsSinceUpdate) / PERCENTAGE\_DENOMINATOR);

uint256 minPrice = curPrice -
 ((curPrice \*
 self.PERIOD\_PRICE\_DECREASE\_LIMIT \*
 \_periodsSinceUpdate) / PERCENTAGE\_DENOMINATOR);

require(
 \_newPrice >= minPrice && \_newPrice <= maxPrice,
 "OracleUtils: price is insane"

```
While the rewards of staking can be reasonably predicted, the balances may also be changed due to slashing. So any slashing event should reduce the price, and if enough ETH is slashed, the price will drop heavily. The oracle will not be updated because of a sanity check. After that, there will be an arbitrage opportunity, and everyone will be incentivized to withdraw as soon as possible. That process will inevitably devaluate gETH to zero.
The severity of this issue is also amplified by the fact that operators have no skin in the game and won’t lose anything from slashing.


#### Recommendation


Make sure that slashing can be adequately processed when updating the price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geodefi |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Christian Goll,  Chingiz Mardanov
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/11/geodefi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

