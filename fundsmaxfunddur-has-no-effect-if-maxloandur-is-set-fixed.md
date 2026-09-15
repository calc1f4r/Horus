---
# Core Classification
protocol: Atomic Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 14001
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/atomic-loans/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Steve Marx

---

## Vulnerability Title

Funds.maxFundDur has no effect if maxLoanDur is set ✓ Fixed

### Overview


This bug report is about the `Funds.maxFundDur` feature in the AtomicLoans/atomicloans-eth-contracts repository. This feature should specify the maximum amount of time a fund should be active, and is checked in the `request()` function to ensure the duration of the loan won't exceed that time. However, when the `maxLoanDur` parameter is set, the check is skipped. 

For example, if a user sets `maxLoanDur` to 1 week and sets the `maxFundDur` to December 1st, then there can actually be a loan that ends on December 7th.

The resolution for this bug is to check against `maxFundDur` even when `maxLoanDur` is set. This fix is available in the [AtomicLoans/atomicloans-eth-contracts#68](https://github.com/AtomicLoans/atomicloans-eth-contracts/pull/68) pull request.

### Original Finding Content

#### Resolution



This is fixed in [AtomicLoans/atomicloans-eth-contracts#68](https://github.com/AtomicLoans/atomicloans-eth-contracts/pull/68).


#### Description


`Funds.maxFundDur` specifies the maximum amount of time a fund should be active. It’s checked in `request()` to ensure the duration of the loan won’t exceed that time, but the check is skipped if `maxLoanDur` is set:


**code/ethereum/contracts/Funds.sol:L510-L514**



```
if (maxLoanDur(fund) > 0) {
    require(loanDur\_       <= maxLoanDur(fund));
} else {
    require(now + loanDur\_ <= maxFundDur(fund));
}

```
#### Examples


If a user sets `maxLoanDur` (the maximum loan duration) to 1 week and sets the `maxFundDur` (timestamp when all loans should be complete) to December 1st, then there can actually be a loan that ends on December 7th.


#### Recommendation


Check against `maxFundDur` even when `maxLoanDur` is set.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Atomic Loans |
| Report Date | N/A |
| Finders | Steve Marx
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/atomic-loans/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

