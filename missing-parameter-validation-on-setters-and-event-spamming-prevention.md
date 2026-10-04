---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6944
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

Missing parameter validation on setters and event spamming prevention

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context

- `RewardsManagerForAave.sol#L72-L79`
- `MarketsManagerForAave.sol#L143-L151`
- `MarketsManagerForAave.sol#L189-L196`
- `MarketsManagerForAave.sol#L200-L202`
- `MarketsManagerForAave.sol#L206-L208`
- `PositionsManagerForAaveGettersSetters.sol#L33-L36`
- `PositionsManagerForAaveGettersSetters.sol#L40-L43`
- `PositionsManagerForAaveGettersSetters.sol#L47-L50`
- `PositionsManagerForAaveGettersSetters.sol#L54-L57`
- `PositionsManagerForAaveGettersSetters.sol#L61-L64`
- `PositionsManagerForAaveGettersSetters.sol#L68-L72`

## Description

User parameter validity should always be verified to prevent contract updates in an inconsistent state. The parameter’s value should also be different from the old one in order to prevent event spamming (emitting an event when not needed) and improve contract monitoring.

### Example Code Changes

**`contracts/aave/RewardsManagerForAave.sol`**

```solidity
function setAaveIncentivesController(address _aaveIncentivesController)
external
override
onlyOwner
{
    require(_aaveIncentivesController != address(0), "param != address(0)");
    require(_aaveIncentivesController != aaveIncentivesController, "param != prevValue");
    aaveIncentivesController = IAaveIncentivesController(_aaveIncentivesController);
    emit AaveIncentivesControllerSet(_aaveIncentivesController);
}
```

**`contracts/aave/MarketsManagerForAave.sol`**

```solidity
function setReserveFactor(address _marketAddress, uint16 _newReserveFactor) external onlyOwner {
    require(_marketAddress != address(0), "param != address(0)");
    uint16 finalReserveFactor = HALF_MAX_BASIS_POINTS <= _newReserveFactor
    ? HALF_MAX_BASIS_POINTS
    : _newReserveFactor;

    if (finalReserveFactor !== reserveFactor[_marketAddress]) {
        reserveFactor[_marketAddress] = finalReserveFactor;
        emit ReserveFactorSet(_marketAddress, finalReserveFactor);
    }

    updateRates(_marketAddress);
}
```

```solidity
function setNoP2P(address _marketAddress, bool _noP2P)
external
onlyOwner
isMarketCreated(_marketAddress)
{
    require(_noP2P != noP2P[_marketAddress], "param != prevValue");
    noP2P[_marketAddress] = _noP2P;
    emit NoP2PSet(_marketAddress, _noP2P);
}
```

```solidity
function updateP2PExchangeRates(address _marketAddress)
external
override
onlyPositionsManager
isMarketCreated(_marketAddress)
{
    _updateP2PExchangeRates(_marketAddress);
}
```

```solidity
function updateSPYs(address _marketAddress)
external
override
onlyPositionsManager
isMarketCreated(_marketAddress)
{
    _updateSPYs(_marketAddress);
}
```

**`contracts/aave/positions-manager-parts/PositionsManagerForAaveGettersSetters.sol`**

```solidity
function setAaveIncentivesController(address _aaveIncentivesController) external onlyOwner {
    require(_aaveIncentivesController != address(0), "param != address(0)");
    require(_aaveIncentivesController != aaveIncentivesController, "param != prevValue");
    aaveIncentivesController = IAaveIncentivesController(_aaveIncentivesController);
    emit AaveIncentivesControllerSet(_aaveIncentivesController);
}
```

## Important Notes

- `_newNDS` min/max value should be accurately validated by the team because this will influence the maximum number of cycles that `DDL.insertSorted` can do. Setting a value too high would make the transaction fail, while setting it too low would make the `insertSorted` loop exit earlier, resulting in the user being added to the tail of the list. A more detailed issue about the NDS value can be found here: #33

```solidity
function setNDS(uint8 _newNDS) external onlyOwner {
    // add a check on `_newNDS ` validating correctly max/min value of `_newNDS `
    require(NDS != _newNDS, "param != prevValue");
    NDS = _newNDS;
    emit NDSSet(_newNDS);
}
```

- `_newNDS` set to 0 would skip all the `MatchingEngineForAave` match/unmatch supplier/borrower functions if the user does not specify a custom `maxGas`. A more detailed issue about NDS value can be found here: #34

```solidity
function setMaxGas(MaxGas memory _maxGas) external onlyOwner {
    // add a check on `_maxGas ` validating correctly max/min value of `_maxGas `
    // add a check on `_maxGas ` internal value checking that at least one of them is different compared to the old version, !
    maxGas = _maxGas;
    emit MaxGasSet(_maxGas);
}
```

```solidity
function setTreasuryVault(address _newTreasuryVaultAddress) external onlyOwner {
    require(_newTreasuryVaultAddress != address(0), "param != address(0)");
    require(_newTreasuryVaultAddress != treasuryVault, "param != prevValue");
    treasuryVault = _newTreasuryVaultAddress;
    emit TreasuryVaultSet(_newTreasuryVaultAddress);
}
```

```solidity
function setRewardsManager(address _rewardsManagerAddress) external onlyOwner {
    require(_rewardsManagerAddress != address(0), "param != address(0)");
    require(_rewardsManagerAddress != rewardsManager, "param != prevValue");
    rewardsManager = IRewardsManagerForAave(_rewardsManagerAddress);
    emit RewardsManagerSet(_rewardsManagerAddress);
}
```

- Important note: Should also check that `_poolTokenAddress` is currently handled by the `PositionsManagerForAave` and by the `MarketsManagerForAave`. Without this check, a pool token could start in a paused state.

```solidity
function setPauseStatus(address _poolTokenAddress) external onlyOwner {
    require(_poolTokenAddress != address(0), "param != address(0)");
    bool newPauseStatus = !paused[_poolTokenAddress];
    paused[_poolTokenAddress] = newPauseStatus;
    emit PauseStatusSet(_poolTokenAddress, newPauseStatus);
}
```

## Recommendation

For each setter, add a validity check on user parameter and a check to prevent updating the state value with the same value and fire an event when it’s not needed.

### Morpho

After reflection, as all these functions will be triggered by governance, it might be overkill to implement all these checks. Although we will implement min and max value for `NDS` and for `maxGas` values.

### Spearbit

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

