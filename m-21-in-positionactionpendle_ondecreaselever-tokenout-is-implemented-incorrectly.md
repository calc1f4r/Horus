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
solodit_id: 49058
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/160

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
finders_count: 4
finders:
  - minglei-wang-3570
  - lian886
  - 0xc0ffEE
  - zhaojohnson
---

## Vulnerability Title

[M-21] In `PositionActionPendle::_onDecreaseLever`, `tokenOut` is implemented incorrectly

### Overview


The bug report discusses an issue with the function `PositionActionPendle::_onDecreaseLever` in the LoopFi code. This function is used to decrease the lever by withdrawing collateral from the CDPVault. However, the current implementation is incorrect if a certain parameter, `leverParams.auxAction.args.length`, is equal to 0. In this case, the function `_onWithdraw` is called, but the `tokenOut` still returns 0, leading to incorrect accounting. The bug is confirmed and it is recommended to handle this edge case properly by returning `tokenOut` if `leverParams.auxAction.args.length` is 0. The severity of this bug has been decreased to Medium since it is an edge case.

### Original Finding Content


The function `PositionActionPendle::_onDecreaseLever` is a  hook to decrease lever by withdrawing collateral from the CDPVault. But the current implementation is wrong if `leverParams.auxAction.args.length` is 0, `_onWithdraw` is called here, but the `tokenOut` still returns 0.

```solidity
    function _onDecreaseLever(
        LeverParams memory leverParams,
        uint256 subCollateral
    ) internal override returns (uint256 tokenOut) {
@>      _onWithdraw(leverParams.vault, leverParams.position, address(0), subCollateral);

        if (leverParams.auxAction.args.length != 0) {
            bytes memory exitData = _delegateCall(
                address(poolAction), abi.encodeWithSelector(poolAction.exit.selector, leverParams.auxAction)
            );

@>          tokenOut = abi.decode(exitData, (uint256));
        }
    }
```

The `tokenOut` accounting will be incorrect if the `leverParams.auxAction.args.length` is 0.

### Proof of Concept

We can see that the function [`PositionActionPendle::_onDecreaseLever`](https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/proxy/PositionActionPendle.sol#L76) returns the `tokenOut` on successful withdraw.

```solidity
    function _onDecreaseLever(
        LeverParams memory leverParams,
        uint256 subCollateral
    ) internal override returns (uint256 tokenOut) {
        _onWithdraw(leverParams.vault, leverParams.position, address(0), subCollateral);

        if (leverParams.auxAction.args.length != 0) {
            bytes memory exitData = _delegateCall(
                address(poolAction), abi.encodeWithSelector(poolAction.exit.selector, leverParams.auxAction)
            );

            tokenOut = abi.decode(exitData, (uint256));
        }
    }
```

But in the above implementation, The `tokenOut` accounting will be incorrect if the `leverParams.auxAction.args.length` is 0.

The implementation properly handled in the function [`PositionAction4626::_onDecreaseLever()`](https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/proxy/PositionAction4626.sol#L136) as the `tokenOut` is return even if `leverParams.auxAction.args.length` is 0.

```solidity
    function _onDecreaseLever(
        LeverParams memory leverParams,
        uint256 subCollateral
    ) internal override returns (uint256 tokenOut) {
        // withdraw collateral from vault
        uint256 withdrawnCollateral = ICDPVault(leverParams.vault).withdraw(address(this), subCollateral);

        // withdraw collateral from the ERC4626 vault and return underlying assets
@>       tokenOut = IERC4626(leverParams.collateralToken).redeem(withdrawnCollateral, address(this), address(this));

        if (leverParams.auxAction.args.length != 0) {
            bytes memory exitData = _delegateCall(
                address(poolAction),
                abi.encodeWithSelector(poolAction.exit.selector, leverParams.auxAction)
            );

            tokenOut = abi.decode(exitData, (uint256));
        }
    }
```

### Recommended Mitigation Steps

Handle the edge case properly like `PositionAction4626::_onDecreaseLever()` and return `tokenOut` if `leverParams.auxAction.args.length` is 0.

### Assessed type

Token-Transfer

**[amarcu (LoopFi) confirmed and commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/160#issuecomment-2360426562):**
 > The flow will always revert because of how the parameters are set. We will make the update to always revert with a custom message for the case where the `auxSwap` is not defined. Maybe this can be re-evaluated as a medium.

**[Koolex (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/160#issuecomment-2371320667):**
 > Medium, since it is an edge case.

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
| Finders | minglei-wang-3570, lian886, 0xc0ffEE, zhaojohnson |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/160
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

