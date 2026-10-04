---
# Core Classification
protocol: Backd
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2601
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-backd-tokenomics-contest
source_link: https://code4rena.com/reports/2022-05-backd
github_link: https://github.com/code-423n4/2022-05-backd-findings/issues/98

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-06] Minter.sol#_executeInflationRateUpdate() inflationManager().checkpointAllGauges() is called after InflationRate is updated, causing users to lose rewards

### Overview


This bug report is about a vulnerability in the Minter.sol#_executeInflationRateUpdate() function. When this function is called, if an _INFLATION_DECAY_PERIOD has passed since the lastInflationDecay, it will update the InflationRate for all of the gauges. However, the current implementation updates the rates first, followed by the rewards being settled using the new rates on the gauges using inflationManager().checkpointAllGauges(). If the _INFLATION_DECAY_PERIOD has passed for a long time before Minter.sol#executeInflationRateUpdate() is called, the users may lose a significant amount of rewards.

A proof of concept (PoC) is given to illustrate the issue. In the example, Alice deposited as the one and only staker in the AmmGauge pool, 1 month later, Minter.sol#_executeInflationRateUpdate() was called and Alice claimed her rewards and received 500 Bkd tokens instead of the expected 1000 Bkd tokens.

The recommendation is to move the call to checkpointAllGauges() to before the currentInflationAmountKeeper is updated. This would ensure that the rewards are settled using the new rates before they are updated.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/Minter.sol#L187-L215


## Vulnerability details

When `Minter.sol#_executeInflationRateUpdate()` is called, if an `_INFLATION_DECAY_PERIOD` has past since `lastInflationDecay`, it will update the InflationRate for all of the gauges.

However, in the current implementation, the rates will be updated first, followed by the rewards being settled using the new rates on the gauges using `inflationManager().checkpointAllGauges()`.

If the `_INFLATION_DECAY_PERIOD` has passed for a long time before `Minter.sol#executeInflationRateUpdate()` is called, the users may lose a significant amount of rewards.

On a side note, `totalAvailableToNow` is updated correctly.

https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/Minter.sol#L187-L215

```solidity
function _executeInflationRateUpdate() internal returns (bool) {
    totalAvailableToNow += (currentTotalInflation * (block.timestamp - lastEvent));
    lastEvent = block.timestamp;
    if (block.timestamp >= lastInflationDecay + _INFLATION_DECAY_PERIOD) {
        currentInflationAmountLp = currentInflationAmountLp.scaledMul(annualInflationDecayLp);
        if (initialPeriodEnded) {
            currentInflationAmountKeeper = currentInflationAmountKeeper.scaledMul(
                annualInflationDecayKeeper
            );
            currentInflationAmountAmm = currentInflationAmountAmm.scaledMul(
                annualInflationDecayAmm
            );
        } else {
            currentInflationAmountKeeper =
                initialAnnualInflationRateKeeper /
                _INFLATION_DECAY_PERIOD;

            currentInflationAmountAmm = initialAnnualInflationRateAmm / _INFLATION_DECAY_PERIOD;
            initialPeriodEnded = true;
        }
        currentTotalInflation =
            currentInflationAmountLp +
            currentInflationAmountKeeper +
            currentInflationAmountAmm;
        controller.inflationManager().checkpointAllGauges();
        lastInflationDecay = block.timestamp;
    }
    return true;
}
```

https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/InflationManager.sol#L110-L125

```solidity
function checkpointAllGauges() external override returns (bool) {
    uint256 length = _keeperGauges.length();
    for (uint256 i; i < length; i = i.uncheckedInc()) {
        IKeeperGauge(_keeperGauges.valueAt(i)).poolCheckpoint();
    }
    address[] memory stakerVaults = addressProvider.allStakerVaults();
    for (uint256 i; i < stakerVaults.length; i = i.uncheckedInc()) {
        IStakerVault(stakerVaults[i]).poolCheckpoint();
    }

    length = _ammGauges.length();
    for (uint256 i; i < length; i = i.uncheckedInc()) {
        IAmmGauge(_ammGauges.valueAt(i)).poolCheckpoint();
    }
    return true;
}
```

https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/KeeperGauge.sol#L110-L117

```solidity
function poolCheckpoint() public override returns (bool) {
    if (killed) return false;
    uint256 timeElapsed = block.timestamp - uint256(lastUpdated);
    uint256 currentRate = IController(controller).inflationManager().getKeeperRateForPool(pool);
    perPeriodTotalInflation[epoch] += currentRate * timeElapsed;
    lastUpdated = uint48(block.timestamp);
    return true;
}
```

https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/InflationManager.sol#L507-L519

```solidity
function getKeeperRateForPool(address pool) external view override returns (uint256) {
    if (minter == address(0)) {
        return 0;
    }
    uint256 keeperInflationRate = Minter(minter).getKeeperInflationRate();
    // After deactivation of weight based dist, KeeperGauge handles the splitting
    if (weightBasedKeeperDistributionDeactivated) return keeperInflationRate;
    if (totalKeeperPoolWeight == 0) return 0;
    bytes32 key = _getKeeperGaugeKey(pool);
    uint256 poolInflationRate = (currentUInts256[key] * keeperInflationRate) /
        totalKeeperPoolWeight;
    return poolInflationRate;
}
```


https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/Minter.sol#L173-L176

```solidity
    function getKeeperInflationRate() external view override returns (uint256) {
        if (lastEvent == 0) return 0;
        return currentInflationAmountKeeper;
    }
```

### PoC

Given:

- currentInflationAmountAmm: 12,000 Bkd (1000 per month)
- annualInflationDecayAmm: 50%
- initialPeriodEnded: true
- lastInflationDecay: 11 months ago
- _INFLATION_DECAY_PERIOD: 1 year

1. Alice deposited as the one and only staker in the `AmmGauge` pool;
2. 1 month later;
3. `Minter.sol#_executeInflationRateUpdate()` is called;
4. Alice `claimableRewards()` and received `500` Bkd tokens.

Expected Results:

- Alice to receive `1000` Bkd tokens as rewards.

Actual Results:

- Alice received `500` Bkd tokens as rewards.

### Recommendation

Consider moving the call to `checkpointAllGauges()` to before the `currentInflationAmountKeeper` is updated.

```solidity
function _executeInflationRateUpdate() internal returns (bool) {
    totalAvailableToNow += (currentTotalInflation * (block.timestamp - lastEvent));
    lastEvent = block.timestamp;
    if (block.timestamp >= lastInflationDecay + _INFLATION_DECAY_PERIOD) {
        controller.inflationManager().checkpointAllGauges();
        currentInflationAmountLp = currentInflationAmountLp.scaledMul(annualInflationDecayLp);
        if (initialPeriodEnded) {
            currentInflationAmountKeeper = currentInflationAmountKeeper.scaledMul(
                annualInflationDecayKeeper
            );
            currentInflationAmountAmm = currentInflationAmountAmm.scaledMul(
                annualInflationDecayAmm
            );
        } else {
            currentInflationAmountKeeper =
                initialAnnualInflationRateKeeper /
                _INFLATION_DECAY_PERIOD;

            currentInflationAmountAmm = initialAnnualInflationRateAmm / _INFLATION_DECAY_PERIOD;
            initialPeriodEnded = true;
        }
        currentTotalInflation =
            currentInflationAmountLp +
            currentInflationAmountKeeper +
            currentInflationAmountAmm;
        lastInflationDecay = block.timestamp;
    }
    return true;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-backd
- **GitHub**: https://github.com/code-423n4/2022-05-backd-findings/issues/98
- **Contest**: https://code4rena.com/contests/2022-05-backd-tokenomics-contest

### Keywords for Search

`Business Logic`

