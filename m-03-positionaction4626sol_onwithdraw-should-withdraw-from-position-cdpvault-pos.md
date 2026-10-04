---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49115
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-loopfi
source_link: https://code4rena.com/reports/2024-10-loopfi
github_link: https://github.com/code-423n4/2024-10-loopfi-findings/issues/13

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
  - pkqs90
---

## Vulnerability Title

[M-03] `PositionAction4626.sol#_onWithdraw` should withdraw from position CDPVault position instead of `address(this)`

### Overview


This bug report is about a problem found in the code of a protocol called Loopfi. The team responsible for the protocol has fixed one part of the bug but not the other. The part that was not fixed is in a function called `_onWithdraw()` and it withdraws from the wrong position. The team has provided a recommended solution to fix this bug.

### Original Finding Content


*Note: This is based on the 2024-07 Loopfi audit [M-35](https://github.com/code-423n4/2024-07-loopfi-findings/issues/81) issue. This protocol team applied a fix, but the fix is incomplete.*

Only the bug in the `_onDeposit()` was fixed, but not the one in `_onWithdraw()`. `PositionAction4626.sol#_onWithdraw` does not withdraw from the correct position, it should withdraw from `position` instead of `address(this)`.

```solidity
    function _onDeposit(address vault, address position, address src, uint256 amount) internal override returns (uint256) {
        address collateral = address(ICDPVault(vault).token());

        // if the src is not the collateralToken, we need to deposit the underlying into the ERC4626 vault
        if (src != collateral) {
            address underlying = IERC4626(collateral).asset();
            IERC20(underlying).forceApprove(collateral, amount);
            amount = IERC4626(collateral).deposit(amount, address(this));
        }

        IERC20(collateral).forceApprove(vault, amount);

        // @audit-note: This was fixed.
        return ICDPVault(vault).deposit(position, amount);
    }


    function _onWithdraw(
        address vault,
        address /*position*/,
        address dst,
        uint256 amount
    ) internal override returns (uint256) {
        // @audit-note: This is still a bug.
@>      uint256 collateralWithdrawn = ICDPVault(vault).withdraw(address(this), amount);

        // if collateral is not the dst token, we need to withdraw the underlying from the ERC4626 vault
        address collateral = address(ICDPVault(vault).token());
        if (dst != collateral) {
            collateralWithdrawn = IERC4626(collateral).redeem(collateralWithdrawn, address(this), address(this));
        }

        return collateralWithdrawn;
    }
```

### Recommended Mitigation Steps

```diff
-       uint256 collateralWithdrawn = ICDPVault(vault).withdraw(address(this), amount);
+       uint256 collateralWithdrawn = ICDPVault(vault).withdraw(position, amount);
```

**[amarcu (LoopFi) confirmed](https://github.com/code-423n4/2024-10-loopfi-findings/issues/13#event-14870931535)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | pkqs90 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-loopfi
- **GitHub**: https://github.com/code-423n4/2024-10-loopfi-findings/issues/13
- **Contest**: https://code4rena.com/reports/2024-10-loopfi

### Keywords for Search

`vulnerability`

