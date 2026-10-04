---
# Core Classification
protocol: zkSync – L1 Diff Audit (February 2023)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10307
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-l1-diff-audit-february-2023/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - lending
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Deposit cap not updated on withdrawals

### Overview


This bug report is about a problem with user deposits being capped by an increasing counter, but the counter not being decreased by withdrawals. This can lead to users being locked out of depositing again after making their first deposit and withdrawal, if the initial amount is larger than half the cap. The suggested solution is to decrease the per-user cap during withdrawals to allow users to return to the rollup. The Matter Labs team acknowledged the issue but stated that it is an accepted risk until the Full Launch Alpha, when the deposit limitations will be removed.

### Original Finding Content

User deposits are capped by [increasing the `totalDepositedAmountPerUser`](https://github.com/matter-labs/zksync-2-contracts/blob/3f345ce52bc378c4b5d710c80d817db170775049/ethereum/contracts/zksync/facets/Mailbox.sol#L266) counter. However, the counter is not decreased by withdrawals.


As the counter can only be increased, after sufficient usage, all withdrawing users will be locked out of depositing again. This can possibly happen right after the first deposit and withdrawal, if the initial amount is larger than half the cap.


Consider decreasing the per-user cap during withdrawals to allow users to return to the rollup.


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *The deposit limitations are only enabled in Fair Onboarding Alpha, while only approved partners may deposit funds. This will be removed at Full Launch Alpha, so we treat this issue as an accepted risk.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync – L1 Diff Audit (February 2023) |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-l1-diff-audit-february-2023/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

