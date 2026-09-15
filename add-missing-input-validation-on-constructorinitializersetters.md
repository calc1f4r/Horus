---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7024
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.50
financial_impact: medium

# Scoring
quality_score: 2.5
rarity_score: 2

# Context Tags
tags:
  - validation
  - initialization

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

Add missing input validation on constructor/initializer/setters

### Overview


This bug report is about the contracts Allowlist.1.sol, Firewall.sol, OperatorsRegistry.1.sol, Oracle.1.sol, River.1.sol and ConsensusLayerDepositManager.1.sol. The bug report recommends to implement checks to ensure that the address(0) is not used in the parameters of the contracts. The report also recommends adding min and max limits to the values of _annualAprUpperBound and _relativeLowerBound in Oracle.1.sol and _withdrawalCredentials in ConsensusLayerDepositManager.1.sol. The bug report has been implemented in SPEARBIT/10 and some validation checks will be addressed in another PR.

### Original Finding Content

## Severity: Medium Risk

## Description: Allowlist.1.sol

- `initAllowlistV1` should require the `_admin` parameter to be not equal to `address(0)`. This check is not needed if the issue with `LibOwnable._setAdmin` allows setting `address(0)` as the admin of the contract is implemented directly at `LibOwnable._setAdmin` level.
- `allow` should check that `_accounts[i]` is not equal to `address(0)`.

## Firewall.sol

- Constructor should check that: `governor_ != address(0)`, `executor_ != address(0)`, `destination_ != address(0)`.
- `setGovernor` should check that `newGovernor` is not equal to `address(0)`.
- `setExecutor` should check that `newExecutor` is not equal to `address(0)`.

## OperatorsRegistry.1.sol

- `initOperatorsRegistryV1` should require the `_admin` parameter to be not equal to `address(0)`. This check is not needed if the issue with `LibOwnable._setAdmin` allows setting `address(0)` as the admin of the contract is implemented directly at `LibOwnable._setAdmin` level.
- `addOperator` should check: `_name` is not an empty string, `_operator` is not equal to `address(0)`, and `_feeRecipient` is not equal to `address(0)`.
- `setOperatorAddress` should check that `_newOperatorAddress` is not equal to `address(0)`.
- `setOperatorFeeRecipientAddress` should check that `_newOperatorFeeRecipientAddress` is not equal to `address(0)`.
- `setOperatorName` should check that `_newName` is not an empty string.

## Oracle.1.sol

- `initOracleV1` should require the `_admin` parameter to be not equal to `address(0)`. This check is not needed if the issue with `LibOwnable._setAdmin` allows setting `address(0)` as the admin of the contract is implemented directly at `LibOwnable._setAdmin` level. Consider also adding some min and max limit to the values of `_annualAprUpperBound` and `_relativeLowerBound`, and ensure that `_epochsPerFrame`, `_slotsPerEpoch`, `_secondsPerSlot`, and `_genesisTime` match the expected values.
- `addMember` should check that `_newOracleMember` is not equal to `address(0)`.
- `setBeaconBounds`: Consider adding min/max values that `_annualAprUpperBound` and `_relativeLowerBound` should respect.

## River.1.sol

- `initRiverV1`: 
  - `_globalFee` should follow the same validation done in `setGlobalFee`. Note that the client said 0 is a valid `_globalFee` value. 
    > "The revenue redistribution would be computed off-chain and paid by the treasury in that case. It's still an ongoing discussion they're having at Alluvial."
  - `_operatorRewardsShare` should follow the same validation done in `setOperatorRewardsShare`. Note that the client said 0 is a valid `_operatorRewardsShare` value.
    > "The revenue redistribution would be computed off-chain and paid by the treasury in that case. It's still an ongoing discussion they're having at Alluvial."

## ConsensusLayerDepositManager.1.sol

- `initConsensusLayerDepositManagerV1`: `_withdrawalCredentials` should not be empty and follow the requirements expressed in the following official Consensus Specs document.

## Recommendation

Consider implementing all the checks suggested above. 

### Alluvial

Recommendation implemented in `SPEARBIT/10`. Some validation checks, like ensuring the admin is not `address(0)`, will be addressed in another PR.

### Spearbit

Only an empty check is performed on `_withdrawalCredentials`. `_annualAprUpperBound` and `_relativeLowerBound` are still not checked in both `initOracleV1` and `setReportBounds`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Initialization`

