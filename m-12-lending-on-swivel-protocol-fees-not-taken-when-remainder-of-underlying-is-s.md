---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3740
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/12
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/45

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
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - kenzo
---

## Vulnerability Title

M-12: Lending on Swivel: protocol fees not taken when remainder of underlying is swapped in YieldPool

### Overview


This bug report is about an issue with the Swivel lending function, where the protocol fees are not taken when the remainder of underlying is swapped in YieldPool. The bug was found by kenzo and was manually reviewed. 

The bug is related to the `lend` function of Swivel, which allows swapping the remainder underlying on Yield. When executing orders on Swivel, if the user has set `e==true` and there is remaining underlying, the lending function will swap these funds using YieldPool. But it does not take the protocol fees on that amount, leading to some fees being lost. This means that users may be able to trade on the YieldPool without incurring protocol fees.

The code snippet provided in the report shows that in the `if(e)` block of Swivel's `lend`, the function `swivelLendPremium` is executed, which does not extract fees from the raw balance. The `yield` function that is called by `swivelLendPremium` also does not take protocol fees. 

The recommendation given is to extract the protocol fee from `premium` in the `if(e)` block of Swivel's `lend`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/45 

## Found by 
kenzo

## Summary
The `lend` function for Swivel allows swapping the remainder underlying on Yield.
But it does not take protocol fees on this amount.

## Vulnerability Detail
When executing orders on Swivel,
if the user has set `e==true` and there is remaining underlying,
the lending function will swap these funds using YieldPool.
But it does not take the protocol fees on that amount.

## Impact
Some protocol fees will be lost.
Users may even use this function to trade on the YieldPool without incurring protocol fees.
While I think it can be rightfully said that at that point they can just straight away trade on the YieldPool without incurring fees, that can also be said about the general Illuminate/Yield `lend` function, which swaps on the YieldPool and does extract fees.

## Code Snippet
In Swivel's [`lend` function](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L417),
if the user has set `e` to true,
the following block will be executed.
Note that no fees are extracted from the raw balance.
```solidity
                if (e) {
                    // Calculate the premium
                    uint256 premium = IERC20(u).balanceOf(address(this)) - starting;
                    // Swap the premium for Illuminate principal tokens
                    swivelLendPremium(u, m, y, premium, premiumSlippage);
                }
```
`swivelLendPremium` [being](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L960):
```solidity
        // Lend remaining funds to Illuminate's Yield Space Pool
        uint256 swapped = yield(u, y, p, address(this), IMarketPlace(marketPlace).token(u, m, 0), slippageTolerance);
        // Mint the remaining tokens
        IERC5095(principalToken(u, m)).authMint(msg.sender, swapped);
```
And `yield` [doesn't take](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L943) protocol fees either. So the fees are lost from the premium.

## Tool used
Manual Review

## Recommendation
In the `if(e)` block of Swivel's `lend`, extract the protocol fee from `premium`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | kenzo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/45
- **Contest**: https://app.sherlock.xyz/audits/contests/12

### Keywords for Search

`vulnerability`

