---
# Core Classification
protocol: Origin Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18208
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/OriginDollar.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/OriginDollar.pdf
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
  - Dominik Teiml
  - Alexander Remie
---

## Vulnerability Title

VaultCore.rebase functions have no return statements

### Overview

See description below for full details.

### Original Finding Content

## Type: Undefined Behavior

**Target**: OpenUniswapOracle.sol, IPriceOracle.sol, ChainlinkOracle.sol, RebaseHooks.sol, IRebaseHooks.sol

**Difficulty**: Low

## Description

`VaultCore.rebase()` and `VaultCore.rebase(bool)` return a `uint` but lack a return statement. As a result, these functions will always return the default value and are likely to cause issues for their callers. Both `VaultCore.rebase()` and `VaultCore.rebase(bool)` are expected to return a `uint256`:

```solidity
/**
 *  @dev Calculate the total value of assets held by the Vault and all
 *       strategies and update the supply of oUSD
 */
function rebase() public whenNotRebasePaused returns (uint256) {
    rebase(true);
}

/**
 *  @dev Calculate the total value of assets held by the Vault and all
 *       strategies and update the supply of oUSD
 */
function rebase(bool sync) internal whenNotRebasePaused returns (uint256) {
    if (oUSD.totalSupply() == 0) return 0;
    uint256 oldTotalSupply = oUSD.totalSupply();
    uint256 newTotalSupply = _totalValue();
    // Only rachet upwards
    if (newTotalSupply > oldTotalSupply) {
        oUSD.changeSupply(newTotalSupply);
        if (rebaseHooksAddr != address(0)) {
            IRebaseHooks(rebaseHooksAddr).postRebase(sync);
        }
    }
}
```

`rebase()` does not have a return statement. `rebase(bool)` has one return statement in one branch (return 0), but lacks a return statement for the other paths. So both functions will always return zero. As a result, third-party code relying on the return value might not work as intended.

## Exploit Scenario

Bob’s smart contract uses `rebase()`. Bob assumes that the value returned is the amount of assets rebased. His contract checks that the return value is always greater than zero. Since this function always returns 0, Bob’s contract does not work.

## Recommendation

Short term, add the missing return statement(s) or remove the return type in `VaultCore.rebase()` and `VaultCore.rebase(bool)`. Properly adjust the documentation as necessary.

Long term, use Slither or subscribe to Crytic.io to detect when functions are missing appropriate return statements. Crytic catches this bug type.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Origin Dollar |
| Report Date | N/A |
| Finders | Dominik Teiml, Alexander Remie |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/OriginDollar.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/OriginDollar.pdf

### Keywords for Search

`vulnerability`

