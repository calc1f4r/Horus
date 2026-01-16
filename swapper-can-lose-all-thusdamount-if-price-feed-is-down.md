---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54692
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
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
finders_count: 3
finders:
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

Swapper can lose all thusdAmount if Price Feed is down 

### Overview


The report discusses a bug in a smart contract called BAMM.sol, specifically in the swap function. This function is supposed to allow users to purchase collateral and automatically compound it into more THUSD. However, if the call to the Chainlink Price Feed fails, the function will return 0, causing the user to pay for THUSD but receive no collateral in return. The report recommends adding a check to revert the transaction if the price feed is down to prevent users from losing funds. The report also mentions another unrelated check that was added recently and always leads to failure. The bug has been fixed in a recent commit.

### Original Finding Content

## Context
**BAMM.sol#L256-L271**

## Description
The swap function is meant to allow purchasing of collateral as a way to automate auto-compounding of collateral into more THUSD. To allow the swap, `getSwapCollateralAmount` will query the Chainlink Price Feed for the Collateral / USD pair and use that value to compute the price. 

In the case in which the call fails, `getSwapCollateralAmount` will return `0`, which means that `msg.sender` will pay the `thusdAmount` but receives no collateral in return, as seen in **BAMM.sol#L234**:

```solidity
if(collateral2usdPrice == 0) return (0, 0); // chainlink is down
```

The slippage check would prevent this from happening, but a distracted buyer (or an automated strategy) may just use `0`, causing the transaction to go through.

## Recommendation
Consider reverting if the price feed is down to avoid the caller losing funds.

## Threshold
There is one check for the swap function (in commit **d5e7a5**) that was added recently. This is unrelated to the suggestion but it will always lead to failure because `minReturn` can't be `0` and `collateralAmount` must be greater than `0`.

## Cantina
Verified that this is fixed with the changes shown in commit **d5e7a5**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

