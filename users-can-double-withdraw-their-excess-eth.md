---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40749
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7cb70b9d-62b1-48c3-9b28-a9eb95d2dc40
source_link: https://cdn.cantina.xyz/reports/cantina_coinbase_magicspend_feb2024.pdf
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
  - Riley Holterhus
  - RustyRabbit
---

## Vulnerability Title

Users can double withdraw their excess ETH 

### Overview


The MagicSpend contract has a bug where the _gasMaxCostExcess mapping is not being reset to zero after a user withdraws their excess ETH. This allows an attacker to drain all ETH from the contract by repeatedly withdrawing large excesses. The recommendation is to add a delete statement in the postOp() function to reset the mapping. This bug has been fixed in PR 3 and has been verified by Cantina Managed. This is an informational report.

### Original Finding Content

## MagicSpend Contract Analysis

## Context
MagicSpend.sol#L74-L91

## Description
When the MagicSpend contract is used as an ERC-4337 compatible paymaster, the user's `withdrawRequest` is used to cover the `UserOp`'s gas fees, and any excess withdrawn ETH is recorded in the `_gasMaxCostExcess` mapping. 

When the user's transaction later executes, they have the option to either claim this excess immediately using the `withdrawGasExcess()` function or wait for the ERC-4337 `postOp()` function to refund it automatically. In either scenario, the `_gasMaxCostExcess` mapping should ultimately be reset to zero since the user has received their excess ETH withdrawal.

However, this is currently not the case, as the `postOp()` function does not reset the `_gasMaxCostExcess` mapping. This means that a user can receive their excess once in the `postOp()` function and again by calling `withdrawGasExcess()` in a subsequent transaction. By using multiple withdrawals with large excesses, an attacker can exploit this bug to drain all ETH in the MagicSpend contract.

## Recommendation
Add a delete statement in the `postOp()` function:

```solidity
function postOp(IPaymaster.PostOpMode mode, bytes calldata context, uint256 actualGasCost)
external
onlyEntryPoint
{
    if (mode == IPaymaster.PostOpMode.postOpReverted) {
        return;
    }
    (uint256 withheld, address account) = abi.decode(context, (uint256, address));
    
    // Credit user difference between actual and withheld
    // and unwithdrawn excess
    uint256 excess = _gasMaxCostExcess[account] + (withheld - actualGasCost);
    delete _gasMaxCostExcess[account]; // Reset the mapping
    
    if (excess > 0) {
        _withdraw(address(0), account, excess);
    }
}
```

## Base
Fixed in PR 3.

## Cantina Managed
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | Riley Holterhus, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_coinbase_magicspend_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7cb70b9d-62b1-48c3-9b28-a9eb95d2dc40

### Keywords for Search

`vulnerability`

