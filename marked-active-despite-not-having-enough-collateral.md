---
# Core Classification
protocol: Interplanetary Consensus (Ipc)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37363
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
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

Marked active despite not having enough collateral

### Overview


This bug report discusses a medium severity issue that has been resolved in the codebase. The problem was found in the `register()` function of the GatewayManagerFacet.sol file, where collateral was not being properly checked to ensure it was greater than a minimum stake amount. This resulted in subnets being marked as active even when they did not meet the required stake amount. The recommendation is to implement a validation method to fix this issue. The bug has been fixed in the latest codebase by removing the line of code that caused the issue. The client has also confirmed that the vulnerability no longer exists in the updated code.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

GatewayManagerFacet.sol - In `register()` function, collateral is not being validated to be greater than `s.minStake`. Consequently we end up having a subnet status marked as Status.Active as shown in the following:
```solidity
        subnet.id = subnetId;
        subnet.stake = collateral;
        subnet.status = Status.Active;
        subnet.genesisEpoch = block.number;
        subnet.circSupply = genesisCircSupply;
```
Noting that this contradicts the implementation of addStake function which asserts that the stake becomes greater than a given threshold (i.e. s.minStake) in order to have an active status as shown in the following:
```solidity
       if (subnet.status == Status.Inactive) {
            if (subnet.stake >= s.minStake) {
                subnet.status = Status.Active;
            }
        }
```
**Recommendation**

Apply the required validation method to ensure that collateral is the intended value to have an active subnet. 
**Fix**: Issue is fixed in commit 2440ac2 by removing   `subnet.status = Status.Active;`. Therefore the subnet is no longer marked active on calling register to avoid that mislabelling if collateral is not enough.
**Client comment**: Invalid. There is no such vulnerability in the latest codebase after implementing changes in the protocol - https://www.google.com/url?q=https://github.com/consensus-shipyard/ipc-monorepo/blob/main/contracts/src/subnet/SubnetActorManagerFacet.sol%23L107-L254&sa=D&source=docs&ust=1704927823490184&usg=AOvVaw3-GVrDm8nvR39T5f8sH0Xv

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Interplanetary Consensus (Ipc) |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

