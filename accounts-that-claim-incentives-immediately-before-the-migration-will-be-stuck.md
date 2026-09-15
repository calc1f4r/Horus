---
# Core Classification
protocol: Notional Protocol V2.1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13274
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/notional-protocol-v2.1/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  Jasper Hepp

  - Heiko Fisch
  -  Elias Leers
---

## Vulnerability Title

Accounts that claim incentives immediately before the migration will be stuck

### Overview


This bug report is about an issue related to a new incentive calculation for accounts that existed before the migration. The problem occurs when an account claims incentives immediately before the migration happens, in the same block. In this case, the division in the last line of the code will throw an error, and the account will be stuck. The recommended solution is to return 0 if `finalMigrationTime` and `lastClaimTime` are equal, and also to rename the variable `timeSinceMigration` to something more accurate.

### Original Finding Content

#### Description


For accounts that existed before the migration to the new incentive calculation, the following happens when they claim incentives for the first time after the migration: First, the incentives that are still owed from before the migration are computed according to the old formula; the incentives *since* the migration are calculated according to the new logic, and the two values are added together. The first part – calculating the pre-migration incentives according to the old formula – happens in function `MigrateIncentives.migrateAccountFromPreviousCalculation`; the following lines are of particular interest in the current context:


**code-582dc37/contracts/external/MigrateIncentives.sol:L39-L50**



```
uint256 timeSinceMigration = finalMigrationTime - lastClaimTime;

// (timeSinceMigration \* INTERNAL\_TOKEN\_PRECISION \* finalEmissionRatePerYear) / YEAR
uint256 incentiveRate =
    timeSinceMigration
        .mul(uint256(Constants.INTERNAL\_TOKEN\_PRECISION))
        // Migration emission rate is stored as is, denominated in whole tokens
        .mul(finalEmissionRatePerYear).mul(uint256(Constants.INTERNAL\_TOKEN\_PRECISION))
        .div(Constants.YEAR);

// Returns the average supply using the integral of the total supply.
uint256 avgTotalSupply = finalTotalIntegralSupply.sub(lastClaimIntegralSupply).div(timeSinceMigration);

```
The division in the last line will throw if `finalMigrationTime` and `lastClaimTime` are equal. This will happen if an account claims incentives immediately before the migration happens – where “immediately” means in the same block. In such a case, the account will be stuck as any attempt to claim incentives will revert.


#### Recommendation


The function should return `0` if `finalMigrationTime` and `lastClaimTime` are equal. Moreover, the variable name `timeSinceMigration` is misleading, as the variable doesn’t store the time since the migration but the time between the last incentive claim and the migration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Notional Protocol V2.1 |
| Report Date | N/A |
| Finders |  Jasper Hepp
, Heiko Fisch,  Elias Leers |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/notional-protocol-v2.1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

