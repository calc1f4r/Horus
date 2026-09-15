---
# Core Classification
protocol: Auxo Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60569
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
source_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
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
finders_count: 4
finders:
  - Ed Zulkoski
  - Ruben Koch
  - Cameron Biniamow
  - Mostafa Yassin
---

## Vulnerability Title

Missing Input Validation

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Mitigated" by the client. Addressed in: `6c2cd78ac298f52516c64d0d48e7db706d0cb12b`.

The client provided the following explanation:

Quantstamp correctly notes that some variables do not have validations for null checks or known erroneous values. We subdivide these errors into:

• Initialization validation: missing validations during contract deployment and/or initialization

• Runtime validation: missing validations for values that can be changed over the contract lifetime

• For initialization validation, we acknowledge the risks, instead opting for runtime, pre and post deploy health checks to ensure all variables are set as expected. These health checks are in the form of foundry scripts, although they have not themselves been subject to a formal audit. The scripts cover the following issues raised:

• StakingManager.sol: all values

• Governor.sol: all values

• RollStaker.sol: all values

• TokenLocker: min duration, max duration, min lock amount

• For runtime validation, here are the specific comments:

• Migrator.sol.setMigrationEnabled: covered by deploy scripts mentioned above

• TokenLocker.sol.setXAuxo: covered by deploy scripts and not expected to change

• xAuxo.sol.setEntryFee/constructor: risk of setting fee without beneficiary is bourne by operator

• EarlyTermination.sol.setPenaltyBeneficiary: risk of setting incorrect address is bourne by operator

• MerkleDistribution.sol.setLock: risk of setting incorrect block number is bourne by operator

• The following 3 cases were flagged for missing validation but have reverts further down the call stack:

• TokenLocker.sol.depositByMonths: veAUXO reverts on mint to Zero Address

• TokenLocker.sol: getDuration(months) is called in depositByMonts, and increaseByMonths. Both these functions validate the passed months inside getLockMultiplier.

• xAUXO._depositAndStake: _account will revert if minting to the zero address as it is OpenZeppelin

**File(s) affected:**`StakingManager.sol`, `EarlyTermiantion.sol`, `Migrator.sol`, `Governor.sol`, `xAUXO.sol`, `MerkleDistributor.sol`, `RollStaker.sol`

**Description:** The following inputs need to be checked

• In `StakingManager.sol`, check `initialize._auxo` against the `0x0` address.

• In `StakingManager.sol`, check `initialize._veAuxo` against the `0x0` address.

• In `StakingManager.sol`, check `initialize.governor` against the `0x0` address.

• In `StakingManager.sol`, check `initialize.tokenLocker` against the `0x0` address.

• In `EarlyTermination.sol`, check `setPenaltyBeneficiary.penaltyBeneficiary` against the `0x0` address.

• In `Migrator.sol`, check `setMigrator._migrator` against the `0x0` address.

• In `Migrator.sol`, check the `migrator` against the `0x0` address in `setMigrationEnabled()`.

• In `Governor.sol`, `constructor` is missing validation for all inputs.

• In `TokenLocker.sol`, `initialize._minLockAmount` should be > 0.

• In `TokenLocker.sol`, `initialize._maxLockDuration` should be <= `getDuration(maxRatioArray.length)`.

• In `TokenLocker.sol`, `initialize.minLockDuration` should be >= `getDuration(6)`, or else the multiplier results will revert.

• In `TokenLocker.sol`, `depositByMonths()` should check that`_receiver` is not the `0x0` address; and `getDuration(_months)` is >= `minLockDuration`.

• In `TokenLocker.sol`, check `setxAUXO._xAUXO` against the `0x0` address.

• In `xAUXO.sol`, `constructor()` should check that `entryFee` and `feeBeneficiary` are only settable if `_entryFees` is not zero and`_feeBeneficiary` is not the `0x0` address.

• In `xAUXO.sol`, `setEntryFee()` should revert if the `feeBeneficiary` is the `0x0` address. Or else, fees can potentially be sent off to the `0x0` address. Additionally, `setFeePolicy()` would then need to swap the function calls.

• In `xAUXO.sol`, check `_depositAndStake._account` against the `0x0` address.

• In `MerkleDistributor.sol`, `setLock()` should check that `_lock` is greater than or equal to `block.number`.

• In `RollStaker.sol`, check `constructor.stakingToken` against the `0x0` address.

**Recommendation:** Consider adding the suggested missing input validations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Auxo Governance |
| Report Date | N/A |
| Finders | Ed Zulkoski, Ruben Koch, Cameron Biniamow, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html

### Keywords for Search

`vulnerability`

