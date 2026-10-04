---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2130
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-abranft-contest
source_link: https://code4rena.com/reports/2022-04-abranft
github_link: https://github.com/code-423n4/2022-04-abranft-findings/issues/55

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
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - WatchPug
  - catchup
  - hyh
  - gzeon
---

## Vulnerability Title

[H-05] Mistake while checking LTV to lender accepted LTV

### Overview


A bug report has been filed for the code in the file NFTPairWithOracle.sol, located at line 316. The issue is that the code comments in the _lend() function that the lender accepted conditions must be at least as good as the borrower is asking for. However, the code is checking for the opposite, which could potentially strand the lender if they enter a lower LTV than the borrower. As an example, if the borrower is asking for an LTV of 86%, but the lender enters an accepted LTV of 80%, then the lend() function will execute with an LTV of 86%, punishing the lender. The bug was found using manual analysis, and the recommended mitigation steps are to change the condition as: params.ltvBPS <= accepted.ltvBPS.

### Original Finding Content

_Submitted by catchup, also found by WatchPug, gzeon, and hyh_

It comments in the `\_lend()` function that lender accepted conditions must be at least as good as the borrower is asking for.
The line which checks the accepted LTV (lender's LTV) against borrower asking LTV is:
`params.ltvBPS >= accepted.ltvBPS`,
This means lender should be offering a lower LTV, which must be the opposite way around.
I think this may have the potential to strand the lender, if he enters a lower LTV.
For example borrower asking LTV is 86%. However, lender enters his accepted LTV as 80%.
lend() will execute with 86% LTV and punish the lender, whereas it should revert and acknowledge the lender that his bid is not good enough.

### Proof of Concept

<https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L316>

### Recommended Mitigation Steps

The condition should be changed as:
`params.ltvBPS <= accepted.ltvBPS`,

**[cryptolyndon (AbraNFT) confirmed and commented](https://github.com/code-423n4/2022-04-abranft-findings/issues/55#issuecomment-1118145958):**
 > Confirmed, and the first to note this particular issue.



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | WatchPug, catchup, hyh, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-abranft
- **GitHub**: https://github.com/code-423n4/2022-04-abranft-findings/issues/55
- **Contest**: https://code4rena.com/contests/2022-04-abranft-contest

### Keywords for Search

`vulnerability`

