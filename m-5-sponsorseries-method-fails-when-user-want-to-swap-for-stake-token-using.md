---
# Core Classification
protocol: Sense Update #1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8726
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/58
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-sense-judging/issues/36

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - spyrosonic10
---

## Vulnerability Title

M-5: sponsorSeries() method fails when user want to swap for stake token using

### Overview


A bug was found in the `sponsorSeries()` method of the `Periphery.sol` contract. The `sponsorSeries()` method fails when users want to use `swapQuote` to swap for stake token to sponsor a series. The code that does the transferFrom() of the stakeToken does not use the sellToken, which causes the method to fail. This bug has an impact on the ability of users to sponsor a series, as they cannot swap for the stake token. 

The bug was found manually by spyrosonic10 and the code snippet can be found at https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L116-L128. The recommendation is to implement functionality to transferFrom the sellToken from the msg.sender with the actual amount that is required to get the exact amountOut greater or equal to the stakeSize.

The discussion on the bug report suggested that the statement in the bug report was not quite accurate. The problem was that the wrong params were sent to the _transferFrom. If the permit feature was used, it would have worked, but if the traditional approval was used, it would fail since the stake was not approved by the user. The fix proposed was to change the code to use the quote.sellToken and quote.amount.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-sense-judging/issues/36 

## Found by 
spyrosonic10

## Summary
`sponsorSeries()` fails when user want to use `swapQuote` to swap for stake token to sponsor a series.

## Vulnerability Detail
stake is token that user need to deposit (technically is pulled) to be able to sponsor a series for a given target.  User has option to send `SwapQuote calldata quote` and swap any ERC20 token for stake token.  Below is the code that doing transferFrom() of stakeToken not sellToken()

```solidity
if (address(quote.sellToken) != ETH) _transferFrom(permit, stake, stakeSize);
 if (address(quote.sellToken) != stake) _fillQuote(quote);
```
Expected behaviour of this function is to pull `sellToken` from msg.sender when `address(quote.sellToken) != stake`. For example- stake token is WETH. User want to swap DAI for WETH in `sponsorSeries()`. In this case, user would be sending SwapQuote.sellToken = DAI and swapQuote.buyToke = WETH and expect that fillQuote() would swap it for WETH. This method will fail because sellToken not transferred from msg.sender.
## Impact
sponsorSeries() fails when `address(quote.sellToken) != stake`

## Code Snippet
https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L116-L128

## Tool used

Manual Review

## Recommendation
Consider implementation of functionality to transferFrom `sellToken` from msg.sender with actual amount that is require to get exact amountOut greater or equal to `stakeSize`

## Discussion

**jparklev**

Accepted:

This bug is valid but the below statement

> `sponsorSeries()` fails when user want to use `swapQuote` to swap for stake token to sponsor a series.
> 

is not quite accurate.

The problem here is that here:

```solidity
if (address(quote.sellToken) != ETH) _transferFrom(permit, stake, stakeSize);
```

we are sending wrong params to `_transferFrom`.

If we are making use of the `permit` feature, this would work fine because the `_transferFrom` **ignores** the params on that case.

On the contrary, if we want to make use of the traditional approval, this would revert since we will be trying to pull a the `stake` which has not been approved by the user.

**Fix:**  

```solidity
if (address(quote.sellToken) != ETH) _transferFrom(permit, quote.sellToken, quote.amount);
// quote.amount does not exist so we may need to add this param to the struct
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Sense Update #1 |
| Report Date | N/A |
| Finders | spyrosonic10 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-sense-judging/issues/36
- **Contest**: https://app.sherlock.xyz/audits/contests/58

### Keywords for Search

`vulnerability`

