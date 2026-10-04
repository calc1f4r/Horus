---
# Core Classification
protocol: Perpetual Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18251
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/PerpetualProtocolV2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/PerpetualProtocolV2.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Paweł Płatek
  - Michael Colburn
---

## Vulnerability Title

Lack of zero-value checks on functions Status: Unresolved

### Overview

See description below for full details.

### Original Finding Content

## Perpetual Protocol V2 Retest Report

**Difficulty:** High  
**Type:** Undefined Behavior  
**Target:** ClearingHouseCallee.sol, OrderBook.sol  

## Description
The `ClearingHouseCallee` contract's `setClearingHouse` function and the `OrderBook` contract's `setExchange` function fail to validate some of their incoming arguments, so callers can accidentally set important state variables to the zero address.

### Function: setClearingHouse
```solidity
function setClearingHouse(address clearingHouseArg) external onlyOwner {
    _clearingHouse = clearingHouseArg;
    emit ClearingHouseChanged(clearingHouseArg);
}
```
*Figure 1.1: Missing zero-value check*  
*(perp-lushan/contracts/base/ClearingHouseCallee.sol#30–33)*

### Function: setExchange
```solidity
function setExchange(address exchangeArg) external onlyOwner {
    _exchange = exchangeArg;
    emit ExchangeChanged(exchangeArg);
}
```
*Figure 1.2: Missing zero-value check*  
*(perp-lushan/contracts/OrderBook.sol#93–96)*  

## Fix Analysis
The Perpetual Finance team acknowledged the issue and decided to postpone the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Perpetual Protocol V2 |
| Report Date | N/A |
| Finders | Paweł Płatek, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/PerpetualProtocolV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/PerpetualProtocolV2.pdf

### Keywords for Search

`vulnerability`

