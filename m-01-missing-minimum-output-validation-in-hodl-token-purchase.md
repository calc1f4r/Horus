---
# Core Classification
protocol: Terplayer Hodl
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57911
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Terplayer-Hodl-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-01] Missing Minimum Output Validation in HODL Token Purchase

### Overview


The HODL contract has a problem in the `_buyHodl()` function where it does not check the minimum amount of HODL tokens that users should receive when purchasing. This can result in users paying more than expected in a rising market. The issue is caused by the contract updating the HODL token price based on its balance, but not including a minimum output check. The team has acknowledged the issue and it is recommended to add a `minOut` parameter to let users set their minimum acceptable output. 

### Original Finding Content

## Severity

Medium Risk

## Description

The HODL contract contains an issue in the `_buyHodl()` function where it fails to validate the minimum amount of HODL tokens that users should receive when purchasing. This function is called internally by the public `buy()` function.

The issue occurs because the contract updates the HODL token price based on the contract's `beraBTC` balance after each transaction through the `safetyCheck()` function. This design enforces that the HODL price can only increase and never decrease:

```solidity
require(lastPrice <= newPrice, "The price of hodl cannot decrease");
lastPrice = newPrice;
```

However, the `_buyHodl()` function does not include a minimum output check (`minOut`) for the amount of HODL tokens to be received:

```solidity
function _buyHodl(uint256 BTC, address receiver, address inviter) internal {
    liquidate();
    require(receiver != address(0x0), "Reciever cannot be 0x0 address");
    require(BTC >= MIN, "Transaction amount must be above minimum");
    // Mint HODL to sender
    uint256 receiveHodl = getBuyAmount(BTC);
    beraBTC.safeTransferFrom(msg.sender, address(this), BTC);
    mint(receiver, receiveHodl);
    // Missing minOut validation here
    uint256 feeAddressAmount = (BTC * FEES_BUY) / FEE_BASE_10000;
    require(feeAddressAmount > MIN, "must trade over min");
    sendBTC(FEE_ADDRESS, feeAddressAmount);
    safetyCheck(BTC);
    emit Buy(msg.sender, receiver, inviter, BTC, receiveHodl);
}
```

For example, if a block has both a `donate()` and a `buy()` transaction, the order they're processed changes the outcome. If `donate` comes before `buy()`, the `buy()` gets less `HODL`—and vice versa. Users have no way to avoid this unpredictability.

## Location of Affected Code

File: [src/Hodl.sol](https://github.com/batoshidao/hodl/blob/b180fa8d03bdec56d4c6aea8c3f678428dd55429/src/Hodl.sol)

## Impact

Users can not set a max price they're willing to pay, so in a rising market, they might end up buying at a higher cost than expected.

## Recommendation

Add a `minOut` parameter to let users set their minimum acceptable output.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Terplayer Hodl |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Terplayer-Hodl-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

