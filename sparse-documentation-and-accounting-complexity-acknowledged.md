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
solodit_id: 13209
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
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

Sparse documentation and accounting complexity  Acknowledged

### Overview


This bug report concerns the lack of documentation in the Rocketpool system, which has grown in complexity and makes it difficult to trace the flow of funds through the system. Inline comments are either sparse or missing altogether, and few technical documents about the system's design rationale are available. This increases the likelihood of developer error and makes it harder to introduce new developers to the code base. It is essential that documentation not only outlines what is being done but also why and what a function’s role in the system’s “bigger picture” is. 

The client has acknowledged the finding and agreed to address the issue. It is recommended that the number of inline comments and general technical documentation be significantly increased, and that ways be explored to centralize the system’s accounting further. Where the flow of funds is obscured because multiple components or multi-step processes are involved, extensive inline documentation should be added to give context.

### Original Finding Content

#### Resolution



The client acknowledges the finding and provided the following statement:



> 
> Acknowledged and agree.
> 
> 
> 




#### Description


Throughout the project, inline documentation is either sparse or missing altogether. Furthermore, few technical documents about the system’s design rationale are available. The recent releases' increased complexity makes it significantly harder to trace the flow of funds through the system as components change semantics, are split into separate contracts, etc.


It is essential that documentation not only outlines what is being done but also *why* and what a function’s role in the system’s “bigger picture” is. Many comments in the code base fail to fulfill this requirement and are thus redundant, e.g.


**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L292-L293**



```
// Sanity check that refund balance is zero
require(nodeRefundBalance == 0, "Refund balance not zero");

```
**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L333-L334**



```
// Remove from vacant set
rocketMinipoolManager.removeVacantMinipool();

```
**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L381-L383**



```
if (ownerCalling) {
    // Finalise the minipool if the owner is calling
    \_finalise();

```
The increased complexity and lack of documentation can increase the likelihood of developer error. Furthermore, the time spent maintaining the code and introducing new developers to the code base will drastically increase. This effect can be especially problematic in the system’s accounting of funds as the various stages of a Minipool imply different flows of funds and interactions with external dependencies. Documentation should explain the rationale behind specific hardcoded values, such as the magic `8 ether` boundary for withdrawal detection. An example of a lack of documentation and distribution across components is the calculation and influence of `ethMatched` as it plays a role in:


* the minipool bond reducer,
* the node deposit contract,
* the node manager, and
* the node staking contract.


#### Recommendation


As the Rocketpool system grows in complexity, we highly recommend significantly increasing the number of inline comments and general technical documentation and exploring ways to centralize the system’s accounting further to provide a clear picture of which funds move where and at what point in time. Where the flow of funds is obscured because multiple components or multi-step processes are involved, we recommend adding extensive inline documentation to give context.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

