---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31106
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-salty
source_link: https://code4rena.com/reports/2024-01-salty
github_link: https://github.com/code-423n4/2024-01-salty-findings/issues/712

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
  - 0xpiken
---

## Vulnerability Title

[H-01] Development Team might receive less SALT because there is no access control on `VestingWallet#release()`

### Overview


The report highlights a potential issue with the SALT distribution reward. The problem is that there is no access control on `VestingWallet#release()`, which means anyone can distribute SALT without informing `Upkeep`. This could result in a loss for the Development Team. The report recommends a few mitigation steps, such as configuring `managedTeamWallet` as the beneficiary when deploying `teamVestingWallet` and introducing a new function in `managedTeamWallet` to transfer all SALT balance to `mainWallet`. The issue has been confirmed and mitigated by the team.

### Original Finding Content


The Development Team could potentially incur a loss on their SALT distribution reward due to the absence of access control on `VestingWallet#release()`.

### Proof of Concept

When Salty exchange is actived, 10M SALT will be transferred to `teamVestingWallet` by calling [`InitialDistribution#distributionApproved()`](https://github.com/code-423n4/2024-01-salty/blob/main/src/launch/InitialDistribution.sol#L50-L74):

```solidity
62: 	salt.safeTransfer( address(teamVestingWallet), 10 * MILLION_ETHER );
```

`teamVestingWallet` is responsible for distributing 10M SALT linely over 10 years ([Deployment.sol#L100](https://github.com/code-423n4/2024-01-salty/blob/main/src/dev/Deployment.sol#L100)):

```solidity
    teamVestingWallet = new VestingWallet( address(upkeep), uint64(block.timestamp), 60 * 60 * 24 * 365 * 10 );
```

From the above code we can see that the beneficiary of `teamVestingWallet` is `Upkeep`.

Each time [`Upkeep#performUpkeep()`](https://github.com/code-423n4/2024-01-salty/blob/main/src/Upkeep.sol#L244-L279) is called, `teamVestingWallet` will release a certain amount of SALT to `Upkeep`, the beneficiary, and then the relased SALT will be transferred to `mainWallet` of `managedTeamWallet`:

```solidity
  function step11() public onlySameContract
  {
    uint256 releaseableAmount = VestingWallet(payable(exchangeConfig.teamVestingWallet())).releasable(address(salt));
    
    // teamVestingWallet actually sends the vested SALT to this contract - which will then need to be sent to the active teamWallet
    VestingWallet(payable(exchangeConfig.teamVestingWallet())).release(address(salt));
    
    salt.safeTransfer( exchangeConfig.managedTeamWallet().mainWallet(), releaseableAmount );
  }
```

However, there is no access control on `teamVestingWallet.release()`. Any one can call `release()` to distribute SALT without informing `upkeep`. `upkeep` doesn't know how many SALT has been distributed in advance, it has no way to transfer it to the development team, and the distributed SALT by directly calling `teamVestingWallet.release()` will be locked in `upkeep` forever.

Copy below codes to [DAO.t.sol](https://github.com/code-423n4/2024-01-salty/blob/main/src/dao/tests/DAO.t.sol) and run `COVERAGE="yes" NETWORK="sep" forge test -vv --rpc-url RPC_URL --match-test testTeamRewardIsLockedInUpkeep`

```solidity
  function testTeamRewardIsLockedInUpkeep() public {
    uint releasableAmount = teamVestingWallet.releasable(address(salt));
    uint upKeepBalance = salt.balanceOf(address(upkeep));
    uint mainWalletBalance = salt.balanceOf(address(managedTeamWallet.mainWallet()));
    //@audit-info a certain amount of SALT is releasable
    assertTrue(releasableAmount != 0);
    //@audit-info there is no SALT in upkeep
    assertEq(upKeepBalance, 0);
    //@audit-info there is no SALT in mainWallet
    assertEq(mainWalletBalance, 0);
    //@audit-info call release() before performUpkeep()
    teamVestingWallet.release(address(salt));
    upkeep.performUpkeep();
    
    upKeepBalance = salt.balanceOf(address(upkeep));
    mainWalletBalance = salt.balanceOf(address(managedTeamWallet.mainWallet()));
    //@audit-info all released SALT is locked in upKeep
    assertEq(upKeepBalance, releasableAmount);
    //@audit-info development team receive nothing
    assertEq(mainWalletBalance, 0);
  }
```

### Recommended Mitigation Steps

*   Since `exchangeConfig.managedTeamWallet` is immutable, it is reasonable to config `managedTeamWallet` as the beneficiary when [deploying `teamVestingWallet`](https://github.com/code-423n4/2024-01-salty/blob/main/src/dev/Deployment.sol#L100):

```diff
-   teamVestingWallet = new VestingWallet( address(upkeep), uint64(block.timestamp), 60 * 60 * 24 * 365 * 10 );
+   teamVestingWallet = new VestingWallet( address(managedTeamWallet), uint64(block.timestamp), 60 * 60 * 24 * 365 * 10 );
```

*   Introduce a new function in `managedTeamWallet` to transfer all SALT balance to `mainWallet`:

```solidity
  function release(address token) external {
    uint balance = IERC20(token).balanceOf(address(this));
    if (balance != 0) {
      IERC20(token).safeTransfer(mainWallet, balance);
    }
  }
```

*   Call `managedTeamWallet#release()` in `Upkeep#performUpkeep()`:

```diff
  function step11() public onlySameContract
  {
-   uint256 releaseableAmount = VestingWallet(payable(exchangeConfig.teamVestingWallet())).releasable(address(salt));
    
-   // teamVestingWallet actually sends the vested SALT to this contract - which will then need to be sent to the active teamWallet
    VestingWallet(payable(exchangeConfig.teamVestingWallet())).release(address(salt));
    
-   salt.safeTransfer( exchangeConfig.managedTeamWallet().mainWallet(), releaseableAmount );
+   exchangeConfig.managedTeamWallet().release(address(salt));
  }
```
**[othernet-global (Salty.IO) confirmed and commented](https://github.com/code-423n4/2024-01-salty-findings/issues/712#issuecomment-1945532417):**
 > The ManagedWallet now the recipient of teamVestingWalletRewards to prevent the issue of DOS of the team rewards.
> 
> https://github.com/othernet-global/salty-io/commit/534d04a40c9b5821ad4e196095df70c0021d15ab

 > ManagedWallet has been removed.
> 
> https://github.com/othernet-global/salty-io/commit/5766592880737a5e682bb694a3a79e12926d48a5

**[Picodes (Judge) commented](https://github.com/code-423n4/2024-01-salty-findings/issues/712#issuecomment-1967449721):**
 > My initial view on this is that the issue is within `Upkeep` as it integrates poorly with the vesting wallet. It forgets that there is no access control, so I tend to see this as in scope.

 > The issue is not strictly in the deployment scripts, not strictly in the vesting wallet either because it makes sense to have no access control on `release`, so it must be in `Upkeep`.

_Note: For full discussion, see [here](https://github.com/code-423n4/2024-01-salty-findings/issues/712)._

**Status:** Mitigation confirmed. Full details in reports from [0xpiken](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/61), [zzebra83](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/41), and [t0x1c](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/33).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | 0xpiken |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-salty
- **GitHub**: https://github.com/code-423n4/2024-01-salty-findings/issues/712
- **Contest**: https://code4rena.com/reports/2024-01-salty

### Keywords for Search

`vulnerability`

