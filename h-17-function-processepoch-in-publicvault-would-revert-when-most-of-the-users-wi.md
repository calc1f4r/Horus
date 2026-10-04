---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25812
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/188

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - evan
  - unforgiven
  - 0xbepresent
---

## Vulnerability Title

[H-17] Function `processEpoch()` in PublicVault would revert when most of the users withdraw their funds because of the underflow for new yIntercept calculation

### Overview


This bug report is about the PublicVault.sol code, which is part of a project called Astaria. The code is responsible for calculating the ratio between the WithdrawProxy and the PublicVault when users withdraw their funds from the vault. The problem is that when a lot of users withdraw their funds, the value of the totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18) can be higher than the yIntercept, which can cause an underflow when setting the new value of yIntercept. This would prevent the last user from withdrawing their funds and break the contract epoch system.

The code that is causing the issue is part of the processEpoch() function, which calculates the ratio between WithdrawProxy and PublicVault. The code tries to set a new value for yIntercept but totalAssets() can be higher than yIntercept, which causes the code to revert.

The tools used for this bug report were VIM. To mitigate this issue, it is recommended to call accrue() at the beginning of the processEpoch() to prevent underflow. This was confirmed by SantiagoGregory (Astaria) via duplicate issue #408. The severity was also increased to High by Picodes (judge).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L314-L335><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L479-L493>

When users withdraw their vault tokens PublicVault mint WithdrawProxy's shares token for them and at the end of the epoch PublicVault would calculated WithdrawProxy's assets and update PublicVault assets and start the next epoch. if a lot of users withdraws their funds then the value of the `totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18)` (the amount belongs to the WithdrawProxy) would be higher than `yIntercept` and code would revert because of the underflow when setting the new value of the `yIntercept`. This would cause last users to not be able to withdraw their funds and contract epoch system to be broken for a while.

### Proof of Concept

This is part of `processEpoch()` code that calculates ratio between WithdrawProxy and PublicVault:

      function processEpoch() public {
    .....
    .....
        // reset liquidationWithdrawRatio to prepare for re calcualtion
        s.liquidationWithdrawRatio = 0;

        // check if there are LPs withdrawing this epoch
        if ((address(currentWithdrawProxy) != address(0))) {
          uint256 proxySupply = currentWithdrawProxy.totalSupply();

          s.liquidationWithdrawRatio = proxySupply
            .mulDivDown(1e18, totalSupply())
            .safeCastTo88();

          currentWithdrawProxy.setWithdrawRatio(s.liquidationWithdrawRatio);
          uint256 expected = currentWithdrawProxy.getExpected();

          unchecked {
            if (totalAssets() > expected) {
              s.withdrawReserve = (totalAssets() - expected)
                .mulWadDown(s.liquidationWithdrawRatio)
                .safeCastTo88();
            } else {
              s.withdrawReserve = 0;
            }
          }
          _setYIntercept(
            s,
            s.yIntercept -
              totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18)
          );
          // burn the tokens of the LPs withdrawing
          _burn(address(this), proxySupply);
        }

As you can see in the line `_setYIntercept(s, s.yIntercept - totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18))` code tries to set new value for `yIntercept` but This is `totalAssets()` code:

      function totalAssets()
        public
        view
        virtual
        override(ERC4626Cloned)
        returns (uint256)
      {
        VaultData storage s = _loadStorageSlot();
        return _totalAssets(s);
      }

      function _totalAssets(VaultData storage s) internal view returns (uint256) {
        uint256 delta_t = block.timestamp - s.last;
        return uint256(s.slope).mulDivDown(delta_t, 1) + uint256(s.yIntercept);
      }

So as you can see `totalAssets()` can be higher than `yIntercept` and if most of the user withdraw their funds(for example the last user) then the value of `liquidationWithdrawRatio` would be near `1` too and the value of `totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18)` would be bigger than `yIntercept` and call to `processEpoch()` would revert and code can't start the next epoch and user withdraw process can't be finished and funds would stuck in the contract.

### Tools Used

VIM

### Recommended Mitigation Steps

Prevent underflow by calling `accrue()` in the begining of the `processEpoch()`.

**[SantiagoGregory (Astaria) confirmed via duplicate issue `#408`](https://github.com/code-423n4/2023-01-astaria-findings/issues/408#event-8415693497)**

**[Picodes (judge) increased severity to High](https://github.com/code-423n4/2023-01-astaria-findings/issues/188#issuecomment-1443477344)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | evan, unforgiven, 0xbepresent |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/188
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

