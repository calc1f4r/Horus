---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28716
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#flawed-stable-debt-calculation-due-to-timestamp-mismatch
github_link: none

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
  - MixBytes
---

## Vulnerability Title

Flawed Stable Debt Calculation Due to Timestamp Mismatch

### Overview


The bug report describes an issue with the code found at https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/libraries/logic/ReserveLogic.sol#L341-L347. The code calculates the stable debt using the current stable debt which results in the stable debt difference not being taken into account and the processed stable debt increment not being recorded. 

The recommendation is to treat `vars.principalStableDebt` as the previous stable debt and update `StableDebtToken`'s `_totalSupply` and `_totalSupplyTimestamp` after the operation. This will ensure that the stable debt difference is taken into account and the processed stable debt increment is recorded.

### Original Finding Content

##### Description
https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/libraries/logic/ReserveLogic.sol#L341-L347 

Value `vars.previousStableDebt` calculated this way is actually the current stable debt and always equals to `vars.currentStableDebt`.

```solidity
//calculate the stable debt until the last timestamp update
vars.cumulatedStableInterest = MathUtils.calculateCompoundedInterest(
  vars.avgStableRate,
  vars.stableSupplyUpdatedTimestamp
);

vars.previousStableDebt = vars.principalStableDebt.rayMul(vars.cumulatedStableInterest);
```

As a result, the stable debt difference is not taken into account. Moreover, the processed stable debt increment is not recorded in any way.
##### Recommendation
One possible solution is to treat `vars.principalStableDebt` as the previous stable debt and update `StableDebtToken`'s `_totalSupply` and `_totalSupplyTimestamp` after the operation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#flawed-stable-debt-calculation-due-to-timestamp-mismatch
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

