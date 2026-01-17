---
# Core Classification
protocol: Wallek
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35377
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Unoptimized change of object values.

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Resolved

**Description**
TestStake::reStake()#1957-1963,1934-1940.
In the loop, only the fields 'stakeAmount and 'claimTime of the iterated object are changed. However, instead of changing these fields, a new local object of the 'Stakes' structure is created, and the existing object is overwritten entirely. In the process, the 'startTime` and `endTime', read from the contract storage, and 'msg.sender are overwritten with the same values. This results in unnecessary gas consumption in the cycle. Instead, The auditors recommend modifying only the required fields of the structure and using a storage reference to the structure object. Also, use a storage reference for the 'stakeDetails mapping. Example:
```solidity
mapping (uint256 => Stakes) storage rStakeDetails =
stakeDetails[msg.sender];
Stakes storage rStake;
for (...) {
rStakerStakeDetails[i];
delete rStake.stakeAmount;
rStake.claimTime block.timestamp:
}
```
The same applies to the following parts:
• TestStake::stake()#1902-1908.
• TestStake::unStakeAll() #1985-1991.

**Recommendation:**

Modify only required values instead of overwriting an entire object and use storage references.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wallek |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

