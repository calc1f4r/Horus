---
# Core Classification
protocol: Nayms 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60768
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
source_link: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
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
finders_count: 6
finders:
  - Jonathan Mevs
  - Andy Lin
  - Roman Rohleder
  - Jeffrey Kam
  - Martinet Lee
---

## Vulnerability Title

Invalid Entity Update

### Overview


This bug report describes an issue with the `LibEntity.sol` file in the code. The problem is that when updating an Entity, there are not enough checks to ensure that the Entity is in a valid state. This can lead to the Entity being unable to write new policies. The function `LibEntity._updateEntity()` has a check to make sure the `utilizedCapacity` of the new Entity does not exceed the `maxCapacity`, but it does not check if the `newUtilizedCapacity` (calculated when a new `collateralRatio` is assigned) also exceeds the `maxCapacity`. This means that an Entity can be updated with a `utilizedCapacity` that is too high, which will prevent it from being able to write policies. The report recommends adding a check for the `newUtilizedCapacity` and only updating the `utilizedCapacity` if the `collateralRatio` has changed. The issue has been marked as "Fixed" by the client and the code has been updated to address the problem.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `7fbedc365421a5f389cecf1fa2fa33c1920967c2`. Both items were fixed.

**File(s) affected:**`LibEntity.sol`

**Description:** The lack of crucial checks when updating an Entity allows for an invalid state to persist on an Entity, ultimately denying the ability of this Entity to write new policies. In the function `LibEntity._updateEntity()`, `validateEntity()` is called to check that the `utilizedCapacity` of the new Entity does not exceed the `maxCapacity` for that Entity. In the case where there is a new `collateralRatio` being assigned to the Entity, there is a `newUtilizedCapacity` calculated for the Entity. This `newUtilizedCapacity` is not checked to ensure that it does not exceed the specified `maxCapacity`. As a result, an Entity can be updated to have a `utilizedCapacity` that exceeds the `maxCapacity`, which would deny the ability of this Entity to pass the checks required to write new policies.

Currently, the balance of the Entity and the updated values are only checked if there is an update to the `collateralRatio` of the Entity. In the case where the `collateralRatio` of the Entity is not being updated, you can have an updated `utilizedCapacity` that exceeds the internal balance of that Entity. More generally, it appears that the `utilizedCapacity` of an Entity can be updated, even if the `collateralRatio` has not been updated. Logically, the utilized capacity of an Entity should only be updated if the collateral ratio is changed.

**Recommendation:** Ensure that the new `utilizedCapacity` does not exceed the `maxCapacity` of that Entity or the internal balance of that Entity. Additionally, consider only updating the `utilizedCapacity` of an Entity if the `collateralRatio` changes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nayms 2 |
| Report Date | N/A |
| Finders | Jonathan Mevs, Andy Lin, Roman Rohleder, Jeffrey Kam, Martinet Lee, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html

### Keywords for Search

`vulnerability`

