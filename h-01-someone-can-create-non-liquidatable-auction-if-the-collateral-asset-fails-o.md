---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: weird_erc20

# Attack Vector Details
attack_type: weird_erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3083
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-yield-witch-v2-contest
source_link: https://code4rena.com/reports/2022-07-yield
github_link: https://github.com/code-423n4/2022-07-yield-findings/issues/116

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - weird_erc20
  - erc20

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - antonttc
  - 0x52
---

## Vulnerability Title

[H-01]  Someone can create non-liquidatable auction if the collateral asset fails on transferring to address(0)

### Overview


This bug report describes a vulnerability in the Witch contract code on the 2022-07-yield repository on GitHub. This vulnerability might lead to systematic debt and cause errors for liquidators to run normally. The vulnerability is caused by an absence of input validation when starting an auction. If an auction is started with the 'to' parameter set to 'address(0)', the auction is un-liquidatable and a malicious user can avoid liquidation of their own vault. The recommended mitigation step is to add a check while starting an auction to ensure that the 'to' parameter is not set to 'address(0)'.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-07-yield/blob/main/contracts/Witch.sol#L176
https://github.com/code-423n4/2022-07-yield/blob/6ab092b8c10e4dabb470918ae15c6451c861655f/contracts/Witch.sol#L399


## Vulnerability details

## Impact
might lead to systematic debt. Cause errors for liquidators to run normally.

## Proof of Concept
In the function `auction`, there is on input validation around whether the `to` is `address(0)` or not. and if the `auctioneerReward` is set to an value > 0 (as default),  each liquidate call will call `Join` module to pay out to `auctioneer` with the following line:

```jsx
if (auctioneerCut > 0) {
    ilkJoin.exit(auction_.auctioneer, auctioneerCut.u128());
}
```

This line will revert if `auctioneer` is set to `address(0)` on some tokens (revert on transferring to address(0) is a [default behaviour of the OpenZeppelin template](https://www.notion.so/Yield-Witch-555e6981c26b41008d03a504077b4770)). So if someone start an `auction` with `to = address(0)`, this auction becomes un-liquidatable.

A malicious user can run a bot to monitor his own vault, and if the got underwater and they don’t have enough collateral to top up, they can immediately start an auction on their own vault and set actioneer to `0` to avoid actually being liquidated, which breaks the design of the system.


## Recommended Mitigation Steps

Add check while starting an auction:

```jsx
function auction(bytes12 vaultId, address to)
    external
    returns (DataTypes.Auction memory auction_)
{
    require (to != address(0), "invalid auctioneer");
		...
}		
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | antonttc, 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-yield
- **GitHub**: https://github.com/code-423n4/2022-07-yield-findings/issues/116
- **Contest**: https://code4rena.com/contests/2022-07-yield-witch-v2-contest

### Keywords for Search

`Weird ERC20, ERC20`

