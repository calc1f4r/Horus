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
solodit_id: 2128
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-abranft-contest
source_link: https://code4rena.com/reports/2022-04-abranft
github_link: https://github.com/code-423n4/2022-04-abranft-findings/issues/37

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
finders_count: 9
finders:
  - BowTiedWardens
  - cccz
  - horsefacts
  - gzeon
  - catchup
---

## Vulnerability Title

[H-03] Critical Oracle Manipulation Risk by Lender

### Overview


A bug has been found in the `NFTPairWithOracle` contract, which allows a malicious lender to change the Oracle used once a loan is outstanding and seize the collateral at the expense of the borrower. This could happen if the actual value of the collateral has increased significantly and is higher than the amount the lender is owed (principal + interest). 

The bug was identified through manual review. The `require` statement from line 205 to 211 does not check if `params.oracle` and `cur.oracle` are the same. The malicious lender could pass in their own `oracle` after the loan becomes outstanding, and the change would be reflected in line 221. In line 287, the tampered Oracle could produce a very low `rate` such that line 288 would pass, allowing the lender to seize the collateral, hurting the borrower. 

To mitigate this risk, a check should be added in the `require` statement in line 205 - 211 that `params.oracle == cur.oracle`. This will ensure that the Oracle used cannot be changed after the loan is agreed to, protecting the borrower from malicious lenders.

### Original Finding Content

_Submitted by 0x1337, also found by catchup, cccz, kenzo, GimelSec, BowTiedWardens, gzeon, horsefacts, and hyh_

<https://github.com/code-423n4/2022-04-abranft/blob/5cd4edc3298c05748e952f8a8c93e42f930a78c2/contracts/NFTPairWithOracle.sol#L286-L288>

<https://github.com/code-423n4/2022-04-abranft/blob/5cd4edc3298c05748e952f8a8c93e42f930a78c2/contracts/NFTPairWithOracle.sol#L200-L211>

The intended use of the Oracle is to protect the lender from a drop in the borrower's collateral value. If the collateral value goes up significantly and higher than borrowed amount + interest, the lender should not be able to seize the collateral at the expense of the borrower. However, in the `NFTPairWithOracle` contract, the lender could change the Oracle once a loan is outstanding, and therefore seize the collateral at the expense of the borrower, if the actual value of the collateral has increased significantly. This is a critical risk because borrowers asset could be lost to malicious lenders.

### Proof of Concept

In `NFTPairWithOracle`, the `params` are set by the `borrower` when they call `requestLoan()`, including the Oracle used. Once a lender agrees with the parameters and calls the `lend()` function, the `loan.status` changes to `LOAN_OUTSTANDING`.

Then, the lender can call the `updateLoanParams()` function and pass in its own `params` including the Oracle used. The `require` statement from line 205 to 211 does not check if `params.oracle` and `cur.oracle` are the same. A malicious lender could pass in his own `oracle` after the loan becomes outstanding, and the change would be reflected in line 221.

<https://github.com/code-423n4/2022-04-abranft/blob/5cd4edc3298c05748e952f8a8c93e42f930a78c2/contracts/NFTPairWithOracle.sol#L200-L211>

In a situation where the actual value of the collateral has gone up by a lot, exceeding the amount the lender is owed (principal + interest), the lender would have an incentive to seize the collateral. If the Oracle is not tampered with, lender should not be able to do this, because line 288 should fail. But a lender could freely change Oracle once the loan is outstanding, then a tampered Oracle could produce a very low `rate` in line 287 such that line 288 would pass, allowing the lender to seize the collateral, hurting the borrower.

<https://github.com/code-423n4/2022-04-abranft/blob/5cd4edc3298c05748e952f8a8c93e42f930a78c2/contracts/NFTPairWithOracle.sol#L286-L288>

### Recommended Mitigation Steps

Once a loan is agreed to, the oracle used should not change. I'd recommend adding a check in the `require` statement in line 205 - 211 that `params.oracle == cur.oracle`

**[cryptolyndon (AbraNFT) confirmed and commented](https://github.com/code-423n4/2022-04-abranft-findings/issues/37#issuecomment-1118104950):**
 > Confirmed, this is bad. First report of this particular exploit.



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
| Finders | BowTiedWardens, cccz, horsefacts, gzeon, catchup, hyh, 0x1337, GimelSec, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-abranft
- **GitHub**: https://github.com/code-423n4/2022-04-abranft-findings/issues/37
- **Contest**: https://code4rena.com/contests/2022-04-abranft-contest

### Keywords for Search

`vulnerability`

