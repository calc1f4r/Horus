---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28732
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Vault%20V2%20(Vyper%20part)/README.md#2-potential-issue-with-re-entrancy
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
  - MixBytes
---

## Vulnerability Title

Potential issue with re-entrancy

### Overview


This bug report is about the method `report` in the Vault.vy contract. The method is called by a strategy and makes an external call back to the same strategy in the `_assessFees` method. This could potentially create a problem if the strategy is broken or hacked, as it could call back to the vaults methods while the current state is not finalized.

The recommendation is to add re-entrancy checks to the code to avoid any potential problems. This is especially important as the code logic is complicated, and it is easy to accidentally introduce bugs in the future.

### Original Finding Content

##### Description
Method `report` at this [line](https://github.com/iearn-finance/yearn-vaults/blob/054034304c7912d227d460feadc23177103de0b9/contracts/Vault.vy#L1246) called by strategy makes an external call back to strategy in `_assessFees` method: https://github.com/iearn-finance/yearn-vaults/blob/054034304c7912d227d460feadc23177103de0b9/contracts/Vault.vy#L1239. So broken or hacked, strategy can call back vaults methods while the current state is not finalized.

##### Recommendation
We recommend adding re-entrancy checks to avoid potential problems. Especially when the code logic is complicated even if for now the code is safe, in future it's really easy to implicitly introduce some bugs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Vault%20V2%20(Vyper%20part)/README.md#2-potential-issue-with-re-entrancy
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

