---
# Core Classification
protocol: Shyft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56572
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-12-Shyft.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missing checks to distinguish staked funds and reward funds

### Overview


The report discusses a bug in the ShyftStaking contract that could potentially cause rewards to exceed the actual distributed value. This is because the contract does not have checks in place to prevent this from happening. The recommendation is to add checks to ensure that rewards do not exceed the distributed value.

### Original Finding Content

**Description**

ShyftStaking.sol, unstake(), finishPrePurchasersMode(), _getReward()
The contract operates with the same currency for the rewards and for the user stakes. In spite
of the stakes being tracked within totalSupply variable, there are no checks against that value
during the rewards distribution or transfers to the users.
So, in order to mitigate possible scenarios where (as an effect of the calculations with edge
cases parameters) rewards amount may exceed the actual distributed value (and get the part
of the supplied funds) we recommend to add checks that reward amount does not exceed the
distributed value. So, in order to mitigate possible scenarios where (as an effect of the
calculations with edge cases parameters) rewards amount may exceed the actual distributed
value (and get the part of the supplied funds) we recommend to add checks that reward
amount does not exceed the distributed value.

**Recommendation**:

For the rewards transfers add checks like: rewardToTransfer <=
address(this).balance.sub(totalSupply).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Shyft |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-12-Shyft.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

