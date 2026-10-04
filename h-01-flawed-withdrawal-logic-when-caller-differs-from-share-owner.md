---
# Core Classification
protocol: Blueberry_2025-03-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61469
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-26.md
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

[H-01] Flawed withdrawal logic when caller differs from share owner

### Overview


The report describes a bug in the HyperEvmVault code where the `previewWithdraw()` and `previewRedeem()` functions are not functioning correctly. These functions are supposed to allow users to preview the amount of funds they can withdraw, but they are currently using the wrong account to calculate the amount. This can cause accounting issues and even a denial of service. The recommendation is to fix the code so that the correct account is used for the calculations.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Withdrawals in HyperEvmVault have a custom behavior. Users need to first call `requestRedeem()` to move funds from L1 back to the EVM side. After this, available funds to be withdrawn are stored in the `redeemRequests` mapping.

These mechanics lead to a specialization of the `previewWithdraw()` and `previewRedeem()` functions. Instead of operating with the global supply or TVL values, these functions are implementended using the `redeemRequests` mapping:

```solidity
function previewWithdraw(uint256 assets_) public view override(ERC4626Upgradeable, IERC4626) returns (uint256) {
    V1Storage storage $ = _getV1Storage();
    RedeemRequest memory request = $.redeemRequests[msg.sender];
    return assets_.mulDivUp(request.shares, request.assets);
}

function previewRedeem(uint256 shares_) public view override(ERC4626Upgradeable, IERC4626) returns (uint256) {
    V1Storage storage $ = _getV1Storage();
    RedeemRequest memory request = $.redeemRequests[msg.sender];
    return shares_.mulDivDown(request.assets, request.shares);
}
```

Note that this forces the implementation to predicate over an account, which is chosen here to be `msg.sender`.

Withdrawals in ERC4626 also support a flow in which the caller could be different from the owner of the shares, leveraging ERC20 approvals. While this is correctly implemented in the overridden version of `_withdraw()`, the implementation still uses the preview functions that operate on `msg.sender`. This means that conversion will be calculated using the caller balances, but balances will be modified for the owner account, leading to accounting issues and a potential denial of service.

## Recommendations

Override the implementations of `withdraw()` and `redeem()` so that the `previewWithdraw()` and `previewRedeem()` actions execute the conversion on the owner (i.e. by using `$.redeemRequests[owner]`).





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-03-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

