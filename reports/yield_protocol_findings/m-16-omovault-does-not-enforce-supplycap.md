---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53346
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-16] OmoVault does not enforce supplyCap

### Overview


This bug report is about a contract called `OmoVault.sol` which has a state variable and a function that sets a limit on the amount of a certain asset that can be deposited or created. However, this limit is not being enforced in two important functions called `deposit()` and `mint()`. This means that the contract is not properly checking if the limit has been reached before allowing more assets to be added. The report recommends that this check be implemented in both functions to prevent the contract from being exploited.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `OmoVault.sol` contract has a `supplyCap` state variable and setter function, but this cap is not enforced in the `deposit()` or `mint()` functions.

```solidity
    function deposit(
        uint256 assets,
        address receiver
    ) public virtual override onlyWhitelisted returns (uint256 shares) {
        address msgSender = msg.sender;

        // Check for rounding error since we round down in previewDeposit.
        require((shares = _convertToShares(assets, false)) != 0, "ZERO_SHARES");
        // require(supplyCap >= totalAssets() + assets, "SUPPLY_CAP_EXCEEDED");
        // Need to transfer before minting or ERC777s could reenter.
        asset.safeTransferFrom(msgSender, address(this), assets);

        _totalAssets += assets;

        _mint(receiver, shares);

        emit Deposit(msgSender, receiver, assets, shares);
    }
```

```solidity
    function mint(
        uint256 shares,
        address receiver
    ) public virtual override onlyWhitelisted returns (uint256 assets) {
        address msgSender = msg.sender;

        assets = _convertToAssets(shares, true); // No need to check for rounding error, previewMint rounds up.

        // Need to transfer before minting or ERC777s could reenter.
        asset.safeTransferFrom(msgSender, address(this), assets);

        _totalAssets += assets;

        _mint(receiver, shares);

        emit Deposit(msgSender, receiver, assets, shares);
    }
```

## Recommendations

Implement the supply cap check in both `deposit()` and `mint()` functions

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

