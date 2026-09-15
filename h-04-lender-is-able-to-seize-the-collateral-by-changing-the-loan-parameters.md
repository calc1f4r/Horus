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
solodit_id: 2129
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-abranft-contest
source_link: https://code4rena.com/reports/2022-04-abranft
github_link: https://github.com/code-423n4/2022-04-abranft-findings/issues/51

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
finders_count: 7
finders:
  - IllIllI
  - BowTiedWardens
  - scaraven
  - Ruhum
  - gzeon
---

## Vulnerability Title

[H-04] Lender is able to seize the collateral by changing the loan parameters

### Overview


This bug report is about a vulnerability in the NFTPairWithOracle.sol smart contract code. The vulnerability allows the lender to seize the collateral at any time by modifying the loan parameters. This is possible by setting the ltvBPS value to 0, which bypasses the requirement that the collateral must lose value or the borrower must not repay in time before the lender can seize the collateral. The steps to exploit this vulnerability are: lend funds to the borrower, call updateLoanParams() to set the ltvBPS value to 0, and call removeCollateral() to steal the collateral from the contract. To mitigate this vulnerability, the updateLoanParams() should not be allowed to change the ltvBPS value.

### Original Finding Content

_Submitted by Ruhum, also found by IllIllI, WatchPug, BowTiedWardens, gzeon, plotchy, and scaraven_

<https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L198-L223>

<https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L200-L212>

<https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L288>

The lender should only be able to seize the collateral if:

*   the borrower didn't repay in time
*   the collateral loses too much of its value

But, the lender is able to seize the collateral at any time by modifying the loan parameters.

### Proof of Concept

The [`updateLoanParams()`](https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L198-L223) allows the lender to modify the parameters of an active loan in favor of the borrower. But, by setting the `ltvBPS` value to `0` they are able to seize the collateral.

If `ltvBPS` is `0` the following require statement in `removeCollateral()` will always be true:

<https://github.com/code-423n4/2022-04-abranft/blob/main/contracts/NFTPairWithOracle.sol#L288>

`rate * 0 / BPS < amount` is always `true`.

That allows the lender to seize the collateral although its value didn't decrease nor did the time to repay the loan come.

So the required steps are:

1.  lend the funds to the borrower
2.  call `updateLoanParams()` to set the `ltvBPS` value to `0`
3.  call `removeCollateral()` to steal the collateral from the contract

### Recommended Mitigation Steps

Don't allow `updateLoanParams()` to change the `ltvBPS` value.

**[cryptolyndon (AbraNFT) confirmed and commented](https://github.com/code-423n4/2022-04-abranft-findings/issues/51#issuecomment-1118132221):**
 > Confirmed, and the first to report this particular exploit.



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
| Finders | IllIllI, BowTiedWardens, scaraven, Ruhum, gzeon, WatchPug, plotchy |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-abranft
- **GitHub**: https://github.com/code-423n4/2022-04-abranft-findings/issues/51
- **Contest**: https://code4rena.com/contests/2022-04-abranft-contest

### Keywords for Search

`vulnerability`

