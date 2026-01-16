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
solodit_id: 58105
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
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

[M-01] Redeem function active when vault is paused

### Overview


The report states that there is a bug in the vault's deposit, mint, and withdraw functions. These functions are supposed to be paused when the vault is paused, but the redeem function does not have this pause feature. This means that users can withdraw assets from the vault even when they shouldn't be able to. The report recommends adding the pause feature to the redeem function to fix this bug.

### Original Finding Content

## Severity

**Impact:** High - Allows unauthorized withdrawal of assets during critical situations when the vault is paused.

**Likelihood:** Low - This issue occurs only when the vault is in a paused state.

## Description

The vault's deposit, mint, and withdraw functionalities are halted when it is paused. This is implemented through the `whenNotPaused` modifier in the following functions:

        function deposit(
            uint256 _amount,
            address _receiver
        ) public whenNotPaused returns (uint256 shares) {

        function safeDeposit(
            uint256 _amount,
            uint256 _minShareAmount,
            address _receiver
        ) public whenNotPaused returns (uint256 shares) {

        function withdraw(
            uint256 _amount,
            address _receiver,
            address _owner
        ) external whenNotPaused returns (uint256) {

        function safeWithdraw(
            uint256 _amount,
            uint256 _minAmount,
            address _receiver,
            address _owner
        ) public whenNotPaused returns (uint256 amount) {

However, the redeem function is not pausable because the `whenNotPaused` modifier is not applied . This absence allows users to withdraw assets from the vaul when they should not.

        function redeem(
            uint256 _shares,
            address _receiver,
            address _owner
        ) external returns (uint256 assets) {

        function safeRedeem(
            uint256 _shares,
            uint256 _minAmountOut,
            address _receiver,
            address _owner
        ) external returns (uint256 assets) {

## Recommendations

Adding the whenNotPaused modifier to both the redeem and safeRedeem functions.

```diff
    function redeem(
        uint256 _shares,
        address _receiver,
        address _owner
-   ) external returns (uint256 assets) {
+   ) external whenNotPaused returns (uint256 assets) {
        return _withdraw(previewRedeem(_shares), _shares, _receiver, _owner);
    }

    function safeRedeem(
        uint256 _shares,
        uint256 _minAmountOut,
        address _receiver,
        address _owner
-    ) external returns (uint256 assets) {
+    ) external whenNotPaused returns (uint256 assets) {
        assets = _withdraw(
            previewRedeem(_shares),
            _shares, // _shares
            _receiver, // _receiver
            _owner // _owner
        );
        if (assets < _minAmountOut) revert AmountTooLow(assets);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

