---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17916
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

amoMinterBorrow cannot be paused

### Overview


This bug report is about an undefined behavior in the FraxPoolV3.sol smart contract. The amoMinterBorrow function does not check for any of the "paused" flags or whether the minter's associated collateral type is enabled. This reduces the FraxPoolV3 custodian's ability to limit the scope of an attack.

The exploit scenario is that Eve discovers and exploits a bug in an AMO contract. The FraxPoolV3 custodian discovers the attack but is unable to stop it, resulting in the FraxPoolV3 owner having to disable the AMO contracts after significant funds have been lost.

The recommendations are to require recollateralizePaused[minter_col_idx] to be false and collateralEnabled[minter_col_idx] to be true for a call to amoMinterBorrow to succeed, in order to limit the scope of an attack. Long-term, regularly review all uses of contract modifiers, such as collateralEnabled, to help expose bugs like the one described.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty: Medium

## Type: Undefined Behavior

## Target: FraxPoolV3.sol

### Description
The `amoMinterBorrow` function does not check for any of the “paused” flags or whether the minter’s associated collateral type is enabled. This reduces the FraxPoolV3 custodian’s ability to limit the scope of an attack.

The relevant code appears in figure 3.1. The custodian can set `recollateralizePaused[minter_col_idx]` to `true` if there is a problem with recollateralization, and `collateralEnabled[minter_col_idx]` to `false` if there is a problem with the specific collateral type. However, `amoMinterBorrow` checks for neither of these.

```solidity
// Bypasses the gassy mint->redeem cycle for AMOs to borrow collateral
function amoMinterBorrow(uint256 collateral_amount) external onlyAMOMinters {
    // Checks the col_idx of the minter as an additional safety check
    uint256 minter_col_idx = IFraxAMOMinter(msg.sender).col_idx();
    // Transfer
    TransferHelper.safeTransfer(collateral_addresses[minter_col_idx], msg.sender, collateral_amount);
}
```

*Figure 3.1: contracts/Frax/Pools/FraxPoolV3.sol#L552-L559*

### Exploit Scenario
Eve discovers and exploits a bug in an AMO contract. The FraxPoolV3 custodian discovers the attack but is unable to stop it. The FraxPoolV3 owner is required to disable the AMO contracts. This occurs after significant funds have been lost.

### Recommendations
- **Short term**: Require `recollateralizePaused[minter_col_idx]` to be `false` and `collateralEnabled[minter_col_idx]` to be `true` for a call to `amoMinterBorrow` to succeed. This will help the FraxPoolV3 custodian to limit the scope of an attack.
  
- **Long term**: Regularly review all uses of contract modifiers, such as `collateralEnabled`. Doing so will help to expose bugs like the one described here.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

