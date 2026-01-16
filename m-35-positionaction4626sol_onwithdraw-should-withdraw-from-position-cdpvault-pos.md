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
solodit_id: 49072
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/81

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
finders_count: 3
finders:
  - pkqs90
  - zhaojohnson
---

## Vulnerability Title

[M-35] `PositionAction4626.sol#_onWithdraw` should withdraw from `position` CDPVault position instead of `address(this)`

### Overview


The report identifies a bug in the `PositionAction4626` contract where the `_onWithdraw` function is withdrawing tokens from the wrong address. This is inconsistent with the parent contract and other similar contracts. The recommended mitigation step is to change the address from `address(this)` to `position` in the code. The impact of this bug is still being evaluated by the judges. 

### Original Finding Content


In `PositionAction4626`, the `_onWithdraw` should withdraw the token from `position` CDPVault position. However, currently it withdraws from `address(this)`. This is inconsistent to the parent contract `PositionAction.sol`, which specifically states the operation should handle the `position` address.

Also, in contrast, we can check the `PositionAction20` contract, it withdraws from the `position` address.

PositionAction4626.sol:

```solidity
    function _onWithdraw(address vault, address /*position*/, address dst, uint256 amount) internal override returns (uint256) {
>       uint256 collateralWithdrawn = ICDPVault(vault).withdraw(address(this), amount);

        // if collateral is not the dst token, we need to withdraw the underlying from the ERC4626 vault
        address collateral = address(ICDPVault(vault).token());
        if (dst != collateral) {
            collateralWithdrawn = IERC4626(collateral).redeem(collateralWithdrawn, address(this), address(this));
        }

        return collateralWithdrawn;
    }
```

PositionAction20.sol:

```solidity
    function _onWithdraw(address vault, address position, address /*dst*/, uint256 amount) internal override returns (uint256) {
>       return ICDPVault(vault).withdraw(position, amount);
    }
```

PositionAction.sol:

```solidity
    /// @notice Hook to withdraw collateral from CDPVault, handles any CDP specific actions
    /// @param vault The CDP Vault
>   /// @param position The CDP Vault position
    /// @param dst Token the caller expects to receive
    /// @param amount The amount of collateral to deposit [wad]
    /// @return Amount of collateral (or dst) withdrawn [CDPVault.tokenScale()]
    function _onWithdraw(address vault, address position, address dst, uint256 amount) internal virtual returns (uint256);
```

### Recommended Mitigation Steps

```diff
-       uint256 collateralWithdrawn = ICDPVault(vault).withdraw(address(this), amount);
+       uint256 collateralWithdrawn = ICDPVault(vault).withdraw(position, amount);
```

**[amarcu (LoopFi) confirmed](https://github.com/code-423n4/2024-07-loopfi-findings/issues/81#event-14337586316)**

**[Koolex (judge) commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/81#issuecomment-2385458026):**
 > Please elaborate on the impact, will re-evaluate in PJQA.

**[pkqs90 (warden) commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/81#issuecomment-2392810633):**
 > @Koolex - The proxy supports depositing/withdrawing collateral from positions other than the proxy itself. An example can be found in unit tests, where a user creates a position for another address (aliceProxy).
> 
> The issue here is that for PositionAction4626, it only supports actions on the vault of the sender proxy, and not any other address. To make a comparison, both PositionAction20 and PositionActionPendle supports it, only PositionAction4626 lack this functionality.
> 
> ```solidity
>     function test_deposit_to_an_unrelated_position() public {
>         // create 2nd position
>         address alice = vm.addr(0x45674567);
>         PRBProxy aliceProxy = PRBProxy(payable(address(prbProxyRegistry.deployFor(alice))));
> 
>         uint256 depositAmount = 10_000 ether;
> 
>         deal(address(token), user, depositAmount);
> 
>         CollateralParams memory collateralParams = CollateralParams({
>             targetToken: address(token),
>             amount: depositAmount,
>             collateralizer: address(user),
>             auxSwap: emptySwap // no entry swap
>         });
> 
>         vm.prank(user);
>         token.approve(address(userProxy), depositAmount);
> 
>         vm.prank(user);
>         userProxy.execute(
>             address(positionAction),
>             abi.encodeWithSelector(
>                 positionAction.deposit.selector,
>                 address(aliceProxy),
>                 address(vault),
>                 collateralParams,
>                 emptyPermitParams
>             )
>         );
> 
>         (uint256 collateral, uint256 debt, , , , ) = vault.positions(address(aliceProxy));
> 
>         assertEq(collateral, depositAmount);
>         assertEq(debt, 0);
>     }
> ```

**[Koolex (judge) commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/81#issuecomment-2408957255):**
 > Stays as-is.

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
| Finders | pkqs90, zhaojohnson |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/81
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

