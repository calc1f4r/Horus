---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18020
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

No restrictions on minting to invalid recipients

### Overview

See description below for full details.

### Original Finding Content

## Patching Report

**Type:** Patching  
**Target:** LQTYToken.sol  

**Difficulty:** High  

## Description
Certain transfer restrictions imposed in the LUSD ERC20 token are not properly handled during the minting. The Liquity ERC20 contracts forbids any transfer to a special set of addresses specified in the `_requireValidRecipient` function:

```solidity
function _requireValidRecipient ( address _recipient ) internal view {
    require (
        _recipient != address ( 0 ) &&
        _recipient != address ( this ),
        "LUSD: Cannot transfer tokens directly to the LUSD token contract or the zero address"
    );
    require (
        _recipient != stabilityPoolAddress &&
        _recipient != troveManagerAddress &&
        _recipient != borrowerOperationsAddress,
        "LUSD: Cannot transfer tokens directly to the StabilityPool, TroveManager or BorrowerOps"
    );
}
```
*Figure 3.1: `_requireValidRecipient` in LUSDToken.sol*

However, this restriction doesn’t exist for `_mint`. This could lead to the minting of tokens to invalid recipient addresses.

```solidity
function _mint ( address account , uint256 amount ) internal {
    require (account != address ( 0 ), "ERC20: mint to the zero address" );
    _totalSupply = _totalSupply.add(amount);
    _balances[account] = _balances[account].add(amount);
    emit Transfer ( address ( 0 ), account, amount);
}
```
*Figure 3.2: `_mint` in LUSDToken.sol*

## Exploit Scenario
Alice adds a new feature to the Liquity protocol code. Adding the feature results in code flows where invalid recipient addresses can be passed into `_mint`. Then, tokens can be minted to an invalid recipient address.

## Recommendation
**Short term:** Add `_requireValidRecipient(account)` before any state-changing operations in `_mint`. This will prevent minting to invalid recipient addresses for any future code that calls `_mint`.

**Long term:** Use Manticore or Echidna to make sure important system properties hold.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Gustavo Grieco, Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf

### Keywords for Search

`vulnerability`

