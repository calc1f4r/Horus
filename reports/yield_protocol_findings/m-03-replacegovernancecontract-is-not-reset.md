---
# Core Classification
protocol: AdapterFinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58086
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] replaceGovernanceContract is not reset

### Overview


This bug report discusses an issue where after replacing the governance, the vote count is not reset to 0. This can lead to a situation where a guard can change the governance back to a previous contract without proper voting. The report recommends resetting the vote count to 0.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

After the governance is replaced, the VotesGCByVault is not reset to 0. This can lead to a situation where if the governance for the vault is reverted back to a previous contract, the vote count is still recorded, allowing a guard to change it back without proper voting. For example, consider governance contracts A and B: A is voted to be replaced by B. If B has a problem or bug and is replaced back by A, the vote count for B is still recorded. A guard can then vote to change it back to B immediately without proper voting.

```python
@external
def replaceGovernance(NewGovernance: address, vault: address):
    ...
    #Add Vote to VoteCount
    for guard_addr in self.LGov:
        if self.VotesGCByVault[vault][guard_addr] == NewGovernance:
            VoteCount += 1

    if len(self.LGov) == VoteCount:
        AdapterVault(vault).replaceGovernanceContract(NewGovernance)
```

## Recommendations

Reset `VotesGCByVault` to 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AdapterFinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

