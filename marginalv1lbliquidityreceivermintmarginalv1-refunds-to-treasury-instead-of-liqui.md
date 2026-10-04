---
# Core Classification
protocol: Marginal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40241
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a598d54-c212-4168-acb1-b13c5a08b204
source_link: https://cdn.cantina.xyz/reports/cantina_marginal_aug2024.pdf
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
  - Jeiwan
  - defsec
---

## Vulnerability Title

MarginalV1LBLiquidityReceiver.mintMarginalV1() refunds to treasury, instead of liquidity owner 

### Overview


The MarginalV1LBLiquidityReceiver.sol#L636 function is not properly refunding unspent funds to the correct address. Instead of refunding them to the address that deposited the initial liquidity in the LB pool and the receiver, the funds are being refunded to the treasury address. This can result in a significant amount of unused funds remaining in the receiver contract. To fix this, the function should be updated to refund the unspent funds to the correct address. This issue has been fixed in the MarginalV1LBLiquidityReceiver.mintMarginalV1() function in commit 6e992b68. 

### Original Finding Content

## MarginalV1LBLiquidityReceiver.sol Documentation

## Context
`MarginalV1LBLiquidityReceiver.sol#L636`

## Description
The `MarginalV1LBLiquidityReceiver.mintMarginalV1` function deposits funds as liquidity to a Marginal pool. At the end, the function refunds all unspent funds to the treasury address:

```solidity
// refund any left over unused amounts from uniswap v3 and marginal v1 mints
uint256 balance0 = balance(token0);
uint256 balance1 = balance(token1);
if (balance0 > 0)
    pay(token0, address(this), params.treasuryAddress, balance0);
if (balance1 > 0)
    pay(token1, address(this), params.treasuryAddress, balance1);
```

However, it should refund them to the address that deployed the LB pool, provided the initial liquidity and seeded the receiver. 

The amounts of tokens left in the receiver contract after minting liquidity in Marginal can be significant. Depositing to Uniswap (which is required to deposit to Marginal) and Marginal requires balanced liquidity, which depends on the current prices in the pools. Due to multiple factors (i.e., delayed depositing to Uniswap/Marginal, delayed LB pool finalization, partial initial liquidity swapping, etc...), the liquidity in the receiver contract can be balanced differently. As a result, depositing to Uniswap and Marginal will leave unused liquidity in the receiver.

## Recommendation
In the `MarginalV1LBLiquidityReceiver.mintMarginalV1()` function, consider refunding unspent tokens to the address that deposited the initial liquidity in the LB pool and the receiver.

## Marginal
Fixed in commit `6e992b68`. Added `address refundAddress` to receiver parameters in liquidity receiver. This is the address that then receives unspent receiver funds.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Marginal |
| Report Date | N/A |
| Finders | Jeiwan, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_marginal_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3a598d54-c212-4168-acb1-b13c5a08b204

### Keywords for Search

`vulnerability`

