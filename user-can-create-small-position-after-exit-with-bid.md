---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27453
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4.000752964686205
rarity_score: 3.00150592937241

# Context Tags
tags:
  - liquidation
  - missing_check

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xbepresent
  - rvierdiiev
  - T1MOH
  - 0xffchain
---

## Vulnerability Title

User can create small position after exit with bid

### Overview


This bug report is about a vulnerability in the ExitShortFacet.sol function, which allows a user to partially exit from a position. The function accepts a buyBackAmount parameter which is the amount of debt that the user wants to repay. To cover this debt, the function creates a force bid on behalf of the user with the buyBackAmount as the needed asset. 

The problem is that the function only checks that the position is not too small at the beginning of the action. This means that if the buyBackAmount equals the e.ercDebt, the check is skipped and it is possible for the e.ercAmountLeft to be smaller than the needed min position. This can be done accidentally or an attacker can control this behavior by providing the price of the bid. This creates the ability to have small positions which liquidators may not be interested in liquidating, creating bad debt.

The impact of this vulnerability is that small positions can be created. The tools used to identify this bug were VsCode. The recommendation to fix this bug is to check the position size after the bid matching, when it is known exactly how much is left.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ExitShortFacet.sol#L175-L180">https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ExitShortFacet.sol#L175-L180</a>


## Summary
User can create small position after exit with bid, because there is no validation after matching.
## Vulnerability Details
Shorter can partially exit from position using `ExitShortFacet.exitShort` function. This function acccepts `buyBackAmount` param which is debt amount that user wants to repay.
In order to cover debt, function [will create force bid](https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ExitShortFacet.sol#L210-L212) on behalf of user with `buyBackAmount` as needed asset.

In the beginning function checks that [position will not be too small](https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ExitShortFacet.sol#L175-L180) after this action. In case if `buyBackAmount == e.ercDebt` then this check is skipped. This is needed in order to not allow small positions as it creates risks for the system.

The problem is that such check is not enough and it should be actually done after the bid matching, when you know how many assets were purchased. This is because, matching doesn't guarantee, that there is enough amount that can be sold. As result, not whole `buyBackAmount` can be acquired.
So in case if user provides `buyBackAmount == e.ercDebt` then check is skipped and it's possible that `e.ercAmountLeft` will be smaller than needed min position.

While this can happen accidentally, also attacker can control this behavour, as he can also provide the price of bid. So he can have a bot that will check ask/short lists and provide such bid, that will fill almost, but not whole `buyBackAmount`. This creates ability to have small positions, which liquidators may not be interested to liquidate, which can create bad debt.
## Impact
Small positions can be created.
## Tools Used
VsCode
## Recommendations
I think that you need to check position size after bid matching, when you know exactly what have left.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4.000752964686205/5 |
| Rarity Score | 3.00150592937241/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | 0xbepresent, rvierdiiev, T1MOH, 0xffchain |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`Liquidation, Missing Check`

