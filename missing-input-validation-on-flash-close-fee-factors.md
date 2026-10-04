---
# Core Classification
protocol: Fuji Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16530
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
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
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Missing input validation on flash close fee factors

### Overview


The `FliquidatorFTM` contract is used by authorized parties to set the flash close fee factor, which is provided as two integers denoting numerator and denominator. A bug in the contract allows users to set unrealistically high factors, which go well above 1, which can have unexpected effects on internal accounting and the impact of flashloan balances. To fix this issue, a requirement should be added to make sure that `flashCloseF.a <= flashCloseF.b`.

### Original Finding Content

#### Description


The `FliquidatorFTM` contract allows authorized parties to set the flash close fee factor. The factor is provided as two integers denoting numerator and denominator. Due to a lack of boundary checks, it is possible to set unrealistically high factors, which go well above 1. This can have unexpected effects on internal accounting and the impact of flashloan balances.


#### Examples


**code/contracts/fantom/FliquidatorFTM.sol:L657-L659**



```
function setFlashCloseFee(uint64 \_newFactorA, uint64 \_newFactorB) external isAuthorized {
 flashCloseF.a = \_newFactorA;
 flashCloseF.b = \_newFactorB;

```
#### Recommendation


Add a requirement making sure that `flashCloseF.a <= flashCloseF.b`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fuji Protocol |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

