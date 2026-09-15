---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: refund_ether

# Attack Vector Details
attack_type: refund_ether
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3323
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/98

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - refund_ether

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - lemonmon
---

## Vulnerability Title

H-3: `TradingUtils::_executeTrade` will leak ETH to WETH

### Overview


This bug report involves an issue with the TradingUtils::_executeTrade function in the leveraged-vaults contracts of the 2022-09-notional repository on Github. The issue is that if the sellToken is ETH and using Uniswap as the dex, too much ETH will be deposited to the WETH and not withdrawn, resulting in a wrong amountSold value and accounting error. 

The bug was found by lemonmon and the code snippet can be found at the provided link. The impact of the bug is that amountSold will not reflect the real amount sold, rather the trade.limit, and it is unclear whether the excess amount of ETH deposited can be recovered.

The bug was discussed by jeffywu and weitianjie2000, with the latter confirming it is a legitimate issue that will be fixed. The recommendation is that if the sellToken is ETH and it is an exact out trade, the excess deposit should be recovered in the _executeTrade function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/98 

## Found by 
lemonmon

## Summary

If sellToken is ETH, and using Uniswap for the dex, and it is exact out trade, too much is deposited to the WETH and does not withdraw the excess amount. It will give wrong `amountSold` value as well as accounting error.

## Vulnerability Detail

`trade.sellToken` is ETH and using Uniswap as dex, WETH should be used instead of ETH as Uniswap does not support ETH. There for TradingUtils wraps the ETH to WETH before trading.

If the trade would be exact out, the amount `trade.limit` will be deposited to WETH instead of the `trade.amount`. However, because it is exact out, not all ETH deposited will be traded. In the current implementation, there is no logic to recover the excess deposit.

As the `TradingUtils::_executeInternal`, which uses the `TradingUtils::_executeTrade` will calculate the `amountSold` based on the balance of ETH, it will return the `trade.limit` as the `amountSold`, thus resulting in accounting error.

Note: in the current implementation, the trade using Uniswap with ETH as sellToken would not even work, because the WETH is not properly approved (issue 2). This issue assumes that the issue is resolved. 

## Impact

`amountSold` will reflect not the amount really sold, rather the `trade.limit`. It is unclear whether the excess amount of ETH, which is deposited for WETH can be recovered.

## Code Snippet

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol?plain=1#L118-L137

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol?plain=1#L29-L64


## Tool used

Manual Review

## Recommendation

In the `_executeTrade`, if the sellToken is ETH and it is exact out trade, recover excess deposit.


## Discussion

**jeffywu**

@Evert0x I don't think this is a duplicate of #110

**weitianjie2000**

legit issue, will be fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | lemonmon |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/98
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`Refund Ether`

