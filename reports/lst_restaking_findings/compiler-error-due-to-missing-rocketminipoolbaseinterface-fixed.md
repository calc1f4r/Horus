---
# Core Classification
protocol: Rocket Pool Atlas (v1.2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13217
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Compiler error due to missing RocketMinipoolBaseInterface ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Fixed in <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6> by adding the missing interface file.


#### Description


The interface `RocketMinipoolBaseInterface` is missing from the code repository. Manually generating the interface and adding it to the repository fixes the error.



```
⇒  npx hardhat compile
Error HH404: File ../../interface/minipool/RocketMinipoolBaseInterface.sol, imported from contracts/contract/minipool/RocketMinipoolBase.sol, not found.

For more info go to https://hardhat.org/HH404 or run Hardhat with --show-stack-traces

```
#### Recommendation


Add the missing source unit to the repository.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocket Pool Atlas (v1.2) |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

