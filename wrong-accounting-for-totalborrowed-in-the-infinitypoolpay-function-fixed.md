---
# Core Classification
protocol: Glif Filecoin InfinityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21974
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/04/glif-filecoin-infinitypool/
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Chingiz Mardanov
  -  Sergii Kravchenko

---

## Vulnerability Title

Wrong Accounting for totalBorrowed in the InfinityPool.pay Function ✓ Fixed

### Overview


This bug report is about a problem with the InfinityPool.sol file, which is part of the GLIF Confidential Pool project. The issue is that if an Agent pays more than the current interest debt, the remaining payment is being accounted as repayment of the principal debt. This is due to two mistakes in the calculation, which should be fixed. The first mistake is that the calculation should be done using the `totalBorrowed` value instead of `0`. The second mistake is that the `principalPaid` cannot be larger than the `account.principal` in that calculation. The resolution is addressed as recommended in two pull requests.

### Original Finding Content

#### Resolution



Addressed as recommended in two pull rquests: [1](https://github.com/glif-confidential/pools/pull/441/files), [2](https://github.com/glif-confidential/pools/pull/496/files).


#### Description


If the Agent pays more than the current interest debt, the remaining payment will be accounted as repayment of the principal debt:


**src/Pool/InfinityPool.sol:L382-L401**



```
// pay interest and principal
principalPaid = vc.value - interestOwed;
// the fee basis only applies to the interest payment
feeBasis = interestOwed;
// protect against underflow
totalBorrowed -= (principalPaid > totalBorrowed) ? 0 : principalPaid;
// fully paid off
if (principalPaid >= account.principal) {
 // remove the account from the pool's list of accounts
 GetRoute.agentPolice(router).removePoolFromList(vc.subject, id);
 // return the amount of funds overpaid
 refund = principalPaid - account.principal;
 // reset the account
 account.reset();
} else {
 // interest and partial principal payment
 account.principal -= principalPaid;
 // move the `epochsPaid` cursor to mark the account as "current"
 account.epochsPaid = block.number;
}

```
Let’s focus on the `totalBorrowed` changes:


**src/Pool/InfinityPool.sol:L387**



```
totalBorrowed -= (principalPaid > totalBorrowed) ? 0 : principalPaid;

```
This value is supposed to be decreased by the principal that is repaid. So there are 2 mistakes in the calculation:


* Should be `totalBorrowed` instead of `0`.
* The `principalPaid` cannot be larger than the `account.principal` in that calculation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Glif Filecoin InfinityPool |
| Report Date | N/A |
| Finders | Chingiz Mardanov,  Sergii Kravchenko
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/04/glif-filecoin-infinitypool/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

