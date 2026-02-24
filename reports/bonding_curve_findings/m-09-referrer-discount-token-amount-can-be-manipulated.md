---
# Core Classification
protocol: Unlock Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1085
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-unlock-protocol-contest
source_link: https://code4rena.com/reports/2021-11-unlock
github_link: https://github.com/code-423n4/2021-11-unlock-findings/issues/155

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
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-09] Referrer discount token amount can be manipulated

### Overview


This bug report is about a vulnerability in the `Unlock.recordKeyPurchase` function. This function is called on each key purchase and mints UDT tokens to the referrer. The amount of tokens minted depends on the transaction's gas price, which is controlled by the caller (purchaser). This vulnerability means that tokens can be minted by purchasing a key with themself as the referrer at a high transaction gas price. Depending on the UDT price on external markets, it could be profitable to buy a key at a high gas price, receive UDT and then sell them on a market for a profit.

The recommended mitigation step is to declare an average gas price storage variable that is set by a trusted party and use this one instead of the user's gas price input. This would make the amount minted more predictable and would reduce the risk of exploit.

### Original Finding Content

_Submitted by cmichel_

The `Unlock.recordKeyPurchase` function is called on each key purchase (`MixinPurchase.purchase`) and mints UDT tokens to the referrer.
The amount to mint is based on the transaction's gas price which is controlled by the caller (purchaser):

```solidity
uint tokensToDistribute = (estimatedGasForPurchase * tx.gasprice) * (125 * 10 ** 18) / 100 / udtPrice;
```

#### Impact

Tokens can be minted by purchasing a key with themself as the referrer at a high transaction gas price.
Depending on the UDT price on external markets, it could be profitable to buy a key at a high gas price, receive UDT and then sell them on a market for a profit.

#### Recommended Mitigation Steps

The amount minted should be more predictable and not depend on the user's gas price input.
Consider declaring an *average gas price* storage variable that is set by a trusted party and use this one instead.

**[julien51 (Unlock Protocol) disagreed with severity and commented](https://github.com/code-423n4/2021-11-unlock-findings/issues/155#issuecomment-991691106):**
 > > Depending on the UDT price on external markets, it could be profitable to buy a key at a high gas price, receive UDT and then sell them on a market for a profit.
> 
> Since we get the token price from the Uniswap oracle, the amount of tokens received is always at most equal to what they would have spent to acquire them on Uniswap.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-11-unlock-findings/issues/155#issuecomment-1013842955):**
 > As the uniswap oracle provides averaged price data, if there is any discrepancy between the spot price and the TWAP price, this can definitely be abused to extract value from the protocol. Keeping this as `medium`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Unlock Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-unlock
- **GitHub**: https://github.com/code-423n4/2021-11-unlock-findings/issues/155
- **Contest**: https://code4rena.com/contests/2021-11-unlock-protocol-contest

### Keywords for Search

`vulnerability`

