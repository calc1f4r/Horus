---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40223
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
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
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Various small improvements and other nitpicks 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context
- `AaveV3Pocket.sol#L33`
- `AaveV3Pocket.sol#L4`
- `BasePocket.sol#L108-L116`
- `DeployTCAP.s.sol#L11`
- `DeployTCAP.s.sol#L42`
- `DeployTCAP.s.sol#L5`
- `FeeCalculatorLib.sol#L4`
- `IOracle.sol#L17-L18`
- `LiquidationLib.sol#L4`
- `Vault.sol#L141`
- `Vault.sol#L162-L164`
- `Vault.sol#L247`
- `Vault.sol#L263`
- `Vault.sol#L330`

## Description
During the code review, a variety of smaller changes with the goal of improving readability and following general best practices were suggested.

## Recommendations
Fix those highlighted nitpicks. These are some of the more noteworthy findings:

- **Vault.sol**: Although there is no apparent issue with specifying zero amounts when interacting with the Vault contract (Deposit, Withdrawal, Minting, or Burning), it's still one of those extreme cases where one could consider "failing early" to ensure nothing weird can happen down the line. Consider explicit checks against 0 amounts that wouldn’t have any desirable effect anyway.
    ```solidity
    function deposit(uint96 pocketId, uint256 amount) external returns (uint256 shares) {
        require(amount > 0);
        // ...
    }
    ```

- **Vault.sol**: Functions that should still function normally for disabled pockets (such as `withdraw()`) won't call `_getPocket()` and therefore also skip over its implicit sanity check on whether that pocket exists at all. Consider validating `pocketId` parameters of external functions by requiring the pocket's address to be non-zero.
    ```solidity
    function withdraw(uint96 pocketId, uint256 amount, address to) external ensureLoanHealthy(msg.sender, pocketId) returns (uint256 shares) {
        // @audit should be able to withdraw even if pocket is disabled
        IPocket pocket = _getVaultStorage().pockets[pocketId].pocket;
        require(address(pocket) != address(0x0));
    }
    ```

- **AaveV3Pocket.sol**: The `_balanceOf()` function of `AaveV3Pocket.sol` is lacking a check to prevent division-by-zero which the `_balanceOf()` function from `BasePocket.sol` has which is being overridden. Consider adding this check here as well for consistency:
    ```solidity
    function _balanceOf(address user) internal view override returns (uint256) {
        uint256 totalShares_ = totalShares();
        if (totalShares_ == 0) return 0;
        return sharesOf(user) * OVERLYING_TOKEN.balanceOf(address(this)) / totalShares_;
    }
    ```

- **BasePocket.sol**: In `_balanceOf()` and `_totalBalance()`, the balance of `OVERLYING_TOKEN` should be used instead of `UNDERLYING_TOKEN`. This is because by design, the Pocket holds `OVERLYING_TOKEN` tokens. Although not being an issue, since `BasePocket` has `OVERLYING_TOKEN == UNDERLYING_TOKEN` and `AaveV3Pocket` is already implemented correctly, consider adjusting this for consistency.
    ```solidity
    function _balanceOf(address user) internal view virtual returns (uint256) {
        uint256 totalShares_ = totalShares();
        if (totalShares_ == 0) return 0;
        return sharesOf(user) * OVERLYING_TOKEN.balanceOf(address(this)) / totalShares_;
    }

    function _totalBalance() internal view virtual returns (uint256) {
        return OVERLYING_TOKEN.balanceOf(address(this));
    }
    ```

## Cryptex
As none of these have any significant impact on the protocol's security, the Cryptex Team addressed some of these findings at their own discretion:
- PR 9.
- PR 11.
- PR 13.
- Commit d1799f6e.
- Commit 3ef6bd16.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

