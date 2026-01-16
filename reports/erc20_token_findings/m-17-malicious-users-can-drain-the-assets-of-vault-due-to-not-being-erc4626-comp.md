---
# Core Classification
protocol: Popcorn
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22014
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/471

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 2

# Context Tags
tags:
  - rounding
  - eip-4626
  - erc4626

protocol_categories:
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - fs0c
  - bin2chen
  - ladboy233
  - koxuan
  - rvi0x
---

## Vulnerability Title

[M-17] Malicious Users Can Drain The Assets Of Vault. (Due to not being ERC4626 Complaint)

### Overview


A bug has been found in the `withdraw` function of a vault, which allows malicious users to drain the assets of the vault without burning their shares. The bug is caused by the use of `Math.Rounding.Down` instead of `Math.Rounding.Up` in the `convertToShares` function. 

To illustrate the issue, assume the vault has 1000 WETH in total assets and 10 shares in total supply. If Alice wants to withdraw 99 WETH from the vault by calling the `Vault.withdraw(99 WETH)` function, the calculation would be: `99 * 10 / 1000 = 0`, and the value would be rounded down to zero. This means that the amount of shares burned from Alice's account would be zero, allowing her to drain the assets from the vault without burning her shares.

A similar issue also exists in the `mint` functionality, where `Math.Rounding.Down` is used and `Math.Rounding.Up` should be used. To fix this issue, the following rounding methods should be used: `deposit` → `convertToShares` → `Math.Rounding.Down`; `mint` → `converttoAssets` → `Math.Rounding.Up`; `withdraw` → `convertToShares` → `Math.Rounding.Up`; `redeem` → `convertToAssets` →  `Math.Rounding.Down`. The bug has been confirmed by RedVeil (Popcorn) and the severity has been decreased to Medium by LSDan (judge).

### Original Finding Content


Malicious users can drain the assets of the vault.

### Proof of Concept

The `withdraw` function users `convertToShares` to convert the assets to the amount of shares. These shares are burned from the users account and the assets are returned to the user.

The function `withdraw` is shown below:

```solidity
function withdraw(
        uint256 assets,
        address receiver,
        address owner
    ) public nonReentrant syncFeeCheckpoint returns (uint256 shares) {
        if (receiver == address(0)) revert InvalidReceiver();

        shares = convertToShares(assets);
/// .... [skipped the code]
```

The function `convertToShares` is shown below:

```solidity
function convertToShares(uint256 assets) public view returns (uint256) {
        uint256 supply = totalSupply(); // Saves an extra SLOAD if totalSupply is non-zero.

        return
            supply == 0
                ? assets
                : assets.mulDiv(supply, totalAssets(), Math.Rounding.Down);
    }
```

It uses `Math.Rounding.Down` , but it should use `Math.Rounding.Up`

Assume that the vault with the following state:

*   Total Asset = 1000 WETH
*   Total Supply = 10 shares

Assume that Alice wants to withdraw 99 WETH from the vault. Thus, she calls the **`Vault.withdraw(99 WETH)`** function.

The calculation would go like this:

```solidity
assets = 99
return value = assets * supply / totalAssets()
return value = 99 * 10 / 1000
return value = 0
```

The value would be rounded round to zero. This will be the amount of shares burned from users account, which is zero.

Hence user can drain the assets from the vault without burning their shares.

> Note : A similar issue also exists in `mint` functionality where `Math.Rounding.Down` is used and `Math.Rounding.Up` should be used.

### Recommended Mitigation Steps

Use `Math.Rounding.Up` instead of `Math.Rounding.Down`.

As per OZ implementation here is the rounding method that should be used:

`deposit` : `convertToShares` → `Math.Rounding.Down`

`mint` : `converttoAssets` → `Math.Rounding.Up`

`withdraw` : `convertToShares` → `Math.Rounding.Up`

`redeem` : `convertToAssets` →  `Math.Rounding.Down`

**[RedVeil (Popcorn) confirmed, but disagreed with severity](https://github.com/code-423n4/2023-01-popcorn-findings/issues/471)** 

**[LSDan (judge) decreased severity to Medium](https://github.com/code-423n4/2023-01-popcorn-findings/issues/471)** 


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | fs0c, bin2chen, ladboy233, koxuan, rvi0x, 0xmuxyz, nadin, DadeKuma, rvierdiiev, Kumpa |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/471
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`Rounding, EIP-4626, ERC4626`

