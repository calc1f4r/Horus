---
# Core Classification
protocol: Liquid Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43673
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp
source_link: none
github_link: https://github.com/Cyfrin/2024-09-stakelink

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
  - bladesec
  - trtrth
  - datamcrypto
  - charlesCheerful
---

## Vulnerability Title

Chainlink automation Upkeep can not function because of improper integration

### Overview


The Chainlink automation Upkeep feature is not working correctly due to an error in the integration of the contracts `PriorityPool` and `WithdrawalPool`. This is causing the functions `checkUpkeep()` and `performUpkeep()` to not work properly. The issue is that the data returned by `checkUpkeep()` is not being decoded correctly by `performUpkeep()`, causing it to always fail. This means that the automation tasks cannot be completed using the Upkeep feature. To fix this, the integration needs to be updated to properly return and decode data. This bug has a medium level of risk and was identified using manual tools. 

### Original Finding Content

## Summary
Chainlink automation Upkeep can not work properly because of wrong integration in contracts `PriorityPool`, `WithdrawalPool`

## Vulnerability Details
From [Chainlink's docs](https://docs.chain.link/chainlink-automation/reference/automation-interfaces#checkupkeep-function), the function `checkUpkeep(bytes calldata checkData) external view override returns (bool upkeepNeeded, bytes memory performData)`. In case `upkeepNeeded` returned `true`, then the `performData` is used as input for function `performUpkeep(bytes calldata performData)`.

Chainlink upkeep integration from contract PriorityPool: The function `checkUpkeep()` returns a `abi-encoded` of an `uint256`, when the function `performUpkeep()` tries to decode the input to `bytes[]`. With the returned values from `checkUpkeep()`, the function `performUpkeep()` will always revert.

```Solidity
    function checkUpkeep(bytes calldata) external view returns (bool, bytes memory) {
        uint256 strategyDepositRoom = stakingPool.getStrategyDepositRoom();
        uint256 unusedDeposits = stakingPool.getUnusedDeposits();

        if (poolStatus != PoolStatus.OPEN) return (false, "");
        if (
            strategyDepositRoom < queueDepositMin ||
            (totalQueued + unusedDeposits) < queueDepositMin
        ) return (false, "");

        return (
            true,
@>            abi.encode(
                MathUpgradeable.min(
                    MathUpgradeable.min(strategyDepositRoom, totalQueued + unusedDeposits),
                    queueDepositMax
                )
            )
        );
    }

    function performUpkeep(bytes calldata _performData) external {
@>        bytes[] memory depositData = abi.decode(_performData, (bytes[]));
        _depositQueuedTokens(queueDepositMin, queueDepositMax, depositData);
    }
```

Similarly, the integration in contract `WithdrawalPool` is improper such that: `checkUpkeep()` returns empty data if upkeep is needed, when the function `performUpkeep()` tries to decode input to `bytes[]` which will always revert

```Solidity
    function checkUpkeep(bytes calldata) external view returns (bool, bytes memory) {
        if (
            _getStakeByShares(totalQueuedShareWithdrawals) != 0 &&
            priorityPool.canWithdraw(address(this), 0) != 0 &&
            block.timestamp > timeOfLastWithdrawal + minTimeBetweenWithdrawals
        ) {
@>            return (true, "");
        }
        return (false, "");
    }

    function performUpkeep(bytes calldata _performData) external {
        uint256 canWithdraw = priorityPool.canWithdraw(address(this), 0);
        uint256 totalQueued = _getStakeByShares(totalQueuedShareWithdrawals);
        if (
            totalQueued == 0 ||
            canWithdraw == 0 ||
            block.timestamp <= timeOfLastWithdrawal + minTimeBetweenWithdrawals
        ) revert NoUpkeepNeeded();

        timeOfLastWithdrawal = uint64(block.timestamp);

        uint256 toWithdraw = totalQueued > canWithdraw ? canWithdraw : totalQueued;
@>        bytes[] memory data = abi.decode(_performData, (bytes[]));

        priorityPool.executeQueuedWithdrawals(toWithdraw, data);

        _finalizeWithdrawals(toWithdraw);
    }
```

## Impact
Automation tasks can not be done by Upkeep

## Tools Used
Manual

## Recommendations
Update integration to return and decode data properly

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Liquid Staking |
| Report Date | N/A |
| Finders | bladesec, trtrth, datamcrypto, charlesCheerful |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-09-stakelink
- **Contest**: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp

### Keywords for Search

`vulnerability`

