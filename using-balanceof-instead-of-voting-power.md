---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57185
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 45
finders:
  - kkk
  - petersr
  - x1485967
  - ok567
  - 0xwhyzee
---

## Vulnerability Title

Using balanceOf Instead of Voting Power

### Overview


This bug report discusses an issue in the contracts `BaseGauge` and `GaugeController` where the function `balanceOf` is used instead of `getVotingPower`. This leads to incorrect boost and voting power calculations due to the ignoring of lock expiration decay. This can have significant economic impacts, such as inequitable reward distributions and imbalanced protocol revenue sharing. The report recommends replacing instances of `balanceOf` with `getVotingPower` to accurately reflect voting power. 

### Original Finding Content

## Summary

These contracts (`BaseGauge`, `GaugeController`) use `veToken.balanceOf()` instead of `getVotingPower()`. This ignores lock expiration decay, leading to incorrect boost and voting power calculations.

## Vulnerability Details

The use of `balanceOf()` instead of `getVotingPower()` creates significant calculation discrepancies in the protocol.&#x20;

In BaseGauge.sol#[\_applyBoost](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/gauges/BaseGauge.sol#L229-L235)

```Solidity
function _applyBoost(address account, uint256 baseWeight) internal view virtual returns (uint256) {
    IERC20 veToken = IERC20(IGaugeController(controller).veRAACToken());
    uint256 veBalance = veToken.balanceOf(account); // Should use getVotingPower

```

In GaugeController.sol#[vote](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/gauges/GaugeController.sol#L190-L194)

```Solidity
function vote(address gauge, uint256 weight) external override whenNotPaused {
    uint256 votingPower = veRAACToken.balanceOf(msg.sender); // Should use getVotingPower

```

Economic Impact:

* Boost calculations provide wrong multipliers
* Reward distributions become inequitable
* Incentive mechanisms fail to reward lock duration
* Protocol revenue sharing becomes imbalanced

## Impact

Users have no incentive to lock longer

## Tools Used

Manual

## Recommendations

Replace the instances of `balanceOf` with `getVotingPower(account, block.timestamp)` to reflect actual voting power.

```Solidity
// In BaseGauge.sol
function _applyBoost(address account, uint256 baseWeight) internal view returns (uint256) {
    uint256 votingPower = veToken.getVotingPower(account, block.timestamp);
    uint256 totalVotingPower = veToken.getTotalVotingPower();
    return calculateBoost(votingPower, totalVotingPower, baseWeight);
}

// In GaugeController.sol
function vote(address gauge, uint256 weight) external whenNotPaused {
    uint256 votingPower = veToken.getVotingPower(msg.sender, block.timestamp);
    _updateGaugeWeight(gauge, weight, votingPower);
}

// In BoostController.sol
function calculateBoost(address user, address pool, uint256 amount) external view returns (uint256) {
    uint256 votingPower = veToken.getVotingPower(user, block.timestamp);
    return _calculateBoost(votingPower, amount);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | kkk, petersr, x1485967, ok567, 0xwhyzee, patitonar, kwakudr, casinocompiler, 0xyashar, akhoronko, theirrationalone, 0xbz, 0x9527, zukanopro, johny7173, uzeyirch, amow, aariiif, drlaravel, 3n0ch, iamthesvn, 0xblockhound, charlescheerful, oxanmol, z3nithpu1se, mill1995, hard1k, io10, 0xmystery, josh4324, udogodwin2k22, shui, alexczm, 0xswahili |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

