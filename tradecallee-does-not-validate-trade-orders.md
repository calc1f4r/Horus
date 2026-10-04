---
# Core Classification
protocol: Opyn Gamma Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18167
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
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
finders_count: 2
finders:
  - Dominik Teiml
  - Mike Martel
---

## Vulnerability Title

TradeCallee does not validate trade orders

### Overview


This bug report is about a vulnerability found in the TradeCallee contract of the Gamma Protocol. It allows an attacker to use the funds of a user, Alice, to execute an order signed by another individual, Eve. This is done by using the transaction origin (tx.origin) to specify the account of the trader, which transfers assets from the trader to the TradeCallee contract prior to the execution of the order. There is no subsequent validation to check if the order submitted to this function was signed by tx.origin.

To fix this issue, the developers should consider implementing a signature verification step before orders are forwarded to 0x from TradeCallee. This can be done by having tx.origin sign the data passed to callFunction or by using the provided signatures for orders to validate that they were signed by tx.origin. Alternatively, they can use the _sender parameter instead of the tx.origin validation to prevent attackers from transferring users’ funds.

In the long term, the developers should ensure that all proxy contracts have well-defined call conditions and means of verifying that those conditions are met.

### Original Finding Content

## Undefined Behavior

**Type:** Undefined Behavior  
**Target:** contracts/core/Controller.sol  

**Difficulty:** High  

## Description

The TradeCallee contract provides an interface that enables a Gamma Protocol user to transact with the 0x decentralized exchange. Users send orders by calling the `batchFillLimitOrders` function, which passes in signed orders that 0x then validates and processes. The transaction origin (`tx.origin`) is used to specify the account of the trader, which transfers assets from the trader to the TradeCallee contract prior to the execution of the order.

```solidity
require (
    tx.origin == trader,
    "TradeCallee: funds can only be transferred in from the person sending the transaction"
);

for (uint256 i = 0; i < orders.length; i++) {
    address takerAsset = orders[i].takerToken;
    ERC20Interface(takerAsset).safeTransferFrom(trader, address(this), takerTokenFillAmounts[i]);
    ERC20Interface(takerAsset).safeIncreaseAllowance(address(exchange), takerTokenFillAmounts[i]);
}
```

*Figure 2.1: The portion of callFunction that transfers assets from the tx.origin (without code comments).*

Since there is no subsequent validation that the order submitted to this function was signed by `tx.origin`, the funds may be transferred from the user and leveraged to execute an order signed by another individual.

## Exploit Scenario

Alice has preexisting approval to transfer assets to the TradeCallee contract to facilitate the purchase of assets using 0x. Eve, an attacker, creates a malicious proxy contract, which Alice then calls. The proxy contract calls the Controller, which calls TradeCallee. TradeCallee uses `tx.origin`’s funds (i.e., Alice’s funds) to perform a trade signed by Eve.

## Recommendations

**Short term:** Consider implementing a signature verification step that occurs before orders are forwarded to 0x from TradeCallee, either by having `tx.origin` sign the data passed to `callFunction` or by using the provided signatures for orders to validate that they were signed by `tx.origin`. Alternatively, use the `_sender` parameter instead of the `tx.origin` validation to prevent attackers from transferring users’ funds.

**Long term:** Ensure that all proxy contracts have well-defined call conditions and means of verifying that those conditions are met.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Opyn Gamma Protocol |
| Report Date | N/A |
| Finders | Dominik Teiml, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf

### Keywords for Search

`vulnerability`

