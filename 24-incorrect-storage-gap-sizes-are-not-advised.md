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
solodit_id: 49100
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[24] Incorrect storage gap sizes are not advised

### Overview

See description below for full details.

### Original Finding Content


Multiple instances of this; for example, see [here](https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/oracle/PendleLPOracle.sol#L17-L45).

```solidity
contract PendleLPOracle is IOracle, AccessControlUpgradeable, UUPSUpgradeable {
    using PendleLpOracleLib for IPMarket;
    /*//////////////////////////////////////////////////////////////
                               CONSTANTS
    //////////////////////////////////////////////////////////////*/

    /// @notice Chainlink aggregator address
    AggregatorV3Interface public immutable aggregator;
    /// @notice Stable period in seconds
    uint256 public immutable stalePeriod;
    /// @notice Aggregator decimal to WAD conversion scale
    uint256 public immutable aggregatorScale;
    /// @notice Pendle Market
    IPMarket public immutable market;
    /// @notice TWAP window in seconds
    uint32 public immutable twapWindow;
    /// @notice Pendle Pt Oracle
    IPPtOracle public immutable ptOracle;

    /*//////////////////////////////////////////////////////////////
                              STORAGE GAP
    //////////////////////////////////////////////////////////////*/

    uint256[50] private __gap;

    /*//////////////////////////////////////////////////////////////
                                 ERRORS
    //////////////////////////////////////////////////////////////*/
```

And [here](https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/oracle/ChainlinkOracle.sol#L28-L34).

```solidity
    /*//////////////////////////////////////////////////////////////
                              STORAGE GAP
    //////////////////////////////////////////////////////////////*/

    uint256[50] private __gap;
```

Evidently, more than one storage slot has been used in these contracts and as such the gap `var` should reflect this.

### Impact

The incorrect storage gap size could lead to potential issues during future upgrades. If new variables are added in upgraded versions, they might overwrite the storage gap, potentially causing storage collisions and unexpected behavior.

### Recommended Mitigation Steps

Adjust the storage gap size to account for the storage slot already used in all instances where upgrades could occur.

This ensures that the total number of storage slots reserved for the contract (including both used slots and the gap) remains at 50, maintaining the intended/safe storage layout for future upgrades.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

