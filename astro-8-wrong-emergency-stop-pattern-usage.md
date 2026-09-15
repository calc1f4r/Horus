---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62369
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-17-Astrolab.md
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
  - Hexens
---

## Vulnerability Title

[ASTRO-8] Wrong Emergency Stop pattern usage

### Overview


This bug report is about a contract called `Crate.sol` that has an Emergency Stop pattern. However, some functions in the contract do not have proper checks to stop their usage when the owner has paused the contract. This means that users can still withdraw or redeem funds even when the contract is supposed to be paused. To fix this, the `whenNotPaused` modifier should be added to the `safeWithdraw()`, `redeem()`, and `safeRedeem()` functions. This issue has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** Crate.sol

**Description:** The contract  `Crate.sol` provides an Emergency Stop pattern, but some functions don’t have any checks to halt their usage, so users can withdraw or redeem after the owner has paused the contract. 
```
function safeWithdraw(
        uint256 _amount,
        uint256 _minAmount,
        uint256 _deadline,
        address _receiver,
        address _owner
    ) external returns (uint256 shares) {
        // This represents the amount of crTokens that we're about to burn
        shares = convertToShares(_amount);
        _withdraw(_amount, shares, _minAmount, _deadline, _receiver, _owner);
    }
```
```
function redeem(
        uint256 _shares,
        address _receiver,
        address _owner
    ) external returns (uint256 assets) {
        return (
            _withdraw(
                convertToAssets(_shares),
                _shares,
                0,
                block.timestamp,
                _receiver,
                _owner
            )
        );
    }
```
```
function safeRedeem(
        uint256 _shares,
        uint256 _minAmountOut, // Min_amount
        uint256 _deadline,
        address _receiver,
        address _owner
    ) external returns (uint256 assets) {
        return (
            _withdraw(
                convertToAssets(_shares), // _amount
                _shares, // _shares
                _minAmountOut,
                _deadline,
                _receiver, // _receiver
                _owner // _owner
            )
        );
    }
```

**Remediation:**  Use `whenNotPaused` modifier for `safeWithdraw()`, `redeem()`, and `safeRedeem() `functions.

**Status:**   Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-17-Astrolab.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

