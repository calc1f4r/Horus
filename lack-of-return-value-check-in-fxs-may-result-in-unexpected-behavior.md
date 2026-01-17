---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17887
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of return value check in FXS may result in unexpected behavior

### Overview

See description below for full details.

### Original Finding Content

## Type: Undefined Behavior
**Target:** truffle-config.js  

**Difficulty:** Low  

## Description
The FraxPool contract does not check the return value of a call to transfer FXS tokens. Without this check, the FRAX system may exhibit unexpected behavior.

The `collectRedemption` function calls FRAX’s ERC20 transfer function to transfer tokens from the pool to a user’s account:

```solidity
// After a redemption happens, transfer the newly minted FXS and owed
// collateral from this pool contract to the user. Redemption is split
// into two functions to prevent flash loans from being able
// to take out FRAX/collateral from the system, use an AMM to trade the new
// price, and then mint back into the system.
function collectRedemption() external {
    require((lastRedeemed[msg.sender].add(redemption_delay)) <= block.number,
    "Must wait for redemption_delay blocks before collecting redemption");
    bool sendFXS = false;
    bool sendCollateral = false;
    uint FXSAmount;
    uint CollateralAmount;
    [...]
    if (sendFXS == true) {
        FXS.transfer(msg.sender, FXSAmount);
    }
    if (sendCollateral == true) {
        collateral_token.transfer(msg.sender, CollateralAmount);
    }
}
```
_Figure 7.1: contracts/Frax/Pools/FraxPool.sol#L336-L369_

This transfer functionality is implemented in the ERC20Custom token contract:

```solidity
function _transfer(address sender, address recipient, uint256 amount) internal virtual {
    require(sender != address(0), "ERC20: transfer from the zero address");
    require(recipient != address(0), "ERC20: transfer to the zero address");
    _beforeTokenTransfer(sender, recipient, amount);
    _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
    _balances[recipient] = _balances[recipient].add(amount);
    emit Transfer(sender, recipient, amount);
}
```
_Figure 7.2: contracts/ERC20/ERC20Custom.sol#L159-L168_

The `_beforeTokenTransfer` hook is not currently used. If this function is used in the future, Frax Finance should ensure it reverts upon a failure.

## Exploit Scenario
Alice, a member of the Frax Finance team, adds a new functionality to the `_beforeTokenTransfer` hook that returns `false` upon failing. Neither the `_transfer()` function nor the pool checks for calls that return `false` when they fail. As a result, the failure is ignored, and the transfer still occurs.

## Recommendations
- **Short term:** Document the risks associated with adding functionalities to `_beforeTokenTransfer` to ensure that future refactors will not introduce unexpected behavior.
- **Long term:** Integrate Slither into the continuous integration pipeline to catch missing return value checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

