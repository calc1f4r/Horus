---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6328
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/507

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xA5DF
  - bin2chen
  - 0x52
  - hansfriese
---

## Vulnerability Title

[H-09] Users can bypass the maxWinPercent limit using a partially closing

### Overview


This bug report concerns the code found in the Trading.sol file of the 2022-12-tigris repository on Github. It states that users can bypass the `maxWinPercent` limit set by the protocol with a partial closing. This means that the user can receive more funds than their upper limit from the protocol.

The bug is demonstrated by the following scenario: Alice opens an order with a margin of 100 and PnL of 1000. With a `maxWinPercent` of 500%, Alice should receive a maximum of 500. However, if Alice closes 50% of the position, she can receive 500 for a 50% margin because the `maxWinPercent` is checked with the `_toMint = 500` and `_trade.margin = 100`. This can be repeated, allowing Alice to withdraw almost 100% of the initial PnL (1000) even though she should only receive 500.

The bug was found through manual review. The recommended mitigation step is to check the `maxWinPercent` between the partial payout and partial margin. This can be done by adding the line `uint256 partialMarginToClose = _trade.margin * _percent / DIVISION_CONSTANT;` and changing the if statement to `if (maxWinPercent > 0 && _toMint > partialMarginToClose*maxWinPercent/DIVISION_CONSTANT) {`.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/b2ebb8ea1def4927a747e7a185174892506540ab/contracts/Trading.sol#L625-L627


## Vulnerability details

## Impact
Users can bypass the `maxWinPercent` limit using a partial closing.

As a result, users can receive more funds than their upper limit from the protocol.

## Proof of Concept
As we can see from the [documentation](https://docs.tigris.trade/protocol/trading-and-fees#limitations), there is limitation of a maximum PnL.

```
Maximum PnL is +500%. The trade won't be closed unless the user sets a Take Profit order or closes the position manually.
```

And this logic was implemented like below in `_closePosition()`.

```solidity
File: 2022-12-tigris\contracts\Trading.sol
624:                 _toMint = _handleCloseFees(_trade.asset, uint256(_payout)*_percent/DIVISION_CONSTANT, _trade.tigAsset, _positionSize*_percent/DIVISION_CONSTANT, _trade.trader, _isBot);
625:                 if (maxWinPercent > 0 && _toMint > _trade.margin*maxWinPercent/DIVISION_CONSTANT) { //@audit bypass limit
626:                     _toMint = _trade.margin*maxWinPercent/DIVISION_CONSTANT;
627:                 }
```

But it checks the `maxWinPercent` between the partial payout and full margin so the below scenario is possible.

1. Alice opened an order of margin = 100 and PnL = 1000 after taking closing fees.
2. If `maxWinPercent` = 500%, Alice should receive 500 at most.
3. But Alice closed 50% of the position and she got 500 for a 50% margin because it checks `maxWinPercent` with `_toMint = 500` and `_trade.margin = 100`
4. After she closed 50% of the position, the remaining margin = 50 and PnL = 500 so she can continue step 3 again and again.
5. As a result, she can withdraw almost 100% of the initial PnL(1000) even though she should receive at most 500.

## Tools Used
Manual Review

## Recommended Mitigation Steps
We should check the `maxWinPercent` between the partial payout and partial margin like below.

```solidity
    _toMint = _handleCloseFees(_trade.asset, uint256(_payout)*_percent/DIVISION_CONSTANT, _trade.tigAsset, _positionSize*_percent/DIVISION_CONSTANT, _trade.trader, _isBot);

    uint256 partialMarginToClose = _trade.margin * _percent / DIVISION_CONSTANT; //+++++++++++++++++++++++
    if (maxWinPercent > 0 && _toMint > partialMarginToClose*maxWinPercent/DIVISION_CONSTANT) { 
        _toMint = partialMarginToClose*maxWinPercent/DIVISION_CONSTANT;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | 0xA5DF, bin2chen, 0x52, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/507
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

