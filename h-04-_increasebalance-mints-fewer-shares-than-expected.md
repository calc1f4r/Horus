---
# Core Classification
protocol: Karak-June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38492
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] `_increaseBalance()` mints fewer shares than expected

### Overview


The bug report describes a problem in a function called `NativeVault._increaseBalance` which is used to increase the balance of a node owner. The problem occurs because the order of operations in the function is incorrect, causing the number of shares received by the owner to be lower than it should be. A proof of concept is provided to show how this bug results in the owner losing 10.67 ETH. The report recommends a simple fix to correct the order of operations in the function.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

To increase the balance of a node owner, the `NativeVault._increaseBalance` function is called. This function increases the total assets, calculates the shares to be minted, mints the shares for the node owner, and updates the `totalRestakedETH` of the node owner.

However, the order of the operations is not correct, as updating the `totalAssets` before the calculation of the shares to be minted causes the number of shares received to be lower than it should be.

```solidity
File: NativeVault.sol

    function _increaseBalance(address _of, uint256 assets) internal {
        NativeVaultLib.Storage storage self = _state();
        if (assets + self.totalAssets > maxDeposit(_of)) revert DepositMoreThanMax();
 @>     self.totalAssets += assets;
        uint256 shares = convertToShares(assets);
        _mint(_of, shares);
        self.ownerToNode[_of].totalRestakedETH += assets;
        emit IncreasedBalance(self.ownerToNode[_of].totalRestakedETH);
    }
```

## Proof of concept

The state of the vault is as follows:

- totalAssets: 32 ETH
- totalSupply: 32e18
- exchange rate: 1:1

Alice's balance is increased by 32 ETH, so she should receive 32e18 shares. But this is not the case. The calculation is as follows:

- totalAssets = 32 ETH + 32 ETH = 64 ETH
- shares = assets _ totalSupply / totalAssets = 32 ETH _ 32e18 / 64 ETH = 16e18
- totalSupply = 32e18 + 16e18 = 48e18

Alice receives 16e18 shares. Converting them to assets we have:

- assets = shares _ totalAssets / totalSupply = 16e18 _ 64 ETH / 48e18 = 21.33 ETH

Alice has lost 10.67 ETH.

## Recommendations

```diff
    function _increaseBalance(address _of, uint256 assets) internal {
        NativeVaultLib.Storage storage self = _state();
        if (assets + self.totalAssets > maxDeposit(_of)) revert DepositMoreThanMax();
-       self.totalAssets += assets;
        uint256 shares = convertToShares(assets);
        _mint(_of, shares);
+       self.totalAssets += assets;
        self.ownerToNode[_of].totalRestakedETH += assets;
        emit IncreasedBalance(self.ownerToNode[_of].totalRestakedETH);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Karak-June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

