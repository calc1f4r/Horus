---
# Core Classification
protocol: Geode Liquid Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20744
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/05/geode-liquid-staking/
github_link: none

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
finders_count: 2
finders:
  - Chingiz Mardanov
  -  Sergii Kravchenko

---

## Vulnerability Title

Validators Array Length Has to Be Updated When the Validator Is Alienated.

### Overview


In GeodeFi, when a node operator creates a validator with incorrect withdrawal credentials or signatures, the Oracle has the ability to alienate this validator. This process updates the validator's status, and additionally, the validator's count should be decreased in order for the monopoly threshold to be calculated correctly. This is because the length of the `validators` array is used twice in the `OpeartorAllowance` function. Without the update of the array length, the monopoly threshold as well as the time when the fallback operator will be able to participate is going to be computed incorrectly. To solve this issue, it could be beneficial to not refer to `rks.validators` in the operator allowance function and instead use the `rks.proposedValidators` + `rks.alienatedValidators` + `rks.activeValidators`. This way allowance function can always rely on the most up to date data.

### Original Finding Content

In GeodeFi when the node operator creates a validator with incorrect withdrawal credentials or signatures the Oracle has the ability to alienate this validator. In the process of alienation, the validator status is updated.


**contracts/Portal/modules/StakeModule/libs/OracleExtensionLib.sol:L111-L136**



```
function \_alienateValidator(
 SML.PooledStaking storage STAKE,
 DSML.IsolatedStorage storage DATASTORE,
 uint256 verificationIndex,
 bytes calldata \_pk
) internal {
 require(STAKE.validators[\_pk].index <= verificationIndex, "OEL:unexpected index");
 require(
 STAKE.validators[\_pk].state == VALIDATOR\_STATE.PROPOSED,
 "OEL:NOT all pubkeys are pending"
 );

 uint256 operatorId = STAKE.validators[\_pk].operatorId;
 SML.\_imprison(DATASTORE, operatorId, \_pk);

 uint256 poolId = STAKE.validators[\_pk].poolId;
 DATASTORE.subUint(poolId, rks.secured, DCL.DEPOSIT\_AMOUNT);
 DATASTORE.addUint(poolId, rks.surplus, DCL.DEPOSIT\_AMOUNT);

 DATASTORE.subUint(poolId, DSML.getKey(operatorId, rks.proposedValidators), 1);
 DATASTORE.addUint(poolId, DSML.getKey(operatorId, rks.alienValidators), 1);

 STAKE.validators[\_pk].state = VALIDATOR\_STATE.ALIENATED;

 emit Alienated(\_pk);
}

```
An additional thing that has to be done during the alienation process is that the validator’s count should be decreased in order for the monopoly threshold to be calculated correctly. That is because the length of the `validators` array is used twice in the `OpeartorAllowance` function:


**contracts/Portal/modules/StakeModule/libs/StakeModuleLib.sol:L975**



```
uint256 numOperatorValidators = DATASTORE.readUint(operatorId, rks.validators);

```
**contracts/Portal/modules/StakeModule/libs/StakeModuleLib.sol:L988**



```
uint256 numPoolValidators = DATASTORE.readUint(poolId, rks.validators);

```
Without the update of the array length, the monopoly threshold as well as the time when the fallback operator will be able to participate is going to be computed incorrectly.


It could be beneficial to not refer to `rks.validators` in the operator allowance function and instead use the `rks.proposedValidators` + `rks.alienatedValidators` + `rks.activeValidators`. This way allowance function can always rely on the most up to date data.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geode Liquid Staking |
| Report Date | N/A |
| Finders | Chingiz Mardanov,  Sergii Kravchenko
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/05/geode-liquid-staking/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

