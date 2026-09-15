---
# Core Classification
protocol: Falcon_2025-02-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49896
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Falcon-security-review_2025-02-17.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
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

[M-02] Shares cannot be minted on a deposit attack

### Overview


This bug report discusses an issue with the stakedUSDf contract, where a malicious user can manipulate the deposit process and cause the contract to fail. This can result in users not receiving the correct amount of sUSDf when depositing USDf into the contract. The report suggests a solution to prevent this from happening in the future by sweeping all assets from the contract if the total supply is zero. This will help prevent any potential attacks and ensure that users receive the correct amount of sUSDf when depositing.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When users deposit USDf into the stakedUSDf contract, they get back sUSDf. The calculation follows [ERC4626](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/8ab1f5acf958b937531cee87f99ae4c0242f0dee/contracts/token/ERC20/extensions/ERC4626Upgradeable.sol#L247), as so:

```
  function _convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual returns (uint256) {
        return assets.mulDiv(totalSupply() + 10 ** _decimalsOffset(), totalAssets() + 1, rounding);
    }
```

If the user deposits the first 100e18 USDf, he will get `assets * totalSupply() + 1 / totalAssets() + 1` = 1e18 \* (0+1) / (0+1) = 1e18 shares

There is a `MIN_SHARES`[check](https://github.com/falconfinance/falcon-contracts-evm/blob/9c34a242ae6c39e2054d5e3bb62e44328339aaa1/src/StakedUSDf.sol#L219) during deposit to ensure that the shares cannot be below 1e18.

```
function _checkMinShares() internal view {
        uint256 supply = totalSupply();
>       if (supply > 0 && supply < MIN_SHARES) {
            revert MinSharesViolation();
        }
    }

    function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal override {
        _checkZeroAmount(assets);
        _checkZeroAmount(shares);
        _checkRestricted(caller);
        _checkRestricted(receiver);

        super._deposit(caller, receiver, assets, shares);
        _checkMinShares();
    }
```

The issue with this check is that a malicious user can directly deposit 1e18 USDf inside the stakedUSDf contract before anyone calls `deposit()`, making `totalAssets() = 1e18` and `totalSupply() = 0`

When the shares are calculated, `assets * totalSupply() + 1 / totalAssets() + 1` , 1e18 \* 1 / (1e18 + 1) = 1, and even if more assets are deposited for the first time, eg 1e20, the shares returned will be less than 1e18, which will invoke the `ZeroAmount` error.

The test below describes the direct deposit attack, append under deposit.t.sol.

```
    function test2_deposit() public {
        // User deposits USDf directly into the stakedUSDf contract, resulting in "ZeroAmount" issue

        uint mintAmount = 1e25;

        vm.startPrank(user1);
        deal(address(usdf), user1, mintAmount);
        usdf.approve(address(stakedUSDf), mintAmount);
        // Directly deposit 1e18 worth of USDf before any `deposit()` is called
        usdf.transfer(address(stakedUSDf), 1e18);
        console2.log("USDF BALANCE of user:", usdf.balanceOf(address(stakedUSDf)));
        console2.log("SUSDF TOTALSUPPLY of user", stakedUSDf.totalSupply());
        // If this number is changed from 1e18 -> 1e25 , all will fail because of "MIN_SHARE_VIOLATION"
        stakedUSDf.deposit(1e18, user1);
        vm.stopPrank();
        console2.log("USDF BALANCE TREASURY:", usdf.balanceOf(address(stakedUSDf.TREASURY())));
        console2.log("USDF BALANCE in contract:", usdf.balanceOf(address(stakedUSDf)));
        console2.log("SUSDF TOTALSUPPLY in contract", stakedUSDf.totalSupply());

        console2.log("USDF BALANCE of user:", usdf.balanceOf(address(user1)));
        console2.log("SUSDF TOTALSUPPLY of user", stakedUSDf.balanceOf(user1));
    }
```

## Recommendations

To ensure this doesn't happen, sweep all the assets inside the contract if `totalSupply() == 0`. Override the deposit function instead of the `_deposit()` since in the deposit function will calculate `previewDeposit()` before calling `_deposit()`, which will return 0 for the above attack.

```
Append in stakedUSDf.sol:

     function deposit(uint256 assets, address receiver) public override returns (uint256) {
        if(IERC20(asset()).balanceOf(address(this)) != 0 && totalSupply() == 0) {
            SafeERC20.safeTransfer(IERC20(asset()), TREASURY,  IERC20(asset()).balanceOf(address(this)));
        }
        super.deposit(assets, receiver);
     }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Falcon_2025-02-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Falcon-security-review_2025-02-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

